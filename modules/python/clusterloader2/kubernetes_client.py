from kubernetes import client, config

class KubernetesClient:
    def __init__(self, kubeconfig=None):
        config.load_kube_config(kubeconfig)
        self.api = client.CoreV1Api()

    def describe_node(self, node_name):
        return self.api.read_node(node_name)

    def get_nodes(self, label_selector=None, field_selector=None):
        return self.api.list_node(label_selector=label_selector, field_selector=field_selector).items
    
    def get_ready_nodes(self):
        """
        Get a list of nodes that are in the 'Ready' state and 'NetworkUnavailable' is 'False'.
        """
        nodes = self.get_nodes()
        return [
            node for node in nodes 
            if any(cond.type == "Ready" and cond.status == "True" for cond in node.status.conditions)
               and any(cond.type == "NetworkUnavailable" and cond.status == "False" for cond in node.status.conditions)
        ]