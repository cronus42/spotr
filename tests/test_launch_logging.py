import unittest
from six.moves import mock

from spotr.launch import _log_instance_creation


class TestLaunchLogging(unittest.TestCase):
    def test_log_instance_creation_with_id(self):
        """Test that instance creation logging includes the instance ID"""
        instance = mock.Mock()
        instance.id = 'i-1234567890abcdef0'
        instance.ip_address = '203.0.113.42'
        key_path = '/home/user/.ssh/my-key.pem'
        
        with mock.patch('builtins.print') as mock_print:
            _log_instance_creation(instance, key_path)
            
            # Verify the correct log messages are printed
            expected_calls = [
                mock.call(">> Instance i-1234567890abcdef0 launched, connect with:"),
                mock.call("ssh -i /home/user/.ssh/my-key.pem ubuntu@203.0.113.42")
            ]
            mock_print.assert_has_calls(expected_calls)

    def test_log_instance_creation_empty_id(self):
        """Test that logging works even with empty instance ID"""
        instance = mock.Mock()
        instance.id = ''
        instance.ip_address = '198.51.100.123'
        key_path = '/path/to/key.pem'
        
        with mock.patch('builtins.print') as mock_print:
            _log_instance_creation(instance, key_path)
            
            # Verify the log message still includes the empty ID
            expected_calls = [
                mock.call(">> Instance  launched, connect with:"),
                mock.call("ssh -i /path/to/key.pem ubuntu@198.51.100.123")
            ]
            mock_print.assert_has_calls(expected_calls)

    def test_log_instance_creation_special_characters(self):
        """Test that logging handles special characters in paths and IDs"""
        instance = mock.Mock()
        instance.id = 'i-special_chars-123'
        instance.ip_address = '192.0.2.10'
        key_path = '/home/user/keys/my key with spaces.pem'
        
        with mock.patch('builtins.print') as mock_print:
            _log_instance_creation(instance, key_path)
            
            # Verify special characters are handled properly
            expected_calls = [
                mock.call(">> Instance i-special_chars-123 launched, connect with:"),
                mock.call("ssh -i /home/user/keys/my key with spaces.pem ubuntu@192.0.2.10")
            ]
            mock_print.assert_has_calls(expected_calls)
