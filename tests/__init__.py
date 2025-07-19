import random
import sys
import time
import unittest
from unittest import mock


class BaseTestCase(unittest.TestCase):
    """
    A base test case which mocks out the low-level session to prevent
    any actual calls to Botocore.
    """

    def setUp(self):
        self.bc_session_patch = mock.patch('botocore.session.Session')
        self.bc_session_cls = self.bc_session_patch.start()

        loader = self.bc_session_cls.return_value.get_component.return_value
        loader.data_path = ''
        self.loader = loader

        # We also need to patch the global default session.
        # Otherwise it could be a cached real session came from previous
        # "functional" or "integration" tests.
        patch_global_session = mock.patch('boto3.DEFAULT_SESSION')
        patch_global_session.start()
        self.addCleanup(patch_global_session.stop)

    def tearDown(self):
        self.bc_session_patch.stop()
