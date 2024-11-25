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
        Get a list of nodes that are in the 'Ready' state and do not have a 'NetworkUnavailable' status condition as 'True'.
        """
        nodes = self.get_nodes()
        ready_nodes = []
        for node in nodes:
            status_conditions = {cond.type: cond.status for cond in node.status.conditions}
            if status_conditions.get("Ready") == "True" and status_conditions.get("NetworkUnavailable") != "True":
                ready_nodes.append(node)
        
        return ready_nodes
