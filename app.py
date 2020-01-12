from flask import Flask, request
from db import cluster_data, machine_data
from fields import M_ST_TERMINATED, M_ST_RUNNING
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, Welcome to the application!"


@app.route('/cluster/create', methods=['POST'])
def create_new_cluster():
    """
    Creates a new cluster with the given name and region

    Request params : name: str, region: str
    :return: cluster_id
    """
    cluster_name = request.form['name']
    region = request.form['region']
    if cluster_data.get_cluster_by_name(cluster_name) is not None:
        return "Cluster name already exists, please choose a new name", 409
    else:
        cluster_id = cluster_data.create_cluster(cluster_name, region)
        return 'Cluster created with cluster id: ' + cluster_id, 201


@app.route('/cluster/details/id', methods=['GET'])
def get_cluster_details():
    """
    Provides details of a specific cluster

    Request params : cluster_id: str
    :return: Cluster record
    """
    cluster_id = request.args['cluster_id']
    if cluster_data.get_cluster_record(cluster_id) is None:
        return "Cluster with specified id doesn't exist", 400
    else:
        cluster_record = cluster_data.get_cluster_record(cluster_id)
        return cluster_record, 200


@app.route('/cluster/details/all', methods=['GET'])
def get_all_cluster_details():
    """
    Provides details of all clusters

    :return: List of cluster records
    """
    cluster_recs = cluster_data.get_all_clusters()
    return {'clusters': cluster_recs}, 200


@app.route('/cluster/delete', methods=['DELETE'])
def delete_existing_cluster():
    """
    Deletes a cluster by it's id

    Request params: cluster_id: str
    :return:
    """
    cluster_id = request.args['cluster_id']
    if cluster_data.get_cluster_record(cluster_id) is None:
        return "Cluster with specified id doesn't exist", 400
    else:
        cluster_data.delete_cluster(cluster_id)
        machine_data.delete_machines_in_cluster(cluster_id)
        return "Cluster deleted", 200


@app.route('/cluster/add_machine', methods=['POST'])
def add_machine_to_cluster():
    """
    Adds machines to an existing cluster

    Content-type: application/json
    Request params: cluster_id: str, name: str, ip: str, instance_type: str, tags: List[str]
    :return: Machine id
    """
    inputs = request.get_json(force=True)
    cluster_id = inputs['cluster_id']
    name = inputs['name']
    ip = inputs['ip']
    instance_type = inputs['instance_type']
    tags = inputs.get('tags', None)
    if cluster_data.get_cluster_record(cluster_id) is None:
        return "Cluster with specified id doesn't exist", 400
    elif machine_data.machine_with_name_in_cluster_exists(cluster_id, name):
        return "This cluster already has a machine with the provided name", 409
    else:
        machine_id = machine_data.create_machine(cluster_id, name, ip, instance_type, tags)
        return 'Machine created with machine id: ' + machine_id, 201


@app.route('/machine/details/id', methods=['GET'])
def get_machine_details():
    """
    Provides details of a specific cluster

    Request params: machine_id: str
    :return: Cluster record
    """
    machine_id = request.args['machine_id']
    if machine_data.get_machine_record(machine_id) is None:
        return "Machine with specified id doesn't exist", 400
    else:
        machine_record = machine_data.get_machine_record(machine_id)
        return machine_record, 200


@app.route('/cluster/remove_machine', methods=['DELETE'])
def remove_machine_from_cluster():
    """
    Deletes machine from a cluster

    Request params: machine_id: str
    :return:
    """
    machine_id = request.args['machine_id']
    if machine_data.get_machine_record(machine_id) is None:
        return "Machine with specified id doesn't exist", 400
    else:
        machine_data.delete_machine(machine_id)
        return "Machine removed successfully", 200


@app.route('/cluster/status/modify', methods=['PUT'])
def modify_cluster_machines_state():
    """
    Modifies the state of all machines in a cluster

    Request params: cluster_id: str, state: str
    :return:
    """
    cluster_id = request.form['cluster_id']
    target_state = request.form['state']
    if cluster_data.get_cluster_record(cluster_id) is None:
        return "Cluster with specified id doesn't exist", 400
    elif target_state not in (M_ST_RUNNING, M_ST_TERMINATED):
        return "Target state is not a valid one. Please enter one of: " + M_ST_RUNNING + ", " + M_ST_TERMINATED, 400
    else:
        machine_data.change_machines_status(cluster_id, target_state)
        return "State of machines in the cluster changed successfully", 200


@app.route('/cluster/machine/list', methods=['GET'])
def get_cluster_machine_list():
    """
    Lists all machines present in a cluster

    Request params: cluster_id: str
    :return: List of machine records
    """
    cluster_id = request.args['cluster_id']
    if cluster_data.get_cluster_record(cluster_id) is None:
        return "Cluster with specified id doesn't exist", 400
    else:
        return {'machines': machine_data.get_machines_in_cluster(cluster_id)}, 200


@app.route('/cluster/machine/list/status', methods=['GET'])
def get_cluster_machine_list_by_status():
    """
    Lists all machines of a cluster, in a particular state (Running/Terminated)

    Request params: cluster_id: str, state: str
    :return: List of machine records
    """
    cluster_id = request.args['cluster_id']
    state = request.args['state']
    if cluster_data.get_cluster_record(cluster_id) is None:
        return "Cluster with specified id doesn't exist", 400
    elif state not in (M_ST_TERMINATED, M_ST_RUNNING):
        return "Target state is not a valid state. Please enter one of: " + M_ST_RUNNING + ", " + M_ST_TERMINATED, 400
    else:
        return {'machines': machine_data.return_machines_by_state(cluster_id, state)}, 200


@app.route('/machine/status', methods=['PUT'])
def modify_machine_state():
    """
    Modifies the state of a machine

    Request params: machine_id: str, state: str
    :return:
    """
    machine_id = request.form['machine_id']
    state = request.form['state']
    if machine_data.get_machine_record(machine_id) is None:
        return "Machine with specified id doesn't exist", 400
    elif state not in (M_ST_TERMINATED, M_ST_RUNNING):
        return "Target state is not a valid state. Please enter one of: " + M_ST_RUNNING + ", " + M_ST_TERMINATED, 400
    else:
        machine_data.modify_status(machine_id, state)
        return "Machine state modified"


@app.route('/cluster/status/modify/tags', methods=['PUT'])
def modify_status_by_tags():
    """
    Modifies all machines' state in a cluster that contain all provided tags

    Content-type: application/json
    Request params: cluster_id: str, tags: List[str], state: str
    :return:
    """
    inputs = request.get_json(force=True)
    cluster_id = inputs['cluster_id']
    tags = inputs['tags']
    state = inputs['state']
    if cluster_data.get_cluster_record(cluster_id) is None:
        return "Cluster with specified id doesn't exist", 400
    elif state not in (M_ST_TERMINATED, M_ST_RUNNING):
        return "Target state is not a valid state. Please enter one of: " + M_ST_RUNNING + ", " + M_ST_TERMINATED, 400
    else:
        machine_data.change_machine_status_by_tags(cluster_id, tags, state)
        return "State modified for all machines with specified tags", 200


if __name__ == "__main__":
    app.run()
