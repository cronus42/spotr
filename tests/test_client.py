import unittest
from unittest import mock

from spotr.client import build


class TestClient(unittest.TestCase):
    @mock.patch('spotr.client.boto3')
    def test_build_with_region(self, mock_boto3):
        """Test client creation with region specified"""
        args = mock.Mock()
        args.region = 'us-west-2'
        args.aws_access_key_id = None
        args.aws_secret_access_key = None
        
        mock_client = mock.Mock()
        mock_boto3.client.return_value = mock_client
        
        result = build(args)
        
        # Should set up default session with region
        mock_boto3.setup_default_session.assert_called_once_with(region_name='us-west-2')
        mock_boto3.client.assert_called_once_with('ec2')
        self.assertEqual(result, mock_client)

    @mock.patch('spotr.client.boto3')
    def test_build_with_credentials(self, mock_boto3):
        """Test client creation with explicit AWS credentials"""
        args = mock.Mock()
        args.region = None
        args.aws_access_key_id = 'AKIAIOSFODNN7EXAMPLE'
        args.aws_secret_access_key = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY'
        
        mock_client = mock.Mock()
        mock_boto3.client.return_value = mock_client
        
        result = build(args)
        
        # Should not set up default session when no region
        mock_boto3.setup_default_session.assert_not_called()
        mock_boto3.client.assert_called_once_with(
            'ec2',
            aws_access_key_id='AKIAIOSFODNN7EXAMPLE',
            aws_secret_access_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY'
        )
        self.assertEqual(result, mock_client)

    @mock.patch('spotr.client.boto3')
    def test_build_default(self, mock_boto3):
        """Test client creation with default settings"""
        args = mock.Mock()
        args.region = None
        args.aws_access_key_id = None
        args.aws_secret_access_key = None
        
        mock_client = mock.Mock()
        mock_boto3.client.return_value = mock_client
        
        result = build(args)
        
        # Should use default credentials and no region setup
        mock_boto3.setup_default_session.assert_not_called()
        mock_boto3.client.assert_called_once_with('ec2')
        self.assertEqual(result, mock_client)

    @mock.patch('spotr.client.boto3')
    def test_build_with_region_and_credentials(self, mock_boto3):
        """Test client creation with both region and credentials"""
        args = mock.Mock()
        args.region = 'eu-central-1'
        args.aws_access_key_id = 'AKIAIOSFODNN7EXAMPLE'
        args.aws_secret_access_key = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY'
        
        mock_client = mock.Mock()
        mock_boto3.client.return_value = mock_client
        
        result = build(args)
        
        # Should set up region and use credentials
        mock_boto3.setup_default_session.assert_called_once_with(region_name='eu-central-1')
        mock_boto3.client.assert_called_once_with(
            'ec2',
            aws_access_key_id='AKIAIOSFODNN7EXAMPLE',
            aws_secret_access_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY'
        )
        self.assertEqual(result, mock_client)
