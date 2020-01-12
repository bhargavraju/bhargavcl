from db.mongo_conn import MongoConnection
from models.cluster import Cluster
from fields import CL_ID, CL_NAME


def get_cluster_record(cluster_id):
    cluster_rec = MongoConnection().get_cluster_collection().find_one(
        {CL_ID: cluster_id}
    )
    cluster_rec.pop('_id')
    return cluster_rec


def get_cluster_by_name(cluster_name):
    cluster_rec = MongoConnection().get_cluster_collection().find_one(
        {CL_NAME: cluster_name}
    )
    if cluster_rec is not None:
        cluster_rec.pop('_id')
    return cluster_rec


def get_all_clusters():
    cluster_recs = MongoConnection().get_cluster_collection().find({})
    result = []
    for cluster_rec in cluster_recs:
        cluster_rec.pop('_id')
        result.append(cluster_rec)
    return result


def create_cluster(name, region):
    new_cluster = Cluster(name, region)
    cluster_record = new_cluster.json()
    MongoConnection().get_cluster_collection().insert_one(cluster_record)
    return new_cluster.cluster_id


def delete_cluster(cluster_id):
    MongoConnection().get_cluster_collection().remove(
        {CL_ID: cluster_id}
    )


