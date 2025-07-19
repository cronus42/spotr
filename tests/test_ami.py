import unittest
from unittest import mock

from spotr.ami import get_by_tag


class TestAmi(unittest.TestCase):
    def test_get_by_tag_success(self):
        """Test successfully retrieving an AMI by tag"""
        client = mock.Mock()
        client.describe_images.return_value = {
            'Images': [
                {'ImageId': 'ami-12345678', 'Name': 'test-image'},
                {'ImageId': 'ami-87654321', 'Name': 'another-image'}
            ]
        }
        
        result = get_by_tag(client, 'my-project')
        
        # Should return the first image ID
        self.assertEqual(result, 'ami-12345678')
        
        # Verify the correct API call was made
        client.describe_images.assert_called_once_with(
            Filters=[{'Name': 'tag:project', 'Values': ['my-project']}]
        )

    def test_get_by_tag_no_images(self):
        """Test error when no images are found with the specified tag"""
        client = mock.Mock()
        client.describe_images.return_value = {'Images': []}
        
        with self.assertRaises(RuntimeError) as cm:
            get_by_tag(client, 'nonexistent-tag')
        
        self.assertEqual(
            str(cm.exception), 
            "No saved images with tag: 'nonexistent-tag'"
        )

    def test_get_by_tag_empty_response(self):
        """Test error handling when API returns empty image list"""
        client = mock.Mock()
        client.describe_images.return_value = {'Images': []}
        
        with self.assertRaises(RuntimeError):
            get_by_tag(client, 'test-tag')
