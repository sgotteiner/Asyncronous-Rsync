import unittest
import os
import shutil
import tempfile
from sender_multiprocessing import parallel_rsync_transfer

# Constants for file names and sizes
FILE_5MB = 'file_5mb.txt'
FILE_5MB_SIZE = 5 * 1024 * 1024
FILE_10MB = 'file_10mb.txt'
FILE_10MB_SIZE = 10 * 1024 * 1024

class CustomTextTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asserts_passed = 0
        self.asserts_failed = 0

    def addSuccess(self, test):
        super().addSuccess(test)
        self.asserts_passed += 1

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.asserts_failed += 1

    def stopTest(self, test):
        result_str = f"{test}: {self.asserts_passed} passed, {self.asserts_failed} failed"
        self.stream.writeln(result_str)
        self.asserts_passed = 0
        self.asserts_failed = 0

class CustomTextTestRunner(unittest.TextTestRunner):
    resultclass = CustomTextTestResult

class TestFileTransfer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create temporary folders for source and destination
        cls.source_dir = tempfile.mkdtemp()
        cls.destination_dir = tempfile.mkdtemp()

        # Create test files in the source folder
        cls.create_test_files()

        # Perform parallel transfers and measure time
        cls.total_time_sequential, cls.total_time_parallel = parallel_rsync_transfer([
            os.path.join(cls.source_dir, FILE_5MB),
            os.path.join(cls.source_dir, FILE_10MB)
        ], cls.destination_dir, 0)

    @classmethod
    def create_test_files(cls):
        # Create test files (5MB and 10MB) in the source folder
        with open(os.path.join(cls.source_dir, FILE_5MB), 'wb') as f:
            f.write(b'a' * FILE_5MB_SIZE)  # 5MB file
        with open(os.path.join(cls.source_dir, FILE_10MB), 'wb') as f:
            f.write(b'a' * FILE_10MB_SIZE)  # 10MB file

    @classmethod
    def tearDownClass(cls):
        # Clean up: Delete temporary folders
        shutil.rmtree(cls.source_dir)
        shutil.rmtree(cls.destination_dir)

    def test_parallel_transfers_faster_than_sequential(self):
        # Check if parallel transfers are faster than sequential transfers
        self.assertLess(self.total_time_parallel, self.total_time_sequential,
                        msg="Parallel transfers should take less time than sequential transfers")

    def test_files_exist_in_destination(self):
        # Check if the files exist in the destination folder
        file_5mb_dest = os.path.join(self.destination_dir, FILE_5MB)
        file_10mb_dest = os.path.join(self.destination_dir, FILE_10MB)
        self.assertTrue(os.path.exists(file_5mb_dest),
                        msg=f"{FILE_5MB} should exist in the destination folder")
        self.assertTrue(os.path.exists(file_10mb_dest),
                        msg=f"{FILE_10MB} should exist in the destination folder")

    def test_files_have_correct_sizes(self):
        # Check if the transferred files have the correct sizes
        file_5mb_dest = os.path.join(self.destination_dir, FILE_5MB)
        file_10mb_dest = os.path.join(self.destination_dir, FILE_10MB)
        self.assertEqual(os.path.getsize(file_5mb_dest), FILE_5MB_SIZE,
                        msg=f"{FILE_5MB} should have the correct size")
        self.assertEqual(os.path.getsize(file_10mb_dest), FILE_10MB_SIZE,
                        msg=f"{FILE_10MB} should have the correct size")

if __name__ == '__main__':
    runner = CustomTextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
