import uuid
from fields import M_ID, M_NAME, M_IP, M_INST_TYPE, M_TAGS, M_ST_TERMINATED, M_STATE, CL_ID


def load_machine(machine_doc):
    machine = Machine(machine_doc[CL_ID], machine_doc[M_NAME], machine_doc[M_IP], machine_doc[M_INST_TYPE],
                      machine_doc[M_TAGS], machine_doc[M_ID], machine_doc[M_STATE])
    return machine


class Machine:
    def __init__(self, cluster_id, name, ip, instance_type, tags, machine_id=None, state=None):
        self.cluster_id = cluster_id
        self.name = name
        self.ip = ip
        self.instance_type = instance_type
        self.tags = [] if tags is None else tags
        self.machine_id = uuid.uuid4().hex if machine_id is None else machine_id
        self.state = M_ST_TERMINATED if state is None else state

    def json(self):
        return {
            CL_ID: self.cluster_id,
            M_ID: self.machine_id,
            M_NAME: self.name,
            M_IP: self.ip,
            M_TAGS: self.tags,
            M_INST_TYPE: self.instance_type,
            M_STATE: self.state
        }
