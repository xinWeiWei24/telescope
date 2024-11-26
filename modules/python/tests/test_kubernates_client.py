import unittest
from unittest.mock import patch, MagicMock
from kubernetes.client.models import (
    V1Node, V1NodeStatus, V1NodeCondition, V1NodeSpec, V1ObjectMeta, V1Taint
)
from clusterloader2.kubernetes_client import KubernetesClient

class TestKubernetesClient(unittest.TestCase):

    def setUp(self):
        self.client = KubernetesClient()
        return super().setUp()

    @patch('clusterloader2.kubernetes_client.KubernetesClient.get_nodes')
    def test_get_ready_nodes_with_network_unavailable(self, mock_get_nodes):
        # Mock nodes
        node_not_ready = V1Node(
            metadata=V1ObjectMeta(name="node_not_ready"),
            status=V1NodeStatus(conditions=[V1NodeCondition(type="Ready", status="False")]), 
            spec=V1NodeSpec(unschedulable=False, taints=[])
        )

        node_ready_network_available = V1Node(
            metadata=V1ObjectMeta(name="node_ready_network_available"),
            status=V1NodeStatus(
                conditions=[
                    V1NodeCondition(type="Ready", status="True"), 
                    V1NodeCondition(type="NetworkUnavailable", status="False")]), 
            spec=V1NodeSpec(unschedulable=False, taints=[]))

        node_ready_network_unavailable = V1Node(
            metadata=V1ObjectMeta(name="node_ready_network_unavailable"),
            status=V1NodeStatus(
                conditions=[
                    V1NodeCondition(type="Ready", status="True"),
                    V1NodeCondition(type="NetworkUnavailable", status="True")]), 
            spec=V1NodeSpec(unschedulable=False, taints=[]))
        
        node_ready_no_network_condition = V1Node(
            metadata=V1ObjectMeta(name="node_ready_no_network_condition"),
            status=V1NodeStatus(conditions=[V1NodeCondition(type="Ready", status="True")]),
            spec=V1NodeSpec(unschedulable=False, taints=None)
        )

        node_ready_unschedulable = V1Node(
            metadata=V1ObjectMeta(name="node_ready_unschedulable"),
            status=V1NodeStatus(conditions=[V1NodeCondition(type="Ready", status="True")]),
            spec=V1NodeSpec(unschedulable=True, taints=[])
        )
        
        node_ready_shutdown_taint = V1Node(
            metadata=V1ObjectMeta(name="node_ready_shutdown_taint"),
            status=V1NodeStatus(conditions=[V1NodeCondition(type="Ready", status="True")]),
            spec=V1NodeSpec(unschedulable=False, 
                            taints=[V1Taint(key="node.cloudprovider.kubernetes.io/shutdown", effect="NoSchedule")])
        )
        
        node_ready_shutdown_taint_no_effect = V1Node(
            metadata=V1ObjectMeta(name="node_ready_shutdown_taint_no_effect"),
            status=V1NodeStatus(conditions=[V1NodeCondition(type="Ready", status="True")]),
            spec=V1NodeSpec(unschedulable=False, 
                            taints=[V1Taint(key="node.cloudprovider.kubernetes.io/shutdown", effect="")])
        )
        
        mock_get_nodes.return_value = [
            node_not_ready,
            node_ready_network_available, 
            node_ready_network_unavailable, 
            node_ready_no_network_condition,
            node_ready_unschedulable,
            node_ready_shutdown_taint,
            node_ready_shutdown_taint_no_effect
        ]

        ready_nodes = self.client.get_ready_nodes()

        self.maxDiff = None
        self.assertCountEqual(ready_nodes, 
            [node_ready_network_available, node_ready_no_network_condition, node_ready_shutdown_taint_no_effect]
        )

if __name__ == '__main__':
    unittest.main()