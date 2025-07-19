import unittest
import boto3
from unittest import mock
from mock import Mock, patch
import os
from pathlib import Path


class TestKey(unittest.TestCase):
    @mock.patch('pathlib.Path.exists')
    @mock.patch('os.open')
    @mock.patch('os.fdopen')
    def test_create_key(self, mock_fdopen, mock_open, mock_exists):
        fake_client = mock.Mock(boto3.client('ec2'))
        key_material = "-----BEGIN RSA PRIVATE KEY-----"
        attrs = {
            'create_key_pair.return_value': {
                'KeyMaterial': key_material
            }

        }
        fake_client.configure_mock(**attrs)
        mock_exists.return_value = False

        key_name = 'spotr'
        path = str(Path(f"~/.ssh/{key_name}.pem").expanduser())
        handle = mock_fdopen.return_value.__enter__.return_value

        from spotr import key
        response = key.find_or_create(fake_client, key_name)
        self.assertEqual(response, path)
        handle.write.assert_called_with(key_material)

    @mock.patch('pathlib.Path.exists')
    def test_find_key(self, mock_exists):
        fake_client = mock.Mock(boto3.client('ec2'))
        key_name = 'spotr'
        path = str(Path(f"~/.ssh/{key_name}.pem").expanduser())
        mock_exists.return_value = True

        from spotr import key
        response = key.find_or_create(fake_client, key_name)
        self.assertEqual(response, path)
