from flask import Flask, request
from db.cluster_data import create_cluster, get_cluster_by_name, delete_cluster, get_cluster_record
from db.machine_data import create_machine, delete_machine, get_machine_record, modify_status, \
     change_machines_status, delete_machines_in_cluster, get_machines_in_cluster, change_machine_status_by_tags
from fields import M_ST_TERMINATED, M_ST_RUNNING
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, Welcome to the application!"


@app.route('/cluster/create', methods=['POST'])
def create_new_cluster():
    """
    Creates a new cluster with the given name and region

    Request params : name, region
    :return: Record of the created cluster
    """
    cluster_name = request.form['name']
    region = request.form['region']
    if get_cluster_by_name(cluster_name) is not None:
        return "Cluster name already exists, please choose a new name", 409
    else:
        return create_cluster(cluster_name, region), 201


@app.route('/cluster/delete', methods=['DELETE'])
def delete_existing_cluster():
    """
    Deletes a cluster by it's id

    Request params: cluster_id
    :return:
    """
    cluster_id = request.args['cluster_id']
    if get_cluster_record(cluster_id) is None:
        return "Cluster with specified id doesn't exist", 400
    else:
        delete_cluster(cluster_id)
        delete_machines_in_cluster(cluster_id)
        return "Cluster deleted", 200


@app.route('/cluster/add_machine', methods=['PUT'])
def add_machine_to_cluster():
    """
    Adds machines to an existing cluster

    Request params: cluster_id, machine_id
    :return:
    """
    cluster_id = request.form['cluster_id']
    name = request.form['name']
    ip = request.form['ip']
    instance_type = request.form['instance_type']
    tags = request.form.get('tags', None)
    if get_cluster_record(cluster_id) is None:
        return "Cluster with specified id doesn't exist", 400
    else:
        return create_machine(cluster_id, name, ip, instance_type, tags), 200


@app.route('/cluster/remove_machine', methods=['DELETE'])
def remove_machine_from_cluster():
    """
    Deletes
    :return:
    """
    machine_id = request.args['machine_id']
    if get_machine_record(machine_id) is None:
        return "Machine with specified id doesn't exist", 400
    else:
        delete_machine(machine_id)
        return "Machine removed successfully", 200


@app.route('/cluster/status/modify', methods=['PUT'])
def modify_cluster_machines_state():
    cluster_id = request.form['cluster_id']
    target_state = request.form['state']
    if get_cluster_record(cluster_id) is None:
        return "Cluster with specified id doesn't exist", 400
    elif target_state not in (M_ST_RUNNING, M_ST_TERMINATED):
        return "Target state provided is not a valid one", 400
    else:
        change_machines_status(cluster_id, target_state)
        return "State of machines in the cluster changed successfully", 200


@app.route('/cluster/machine/list', methods=['GET'])
def get_cluster_machine_list():
    cluster_id = request.args['cluster_id']
    if get_cluster_record(cluster_id) is None:
        return "Cluster with specified id doesn't exist", 400
    else:
        return get_machines_in_cluster(cluster_id), 200


@app.route('/machine/status', methods=['PUT'])
def modify_machine_state():
    machine_id = request.form['machine_id']
    state = request.form['state']
    if get_machine_record(machine_id) is None:
        return "Machine with specified id doesn't exist", 400
    elif state not in (M_ST_TERMINATED, M_ST_RUNNING):
        return "Target state is not a valid state", 400
    else:
        modify_status(machine_id, state)
        return "Machine state modified"


@app.route('/cluster/status/modify/tags', methods=['PUT'])
def modify_status_by_tags():
    cluster_id = request.form['cluster_id']
    tags = request.form['tags']
    state = request.form['sate']
    if get_cluster_record(cluster_id) is None:
        return "Cluster with specified id doesn't exist", 400
    elif state not in (M_ST_TERMINATED, M_ST_RUNNING):
        return "Target state is not a valid state", 400
    else:
        change_machine_status_by_tags(cluster_id, tags, state)
        return "State modified for all machines with specified tags", 200
