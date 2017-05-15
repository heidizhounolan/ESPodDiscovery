import yaml
import pod_discovery_pb2
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
PD_ENV = dir_path+"/datastore/dev"
PD_CONFIG = "hosts.yaml"

def read_pod_discovery_database():
    """
    Serve POD list and information from environment specific yaml files
    :return:
    The full contents of the yaml files as a sequence of
      pod_discovery_pb2.Pod.
    """
    pod_list = []
    with open(PD_ENV + "/" + PD_CONFIG, 'r') as pod_list_db_file:
        try:
            data = yaml.load(pod_list_db_file)
            for host in data['hosts']:
                vanity_url, cluster, group = None, None, None
                if 'addr' in data['hosts'][host].keys():
                    vanity_url = data['hosts'][host]['addr']
                if 'groups' in data['hosts'][host].keys():
                    groups = ",".join(data['hosts'][host]['groups'])
                if 'cluster' in data['hosts'][host].keys():
                    cluster = data['hosts'][host]['cluster']

                pod = pod_discovery_pb2.Pod(
                    pod_name = host,
                    vanity_url = vanity_url,
                    cluster = cluster,
                    group = groups
                )
                pod_list.append(pod)
            return pod_list
        except yaml.YAMLError as exc:
            print(exc)
