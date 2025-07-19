import unittest
from unittest import mock

from spotr.list import list_instances


class TestList(unittest.TestCase):
    @mock.patch('spotr.list.find_instances')
    @mock.patch('spotr.list.Config')
    @mock.patch('spotr.list.build_client')
    @mock.patch('builtins.print')
    def test_list_instances_with_results(self, mock_print, mock_build_client, mock_config, mock_find_instances):
        """Test listing instances when instances are found"""
        # Mock dependencies
        args = mock.Mock()
        client = mock.Mock()
        config = mock.Mock()
        mock_build_client.return_value = client
        mock_config.return_value = config
        
        # Mock instances
        instance1 = mock.Mock()
        instance1.id = 'i-1234567890abcdef0'
        instance1.ip_address = '192.0.2.1'
        instance1.launch_time = '2025-07-19T08:00:00.000Z'
        instance1.security_groups = ['sg-12345678']
        
        instance2 = mock.Mock()
        instance2.id = 'i-0fedcba0987654321'
        instance2.ip_address = '203.0.113.2'
        instance2.launch_time = '2025-07-19T09:00:00.000Z'
        instance2.security_groups = ['sg-87654321', 'sg-abcdef12']
        
        mock_find_instances.return_value = [instance1, instance2]
        
        list_instances(args)
        
        # Verify calls
        mock_build_client.assert_called_once_with(args)
        mock_config.assert_called_once_with(client, args)
        mock_find_instances.assert_called_once_with(client, config)
        
        # Verify print statements
        expected_prints = [
            mock.call('\nFound 2 instances'),
            mock.call('Instance ID: i-1234567890abcdef0'),
            mock.call('IP Address: 192.0.2.1'),
            mock.call('Launch Time: 2025-07-19T08:00:00.000Z'),
            mock.call('Security Groups: [\'sg-12345678\']'),
            mock.call('Instance ID: i-0fedcba0987654321'),
            mock.call('IP Address: 203.0.113.2'),
            mock.call('Launch Time: 2025-07-19T09:00:00.000Z'),
            mock.call('Security Groups: [\'sg-87654321\', \'sg-abcdef12\']')
        ]
        mock_print.assert_has_calls(expected_prints)

    @mock.patch('spotr.list.find_instances')
    @mock.patch('spotr.list.Config')
    @mock.patch('spotr.list.build_client')
    @mock.patch('builtins.print')
    def test_list_instances_no_results(self, mock_print, mock_build_client, mock_config, mock_find_instances):
        """Test listing instances when no instances are found"""
        # Mock dependencies
        args = mock.Mock()
        client = mock.Mock()
        config = mock.Mock()
        mock_build_client.return_value = client
        mock_config.return_value = config
        mock_find_instances.return_value = []
        
        list_instances(args)
        
        # Verify calls
        mock_build_client.assert_called_once_with(args)
        mock_config.assert_called_once_with(client, args)
        mock_find_instances.assert_called_once_with(client, config)
        
        # Verify print statements
        expected_prints = [
            mock.call('\nFound 0 instances'),
            mock.call('No instances found')
        ]
        mock_print.assert_has_calls(expected_prints)

    @mock.patch('spotr.list.find_instances')
    @mock.patch('spotr.list.Config')
    @mock.patch('spotr.list.build_client')
    @mock.patch('builtins.print')
    def test_list_instances_single_result(self, mock_print, mock_build_client, mock_config, mock_find_instances):
        """Test listing instances when only one instance is found"""
        # Mock dependencies
        args = mock.Mock()
        client = mock.Mock()
        config = mock.Mock()
        mock_build_client.return_value = client
        mock_config.return_value = config
        
        # Mock single instance
        instance = mock.Mock()
        instance.id = 'i-1234567890abcdef0'
        instance.ip_address = '192.0.2.1'
        instance.launch_time = '2025-07-19T08:00:00.000Z'
        instance.security_groups = []
        
        mock_find_instances.return_value = [instance]
        
        list_instances(args)
        
        # Verify calls
        mock_build_client.assert_called_once_with(args)
        mock_config.assert_called_once_with(client, args)
        mock_find_instances.assert_called_once_with(client, config)
        
        # Verify print statements
        expected_prints = [
            mock.call('\nFound 1 instances'),
            mock.call('Instance ID: i-1234567890abcdef0'),
            mock.call('IP Address: 192.0.2.1'),
            mock.call('Launch Time: 2025-07-19T08:00:00.000Z'),
            mock.call('Security Groups: []')
        ]
        mock_print.assert_has_calls(expected_prints)
