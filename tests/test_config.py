import unittest
import boto3
from pathlib import Path

from unittest import mock

from spotr.config import Config


class TestConfig(unittest.TestCase):
    def test_ami_tag(self):
        args = mock_args({'ami_tag': 'my_tag'})
        conf = Config(mock_client(), args, "./non-existent-config")
        self.assertEqual(conf.ami_tag, 'my_tag')

    def test_default_ami_tag(self):
        args = mock_args({})
        conf = Config(mock_client(), args, "./non-existent-config")
        self.assertEqual(conf.ami_tag, 'spotr')

    def test_no_config_file(self):
        args = mock_args({})
        conf = Config(mock_client(), args, "./non-existent-config")
        self.assertEqual(conf.key_name, 'spotr')

    def test_config_file(self):
        args = mock_args({})
        fixture_path = Path(__file__).parent / "fixtures" / "config"
        conf = Config(mock_client(), args, str(fixture_path))
        self.assertEqual(conf.key_name, 'test_key_name')

    def test_root_volume_size_from_args(self):
        args = mock_args({'root_volume_size': 128})
        conf = Config(mock_client(), args, "./non-existent-config")
        self.assertEqual(conf.root_volume_size, 128)

    def test_root_device_name_from_ami_lookup(self):
        fake_client = mock_client()
        fake_client.describe_images.return_value = {
            'Images': [{'RootDeviceName': '/dev/sda1'}]
        }
        args = mock_args({'ami': 'ami-1234', 'root_volume_size': 128})
        conf = Config(fake_client, args, "./non-existent-config")
        self.assertEqual(conf.root_device_name, '/dev/sda1')


def mock_client():
    fake_client = mock.Mock(boto3.client('ec2'))
    attrs = {}
    fake_client.configure_mock(**attrs)
    return fake_client


def mock_args(arg_dict):
    config_mock = mock.Mock()
    attrs = {'__dict__': arg_dict}
    config_mock.configure_mock(**attrs)
    return config_mock
