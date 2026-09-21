import io
import unittest
import zipfile
from releasekit import create_package as build


class PackageTests(unittest.TestCase):
    def test_entries_and_crc(self):
        records = [('bin/launch', b'\x00\xfflaunch', 0o755),
                   ('etc/settings', b'', 0o640)]
        with zipfile.ZipFile(io.BytesIO(build(records))) as archive:
            self.assertEqual(archive.namelist(), ['bin/launch', 'etc/settings'])
            self.assertIsNone(archive.testzip())

    def test_empty_package(self):
        with zipfile.ZipFile(io.BytesIO(build([]))) as archive:
            self.assertEqual(archive.namelist(), [])
            self.assertIsNone(archive.testzip())
