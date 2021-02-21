import unittest
import os
import sys

class test_pure_ascii(unittest.TestCase):

    #################################################################
    #
    # Tests.
    
    def test_pure_ascii(self):
        test_pure_ascii.create_text_file("abc\tABC1\n23-+=\r;'.>/?\\|~")
        self.verify_clean(test_pure_ascii.run_pure_ascii())

    def test_ascii_with_one_zero(self):
        test_pure_ascii.create_text_file("abc\x00ABC")
        self.verify_one_zero(test_pure_ascii.run_pure_ascii())

    def test_ascii_with_two_zeros(self):
        test_pure_ascii.create_text_file("abc\x00A\nB\x00C")
        self.verify_zeros(test_pure_ascii.run_pure_ascii())

    def test_ascii_with_multiple_zeros(self):
        test_pure_ascii.create_text_file("abc\x00\x00AB\x00C")
        self.verify_zeros(test_pure_ascii.run_pure_ascii())

    def test_non_ascii(self):
        test_pure_ascii.create_bytes_file(b"A\x00BC\n\n33\n\xc2\xad\x12ABC==")
        self.verify_non_ascii(test_pure_ascii.run_pure_ascii(), 9)


    #################################################################
    #
    # Test file helpers.

    @staticmethod
    def get_test_file_name():
        return 'pure_ascii_test_file.dat'

    @staticmethod
    def create_bytes_file(data: bytes):
        with open(test_pure_ascii.get_test_file_name(), 'wb') as f:
            f.write(data)

    @staticmethod
    def create_text_file(text: str):
        with open(test_pure_ascii.get_test_file_name(), 'w') as f:
            f.write(text)

    @staticmethod
    def run_pure_ascii():
        python = sys.executable
        fn = test_pure_ascii.get_test_file_name()
        cmd = f"{python} pure_ascii.py {fn}"
        return os.popen(cmd)


    #################################################################
    #
    # Verify pure ASCII results helpers.

    def merge_lines(self, f):
        lines = [line for line in f]
        return ' '.join(lines)

    def verify_clean(self, f):
        lines = self.merge_lines(f)
        self.assertNotIn('Error:', lines)
        self.assertNotIn('Warning:', lines)

    def verify_one_zero(self, f):
        lines = self.merge_lines(f)
        self.assertNotIn('Error:', lines)
        self.assertIn('contains a zero byte at offset', lines)
        self.assertNotIn('zero bytes', lines)

    def verify_zeros(self, f):
        lines = self.merge_lines(f)
        self.assertNotIn('Error:', lines)
        self.assertIn('contains a zero byte at offset', lines)
        self.assertIn('zero bytes', lines)

    def verify_non_ascii(self, f, bad_offset: int):
        lines = self.merge_lines(f)
        self.assertIn('Error:', lines)
        self.assertIn(str(bad_offset), lines)
        self.assertNotIn('Warning:', lines)

