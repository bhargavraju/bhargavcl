import uuid
from fields import CL_ID, CL_NAME, CL_REGION


def load_cluster(cluster_doc):
    cluster = Cluster(cluster_doc[CL_NAME], cluster_doc[CL_REGION], cluster_doc[CL_ID])
    return cluster


class Cluster:
    def __init__(self, name, region, cluster_id=None):
        self.name = name
        self.region = region
        self.cluster_id = uuid.uuid4().hex if cluster_id is None else cluster_id

    def json(self):
        return {
            CL_ID: self.cluster_id,
            CL_NAME: self.name,
            CL_REGION: self.region
        }
