import unittest
from unittest.mock import patch, MagicMock
from kubernetes.client.models import V1Node, V1NodeStatus, V1NodeCondition
from clusterloader2.kubernetes_client import KubernetesClient

class TestKubernetesClient(unittest.TestCase):

    def setUp(self):
        self.client = KubernetesClient()
        return super().setUp()

    @patch('clusterloader2.kubernetes_client.KubernetesClient.get_nodes')
    def test_get_ready_nodes_with_network_unavailable(self, mock_get_nodes):
        # Mock nodes
        node_ready_network_available = V1Node(status=V1NodeStatus(conditions=[
            V1NodeCondition(type="Ready", status="True"),
            V1NodeCondition(type="NetworkUnavailable", status="False")
        ]))
        node_ready_network_unavailable = V1Node(status=V1NodeStatus(conditions=[
            V1NodeCondition(type="Ready", status="True"),
            V1NodeCondition(type="NetworkUnavailable", status="True")
        ]))
        node_not_ready = V1Node(status=V1NodeStatus(conditions=[V1NodeCondition(type="Ready", status="False")]))
        mock_get_nodes.return_value = [node_ready_network_available, node_ready_network_unavailable, node_not_ready]

        ready_nodes = self.client.get_ready_nodes()
        
        self.maxDiff = None
        self.assertCountEqual(ready_nodes, [node_ready_network_available])

if __name__ == '__main__':
    unittest.main()