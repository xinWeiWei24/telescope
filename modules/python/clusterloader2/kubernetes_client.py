from kubernetes import client, config

class KubernetesClient:
    def __init__(self, kubeconfig=None):
        config.load_kube_config(kubeconfig)
        self.api = client.CoreV1Api()

    def describe_node(self, node_name):
        return self.api.read_node(node_name)

    def get_nodes(self, label_selector=None, field_selector=None):
        return self.api.list_node(label_selector=label_selector, field_selector=field_selector).items
    
    def get_ready_nodes(self, check_network_unavailable=False):
        """
        Get a list of nodes that are in the 'Ready' state.

        Args:
            check_network_unavailable (bool): If True, also check that the 'NetworkUnavailable' condition is False.

        Returns:
            list: A list of nodes that are in the 'Ready' state.
        """
        nodes = self.get_nodes()
        if not check_network_unavailable:
            return [node for node in nodes for condition in node.status.conditions if condition.type == "Ready" and condition.status == "True"]
        else:
            return [
                node for node in nodes for condition in node.status.conditions 
                if condition.type == "Ready" and condition.status == "True" and any(cond.type == "NetworkUnavailable" and cond.status == "False" for cond in node.status.conditions)
            ]