"""Check distribution identity and release-tag consistency before publication."""

import argparse
import os
import tarfile
import zipfile
from email.parser import BytesParser
from pathlib import Path

from packaging.utils import canonicalize_name
from packaging.version import Version


def validate(project: str, directory: Path, tag: str = "") -> str:
    wheels = list(directory.glob("*.whl"))
    sdists = list(directory.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise ValueError("Expected exactly one wheel and one source distribution")
    with zipfile.ZipFile(wheels[0]) as archive:
        names = [n for n in archive.namelist() if n.endswith(".dist-info/METADATA")]
        if len(names) != 1:
            raise ValueError("Wheel must contain exactly one METADATA file")
        wheel = BytesParser().parsebytes(archive.read(names[0]))
    with tarfile.open(sdists[0]) as archive:
        names = [
            m
            for m in archive.getmembers()
            if m.name.count("/") == 1 and m.name.endswith("/PKG-INFO")
        ]
        if len(names) != 1:
            raise ValueError("Source distribution must contain root PKG-INFO")
        stream = archive.extractfile(names[0])
        if stream is None:
            raise ValueError("Missing source metadata")
        sdist = BytesParser().parsebytes(stream.read())
    versions = []
    for metadata in (wheel, sdist):
        if canonicalize_name(metadata["Name"]) != canonicalize_name(project):
            raise ValueError("Distribution project name does not match")
        version = Version(metadata["Version"])
        if str(version) in {"0.0.0", "0+unknown"}:
            raise ValueError("Fallback versions cannot be distributed")
        versions.append(version)
    if versions[0] != versions[1]:
        raise ValueError("Wheel and source versions differ")
    if tag:
        if not tag.startswith("v"):
            raise ValueError("Release tags must use v followed by a version")
        expected = Version(tag[1:])
        if expected.is_devrelease or expected.local:
            raise ValueError("Release tags cannot use development or local versions")
        if versions[0] != expected:
            raise ValueError("Distribution version does not match the release tag")
    return str(versions[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--directory", type=Path, default=Path("dist"))
    args = parser.parse_args()
    print(validate(args.project, args.directory, os.environ.get("RELEASE_TAG", "")))
