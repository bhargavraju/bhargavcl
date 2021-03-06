from db.mongo_conn import MongoConnection
from models.machine import Machine, load_machine
from fields import M_ID, CL_ID, M_NAME


def get_machine_record(machine_id):
    machine_rec = MongoConnection().get_machine_collection().find_one(
        {M_ID: machine_id}
    )
    if machine_rec is not None:
        machine_rec.pop('_id')
    return machine_rec


def get_machine_record_by_name(cluster_id, name):
    machine_rec = MongoConnection().get_machine_collection().find_one(
        {CL_ID: cluster_id, M_NAME: name}
    )
    if machine_rec is not None:
        machine_rec.pop('_id')
    return machine_rec


def get_machines_in_cluster(cluster_id):
    machine_recs = MongoConnection().get_machine_collection().find(
        {CL_ID: cluster_id}
    )
    result = []
    for machine_rec in machine_recs:
        machine_rec.pop('_id')
        result.append(machine_rec)
    return result


def machine_with_name_in_cluster_exists(cluster_id, name):
    rec = get_machine_record_by_name(cluster_id, name)
    if rec is not None:
        return True
    else:
        return False


def create_machine(cluster_id, name, ip, instance_type, tags):
    new_machine = Machine(cluster_id, name, ip, instance_type, tags)
    machine_rec = new_machine.json()
    MongoConnection().get_machine_collection().insert_one(machine_rec)
    return new_machine.machine_id


def delete_machine(machine_id):
    MongoConnection().get_machine_collection().remove(
        {M_ID: machine_id}
    )


def delete_machines_in_cluster(cluster_id):
    MongoConnection().get_machine_collection().remove(
        {CL_ID: cluster_id}
    )


def get_machines_by_tags(cluster_id, tags):
    machine_recs = get_machines_in_cluster(cluster_id)
    match_machines = []
    for machine_rec in machine_recs:
        machine = load_machine(machine_rec)
        match = all(tag in machine.tags for tag in tags)
        if match:
            match_machines.append(machine)
    return match_machines


def get_machines_by_state(cluster_id, state):
    machine_recs = get_machines_in_cluster(cluster_id)
    result = []
    for machine_rec in machine_recs:
        machine = load_machine(machine_rec)
        if machine.state == state:
            result.append(machine)
    return result


def return_machines_by_state(cluster_id, state):
    machines = get_machines_by_state(cluster_id, state)
    return [machine.json() for machine in machines]


def modify_status(machine_id, state, machine_obj=None):
    if machine_obj is None:
        machine_rec = get_machine_record(machine_id)
        machine = load_machine(machine_rec)
    else:
        machine = machine_obj
    machine.state = state
    MongoConnection().get_machine_collection().replace_one({M_ID: machine_id}, machine.json())


def add_machine_tag(machine_id, tag):
    machine_rec = get_machine_record(machine_id)
    machine = load_machine(machine_rec)
    if tag not in machine.tags:
        machine.tags.append(tag)
    MongoConnection().get_machine_collection().replace_one({M_ID: machine_id}, machine.json())


def remove_machine_tags(machine_id, tag):
    machine_rec = get_machine_record(machine_id)
    machine = load_machine(machine_rec)
    machine.tags = [mtag for mtag in machine.tags if mtag != tag]
    MongoConnection().get_machine_collection().replace_one({M_ID: machine_id}, machine.json())


# def add_machine(cluster_id, machine_rec):
#     cluster_record = get_cluster_record(cluster_id)
#     cluster = load_cluster(cluster_record)
#     machine = load_machine(machine_rec)
#     cluster.machines.append(machine.machine_id)
#     MongoConnection().get_cluster_collection().replace_one({CL_ID: cluster_id}, cluster.json())


# def remove_machine(cluster_id, machine_id):
#     cluster_record = get_cluster_record(cluster_id)
#     cluster = load_cluster(cluster_record)
#     cluster.machines = [machine for machine in cluster.machines if machine != machine_id]
#     MongoConnection().get_cluster_collection().replace_one({CL_ID: cluster_id}, cluster.json())


def change_machines_status(cluster_id, state):
    machine_recs = get_machines_in_cluster(cluster_id)
    for machine_rec in machine_recs:
        machine = load_machine(machine_rec)
        modify_status(machine.machine_id, state, machine)


def change_machine_status_by_tags(cluster_id, tags, state):
    machines = get_machines_by_tags(cluster_id, tags)
    for machine in machines:
        modify_status(machine.machine_id, state, machine)

# def get_cluster_machines(cluster_id):
#     cluster_record = get_cluster_record(cluster_id)
#     cluster = load_cluster(cluster_record)
#     return cluster.machines
