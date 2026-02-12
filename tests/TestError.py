import unittest
import sys
import os
from unittest.mock import patch
from PyQt6.QtWidgets import QApplication

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import Error

class TestError(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        self.error_text = "Test error"
        self.error = Error(self.error_text)

    def tearDown(self):
        self.error.close()

    def test_error_creation(self):
        self.assertIsNotNone(self.error)
        self.assertEqual(self.error.text, self.error_text)

    @patch("main.QMessageBox.critical")
    def test_send_error_calls_message_box(self, mock_critical):
        self.error.send_error()
        mock_critical.assert_called_once()
        args, kwargs = mock_critical.call_args

        self.assertEqual(args[0], self.error)
        self.assertEqual(args[1], "Error")
        self.assertEqual(args[2], self.error_text)

    def test_error_is_qwidget(self):
        from PyQt6.QtWidgets import QWidget
        self.assertIsInstance(self.error, QWidget)

if __name__ == "__main__":
    unittest.main(verbosity=2)