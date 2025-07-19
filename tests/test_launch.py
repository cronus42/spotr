import unittest
from six.moves import mock
from mock import Mock

from spotr.launch import _log_instance_creation


class TestLaunch(unittest.TestCase):
    def test_log_instance_creation_integration(self):
        """Test that the log instance creation function works with instance ID"""
        instance = Mock()
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
