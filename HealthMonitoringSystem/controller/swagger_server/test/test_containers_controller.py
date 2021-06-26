# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestContainersController(BaseTestCase):
    """ContainersController integration test stubs"""

    def test_get_containers_list(self):
        """Test case for get_containers_list

        Find container list
        """
        response = self.client.open(
            '/v2/monitoring',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_stop_container(self):
        """Test case for stop_container

        Stops a container
        """
        response = self.client.open(
            '/v2/monitoring/{containerID}'.format(containerID='containerID_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
