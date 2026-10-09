#!/usr/bin/env python3
"""Read-only ZIP integrity and local recovery-manifest verification."""
import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest().upper()


def inspect_archive(path):
    with zipfile.ZipFile(path) as archive:
        files = [entry for entry in archive.infolist() if not entry.is_dir()]
        if not files:
            raise ValueError('Archive contains no files.')
        names = [entry.filename for entry in files]
        if len(names) != len(set(names)):
            raise ValueError('Archive contains duplicate entry paths.')
        if archive.testzip() is not None:
            raise ValueError('Archive CRC validation failed.')
        primary = backups = images = 0
        titles = set()
        for entry in files:
            parts = entry.filename.replace('\\', '/').split('/')
            titles.update(part for part in parts if re.fullmatch(r'PPSA\d{4,8}', part))
            name = parts[-1]
            if name.startswith('sdimg_'):
                with archive.open(entry) as stream:
                    header = stream.read(1)
                if header == b'\x02':
                    images += 1
                    if name.startswith('sdimg_sce_bu_'):
                        backups += 1
                    else:
                        primary += 1
        return {
            'archive_sha256': sha256(path),
            'zip_crc_validation': 'Passed',
            'file_count': len(files),
            'uncompressed_bytes': sum(entry.file_size for entry in files),
            'ps5_image_header_count': images,
            'primary_ps5_images': primary,
            'backup_ps5_images': backups,
            'ps5_title_ids': sorted(titles),
            'internal_save_validity': 'Not established by archive inspection',
        }


def verify_backup(directory, manifest_path):
    manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    entries = manifest if isinstance(manifest, list) else [manifest]
    if not entries:
        raise ValueError('Backup manifest is empty.')
    root = directory.resolve(strict=True)
    seen = set()
    checked = 0
    for entry in entries:
        name = entry.get('Save')
        expected_hash = entry.get('SHA256')
        expected_length = entry.get('Length')
        if not isinstance(name, str) or not re.fullmatch(r'sdimg_[A-Za-z0-9_-]+', name):
            raise ValueError('Manifest contains an unsafe filename.')
        if name in seen:
            raise ValueError('Manifest contains duplicate filenames.')
        seen.add(name)
        if not isinstance(expected_hash, str) or not re.fullmatch(r'[A-Fa-f0-9]{64}', expected_hash):
            raise ValueError('Manifest has an invalid SHA-256 value.')
        if type(expected_length) is not int or expected_length < 0:
            raise ValueError('Manifest has an invalid file length.')
        path = (root / name).resolve(strict=True)
        if path.parent != root or not path.is_file():
            raise ValueError('Manifest path does not resolve to a file inside the backup directory.')
        if path.stat().st_size != expected_length or sha256(path) != expected_hash.upper():
            raise ValueError('Backup length or checksum verification failed.')
        checked += 1
    return {'backup_files_verified': checked, 'length_and_sha256': 'Passed', 'console_second_read': 'Requires separate verification'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--backup-dir', type=Path)
    parser.add_argument('--manifest', type=Path)
    args = parser.parse_args()
    if bool(args.backup_dir) != bool(args.manifest):
        parser.error('--backup-dir and --manifest must be supplied together')
    if not args.archive and not args.backup_dir:
        parser.error('supply --archive and/or --backup-dir with --manifest')
    result = {}
    try:
        if args.archive:
            result['archive'] = inspect_archive(args.archive)
        if args.backup_dir:
            result['backup'] = verify_backup(args.backup_dir, args.manifest)
    except ValueError as error:
        print(json.dumps({'status': 'Failed', 'reason': str(error)}))
        return 1
    except (OSError, zipfile.BadZipFile, RuntimeError, KeyError, TypeError):
        print(json.dumps({'status': 'Failed', 'reason': 'Archive or backup is unreadable or malformed; raw paths and details withheld.'}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
