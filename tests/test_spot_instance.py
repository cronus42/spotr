import unittest
import boto3
from unittest import mock

from spotr.spot_instance import request, SpotInstanceRequest

class TestSpotInstance(unittest.TestCase):
    def runTest(self):
        config = mock.Mock(
            max_bid=0.30,
            ami='1234',
            key_name='test_ssh_key',
            type='p2.xlarge',
            az='us-west-2a',
            security_group_id=None,
            iam_instance_profile_arn=None,
            user_data=None,
            subnet_id='subnet-12345',
            ebs_optimized=False,
            root_volume_size=None,
            root_device_name=None
        )
        fake_client = mock.Mock(boto3.client('ec2'))
        waiter_mock = mock.Mock()
        waiter_mock.wait = mock.Mock()
        attrs = {
            'request_spot_instances.return_value': {
                'SpotInstanceRequests': [
                    {'SpotInstanceRequestId': '123456'}
                ]
            },
            'describe_spot_instance_requests.return_value': {
                'SpotInstanceRequests': [
                    {'InstanceId': '123456', 'Status': { 'Code': 'fulfilled' } }
                ]
            },
            'get_waiter.return_value': waiter_mock
        }
        fake_client.configure_mock(**attrs)

        instance = mock.Mock(has_security_groups=True)
        tag = mock.Mock()
        get_by_instance_id = mock.Mock(return_value=instance)
        open_port = mock.Mock(return_value=True)
        response = request(fake_client, config, tag, get_by_instance_id, open_port)
        self.assertEqual(response, instance)

    def test_spot_request_price_too_low(self):
        """Test error handling when spot price is too low"""
        config = mock.Mock(
            max_bid='0.01',
            ami='ami-1234',
            key_name='test_ssh_key',
            type='p2.xlarge',
            az='us-west-2a',
            security_group_id=None,
            iam_instance_profile_arn=None,
            user_data=None,
            subnet_id='subnet-12345',
            ebs_optimized=False,
            root_volume_size=None,
            root_device_name=None
        )
        fake_client = mock.Mock(boto3.client('ec2'))
        waiter_mock = mock.Mock()
        waiter_mock.wait = mock.Mock()
        attrs = {
            'request_spot_instances.return_value': {
                'SpotInstanceRequests': [
                    {'SpotInstanceRequestId': '123456'}
                ]
            },
            'describe_spot_instance_requests.return_value': {
                'SpotInstanceRequests': [
                    {
                        'InstanceId': '123456', 
                        'Status': { 
                            'Code': 'price-too-low',
                            'Message': 'Your bid price is too low'
                        } 
                    }
                ]
            },
            'get_waiter.return_value': waiter_mock
        }
        fake_client.configure_mock(**attrs)

        tag = mock.Mock()
        get_by_instance_id = mock.Mock()
        open_port = mock.Mock()
        
        with self.assertRaises(RuntimeError) as cm:
            request(fake_client, config, tag, get_by_instance_id, open_port)
            
        self.assertEqual(str(cm.exception), 'Your bid price is too low')

    def test_spot_request_with_user_data(self):
        """Test spot request with user data encoding"""
        config = mock.Mock(
            max_bid='0.30',
            ami='ami-1234',
            key_name='test_ssh_key',
            type='p2.xlarge',
            az='us-west-2a',
            security_group_id='sg-12345',
            iam_instance_profile_arn='arn:aws:iam::123456789012:instance-profile/MyRole',
            user_data='#!/bin/bash\necho "Hello World"',
            subnet_id='subnet-12345',
            ebs_optimized=True,
            root_volume_size=None,
            root_device_name=None
        )
        fake_client = mock.Mock(boto3.client('ec2'))
        waiter_mock = mock.Mock()
        waiter_mock.wait = mock.Mock()
        attrs = {
            'request_spot_instances.return_value': {
                'SpotInstanceRequests': [
                    {'SpotInstanceRequestId': '123456'}
                ]
            },
            'describe_spot_instance_requests.return_value': {
                'SpotInstanceRequests': [
                    {'InstanceId': '123456', 'Status': { 'Code': 'fulfilled' } }
                ]
            },
            'get_waiter.return_value': waiter_mock
        }
        fake_client.configure_mock(**attrs)

        instance = mock.Mock(has_security_groups=True)
        tag = mock.Mock()
        get_by_instance_id = mock.Mock(return_value=instance)
        open_port = mock.Mock(return_value=True)
        response = request(fake_client, config, tag, get_by_instance_id, open_port)
        
        # Verify that the request was made with proper encoding
        call_args = fake_client.request_spot_instances.call_args
        self.assertIn('UserData', call_args[1]['LaunchSpecification'])
        # UserData should be base64 encoded
        user_data = call_args[1]['LaunchSpecification']['UserData']
        import base64
        decoded = base64.b64decode(user_data.encode('ascii')).decode('ascii')
        self.assertEqual(decoded, '#!/bin/bash\necho "Hello World"')
        
        self.assertEqual(response, instance)

    def test_spot_request_with_root_volume_size(self):
        """Test spot request includes BlockDeviceMappings when root volume size is set"""
        config = mock.Mock(
            max_bid='0.30',
            ami='ami-1234',
            key_name='test_ssh_key',
            type='p2.xlarge',
            az='us-west-2a',
            security_group_id='sg-12345',
            iam_instance_profile_arn=None,
            user_data=None,
            subnet_id='subnet-12345',
            ebs_optimized=False,
            root_volume_size=256,
            root_device_name='/dev/sda1'
        )
        fake_client = mock.Mock(boto3.client('ec2'))
        waiter_mock = mock.Mock()
        waiter_mock.wait = mock.Mock()
        attrs = {
            'request_spot_instances.return_value': {
                'SpotInstanceRequests': [
                    {'SpotInstanceRequestId': '123456'}
                ]
            },
            'describe_spot_instance_requests.return_value': {
                'SpotInstanceRequests': [
                    {'InstanceId': '123456', 'Status': { 'Code': 'fulfilled' } }
                ]
            },
            'get_waiter.return_value': waiter_mock
        }
        fake_client.configure_mock(**attrs)

        instance = mock.Mock(has_security_groups=True)
        tag = mock.Mock()
        get_by_instance_id = mock.Mock(return_value=instance)
        open_port = mock.Mock(return_value=True)
        request(fake_client, config, tag, get_by_instance_id, open_port)

        call_args = fake_client.request_spot_instances.call_args
        launch_spec = call_args[1]['LaunchSpecification']
        self.assertIn('BlockDeviceMappings', launch_spec)
        self.assertEqual(
            launch_spec['BlockDeviceMappings'],
            [
                {
                    'DeviceName': '/dev/sda1',
                    'Ebs': {
                        'VolumeSize': 256,
                        'DeleteOnTermination': True
                    }
                }
            ]
        )

    def test_spot_instance_request_init(self):
        """Test SpotInstanceRequest class initialization"""
        response_data = {
            'InstanceId': 'i-1234567890abcdef0',
            'Status': {
                'Code': 'fulfilled',
                'Message': 'Your spot request has been fulfilled'
            }
        }
        
        spot_request = SpotInstanceRequest(response_data)
        
        self.assertEqual(spot_request.instance_id, 'i-1234567890abcdef0')
        self.assertEqual(spot_request.status_code, 'fulfilled')
        self.assertEqual(spot_request.status_message, 'Your spot request has been fulfilled')
