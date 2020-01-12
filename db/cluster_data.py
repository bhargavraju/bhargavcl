from db.mongo_conn import MongoConnection
from models.cluster import Cluster
from fields import CL_ID, CL_NAME


def get_cluster_record(cluster_id):
    cluster_rec = MongoConnection().get_cluster_collection().find_one(
        {CL_ID: cluster_id}
    )
    return cluster_rec


def get_cluster_by_name(cluster_name):
    cluster_rec = MongoConnection().get_cluster_collection().find_one(
        {CL_NAME: cluster_name}
    )
    return cluster_rec


def create_cluster(name, region):
    new_cluster = Cluster(name, region)
    cluster_record = new_cluster.json()
    MongoConnection().get_cluster_collection().insert_one(cluster_record)
    return cluster_record


def delete_cluster(cluster_id):
    MongoConnection().get_cluster_collection().remove(
        {CL_ID: cluster_id}
    )


