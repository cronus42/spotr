import unittest
import boto3
from unittest import mock

from spotr.dns import build_client, set_record


class TestDns(unittest.TestCase):
    def test_build_client_with_region(self):
        """Test DNS client creation with region specified"""
        args = mock.Mock()
        args.region = 'us-west-2'
        args.aws_access_key_id = None
        args.aws_secret_access_key = None
        
        with mock.patch('boto3.setup_default_session') as mock_setup:
            with mock.patch('boto3.client') as mock_client:
                build_client(args)
                mock_setup.assert_called_once_with(region_name='us-west-2')
                mock_client.assert_called_once_with('route53')

    def test_build_client_with_credentials(self):
        """Test DNS client creation with explicit AWS credentials"""
        args = mock.Mock()
        args.region = None
        args.aws_access_key_id = 'test_key_id'
        args.aws_secret_access_key = 'test_secret_key'
        
        with mock.patch('boto3.client') as mock_client:
            build_client(args)
            mock_client.assert_called_once_with(
                'route53',
                aws_access_key_id='test_key_id',
                aws_secret_access_key='test_secret_key'
            )

    def test_build_client_default(self):
        """Test DNS client creation with default settings"""
        args = mock.Mock()
        args.region = None
        args.aws_access_key_id = None
        args.aws_secret_access_key = None
        
        with mock.patch('boto3.client') as mock_client:
            build_client(args)
            mock_client.assert_called_once_with('route53')

    def test_set_record(self):
        """Test DNS record setting functionality"""
        client = mock.Mock()
        instance = mock.Mock()
        instance.ip_address = '192.168.1.100'
        
        config = mock.Mock()
        config.record_name = 'test.example.com'
        config.hosted_zone_id = 'Z1234567890ABC'
        
        # Capture print output for verification (logging improvement test)
        with mock.patch('builtins.print') as mock_print:
            set_record(client, instance, config)
            
            # Verify the print statement was called (testing logging improvement)
            mock_print.assert_called_once_with(
                "Setting DNS record test.example.com to point to IP address 192.168.1.100..."
            )
        
        # Verify the Route53 API was called correctly
        client.change_resource_record_sets.assert_called_once_with(
            HostedZoneId='Z1234567890ABC',
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': 'test.example.com',
                            'Type': 'A',
                            'TTL': 300,
                            'ResourceRecords': [
                                {'Value': '192.168.1.100'},
                            ],
                        }
                    },
                ]
            }
        )
