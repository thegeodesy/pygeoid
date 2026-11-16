"""Exercise publication guards using independent wheel and source metadata."""

import io
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_release import validate


class ReleaseValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def distributions(self, wheel="1.2.3", sdist=None, project="example"):
        if sdist is None:
            sdist = wheel

        def metadata(version):
            return (
                f"Metadata-Version: 2.4\nName: {project}\nVersion: {version}\n".encode()
            )

        with zipfile.ZipFile(self.directory / "example.whl", "w") as archive:
            archive.writestr("example.dist-info/METADATA", metadata(wheel))
        with tarfile.open(self.directory / "example.tar.gz", "w:gz") as archive:
            data = metadata(sdist)
            info = tarfile.TarInfo("example/PKG-INFO")
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))

    def test_matching_release(self):
        self.distributions()
        self.assertEqual(validate("example", self.directory, "v1.2.3"), "1.2.3")

    def test_prerelease(self):
        self.distributions("1.3.0rc1")
        self.assertEqual(validate("example", self.directory, "v1.3.0rc1"), "1.3.0rc1")

    def test_wrong_tag(self):
        self.distributions()
        with self.assertRaisesRegex(ValueError, "tag"):
            validate("example", self.directory, "v1.2.4")

    def test_mismatched_artifacts(self):
        self.distributions(sdist="1.2.4")
        with self.assertRaisesRegex(ValueError, "differ"):
            validate("example", self.directory)

    def test_wrong_project(self):
        self.distributions(project="another-project")
        with self.assertRaisesRegex(ValueError, "name"):
            validate("example", self.directory)

    def test_fallback_version(self):
        self.distributions("0.0.0")
        with self.assertRaisesRegex(ValueError, "Fallback"):
            validate("example", self.directory)

    def test_development_tag(self):
        self.distributions("1.3.0.dev1")
        with self.assertRaisesRegex(ValueError, "development"):
            validate("example", self.directory, "v1.3.0.dev1")

    def test_ambiguous_artifacts(self):
        self.distributions()
        (self.directory / "second.whl").write_bytes(b"unexpected")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            validate("example", self.directory)
