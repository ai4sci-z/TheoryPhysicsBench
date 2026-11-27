#!/usr/bin/env python3
"""Restore the source archive from the base64 parts in this repository."""

import argparse
import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tarfile
import tempfile


def restore(manifest_path, destination, archive_only=False):
    manifest_path = manifest_path.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    archive_name = manifest["archive"]
    if Path(archive_name).name != archive_name:
        raise ValueError("Invalid archive filename in manifest")
    archive_path = manifest_path.parent / archive_name
    digest = hashlib.sha256()
    size = 0
    with tempfile.NamedTemporaryFile(dir=manifest_path.parent, delete=False) as out:
        temporary_path = Path(out.name)
        try:
            for part in manifest["parts"]:
                name = part["name"]
                if Path(name).name != name:
                    raise ValueError("Invalid part filename in manifest")
                encoded = (manifest_path.parent / name).read_bytes()
                if hashlib.sha256(encoded).hexdigest() != part["sha256"]:
                    raise ValueError("Checksum mismatch: " + name)
                data = base64.b64decode(encoded, validate=True)
                out.write(data)
                digest.update(data)
                size += len(data)
            if size != manifest["bytes"] or digest.hexdigest() != manifest["sha256"]:
                raise ValueError("Archive checksum or size mismatch")
        except BaseException:
            temporary_path.unlink(missing_ok=True)
            raise
    temporary_path.replace(archive_path)
    print("Verified:", archive_name, "(" + str(size) + " bytes)")
    if archive_only:
        return

    destination = destination.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("Extraction directory must be empty: " + str(destination))
    with tarfile.open(archive_path, "r:*") as archive:
        members = archive.getmembers()
        for member in members:
            path = PurePosixPath(member.name)
            if path.is_absolute() or ".." in path.parts or "\\" in member.name:
                raise ValueError("Unsafe archive path: " + member.name)
            if not (member.isfile() or member.isdir()):
                raise ValueError("Unsupported archive entry: " + member.name)
        destination.mkdir(parents=True, exist_ok=True)
        for member in members:
            target = destination.joinpath(*PurePosixPath(member.name).parts)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.extractfile(member) as source, target.open("xb") as output:
                shutil.copyfileobj(source, output)
            target.chmod(0o755 if member.mode & 0o111 else 0o644)
    print("Restored:", destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path(__file__).resolve().parent / "source-core.json")
    parser.add_argument("--destination", type=Path, default=Path("restored-source"))
    parser.add_argument("--archive-only", action="store_true")
    args = parser.parse_args()
    try:
        restore(args.manifest, args.destination, args.archive_only)
    except (OSError, ValueError, KeyError, tarfile.TarError) as error:
        parser.exit(1, "Restore failed: " + str(error) + "\n")


if __name__ == "__main__":
    main()
