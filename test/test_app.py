import pytest
from app import app, cluster_data, machine_data
import json


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


def mock_exception(*args):
    raise Exception


def mock_none(*args):
    return None


def mock_empty_dict(*args):
    return {}


def mock_ret_false(*args):
    return False


def mock_ret_true(*args):
    return True


def mock_ret_string(*args):
    return 'abcd1234'


def test_create_cluster_success(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_by_name", mock_none)
    monkeypatch.setattr(cluster_data, "create_cluster", lambda x, y: 'abcd1234')
    resp = client.post('/cluster/create', data={'name': 'test_cluster', 'region': 'India'})
    assert resp.status_code == 201


def test_create_cluster_duplicate(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_by_name", mock_empty_dict)
    monkeypatch.setattr(cluster_data, "create_cluster", lambda x, y: 'abcd1234')
    resp = client.post('/cluster/create', data={'name': 'test_cluster', 'region': 'India'})
    assert resp.status_code == 409


def test_create_cluster_exception(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_by_name", mock_none)
    monkeypatch.setattr(cluster_data, "create_cluster", mock_exception)
    resp = client.post('/cluster/create', data={'name': 'test_cluster', 'region': 'India'})
    assert resp.status_code == 500


def test_cluster_details_id_success(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    resp = client.get('/cluster/details/id?cluster_id=abcd1234')
    assert resp.status_code == 200


def test_cluster_details_id_not_exists(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_none)
    resp = client.get('/cluster/details/id?cluster_id=abcd1234')
    assert resp.status_code == 400


def test_cluster_details_id_exception(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_exception)
    resp = client.get('/cluster/details/id?cluster_id=abcd1234')
    assert resp.status_code == 500


def test_get_all_clusters_success(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_all_clusters", mock_empty_dict)
    resp = client.get('/cluster/details/all')
    assert resp.status_code == 200


def test_get_all_clusters_exception(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_all_clusters", mock_exception)
    resp = client.get('/cluster/details/all')
    assert resp.status_code == 500


def test_delete_cluster_success(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(cluster_data, "delete_cluster", mock_none)
    monkeypatch.setattr(machine_data, "delete_machines_in_cluster", mock_none)
    resp = client.delete('/cluster/delete?cluster_id=abcd1234')
    assert resp.status_code == 200


def test_delete_cluster_doesnt_exist(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_none)
    monkeypatch.setattr(cluster_data, 'delete_cluster', mock_none)
    monkeypatch.setattr(machine_data, 'delete_machines_in_cluster', mock_none)
    resp = client.delete('/cluster/delete?cluster_id=abcd1234')
    assert resp.status_code == 400


def test_delete_cluster_exception(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_exception)
    monkeypatch.setattr(cluster_data, 'delete_cluster', mock_none)
    monkeypatch.setattr(machine_data, 'delete_machines_in_cluster', mock_none)
    resp = client.delete('/cluster/delete?cluster_id=abcd1234')
    assert resp.status_code == 500


def test_add_machine_to_cluster_success(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "machine_with_name_in_cluster_exists", mock_ret_false)
    monkeypatch.setattr(machine_data, "create_machine", mock_ret_string)
    resp = client.post('/cluster/add_machine', data=json.dumps({'cluster_id': 'abcd1234', 'name': 'machine', 'ip': '127.0.0.1',
                                                     'instance_type': 'GPU', 'tags': ['py-server', 'flask']}),
                       content_type='application/json')
    assert resp.status_code == 201


def test_add_machine_to_cluster_cluster_doesnt_exist(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_none)
    monkeypatch.setattr(machine_data, "machine_with_name_in_cluster_exists", mock_ret_false)
    monkeypatch.setattr(machine_data, "create_machine", mock_ret_string)
    resp = client.post('/cluster/add_machine', data=json.dumps({'cluster_id': 'abcd1234', 'name': 'machine', 'ip': '127.0.0.1',
                                                     'instance_type': 'GPU', 'tags': ['py-server', 'flask']}),
                       content_type='application/json')
    assert resp.status_code == 400


def test_add_machine_to_cluster_machine_duplicate(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "machine_with_name_in_cluster_exists", mock_ret_true)
    monkeypatch.setattr(machine_data, "create_machine", mock_ret_string)
    resp = client.post('/cluster/add_machine', data=json.dumps({'cluster_id': 'abcd1234', 'name': 'machine', 'ip': '127.0.0.1',
                                                     'instance_type': 'GPU', 'tags': ['py-server', 'flask']}),
                       content_type='application/json')
    assert resp.status_code == 409


def test_add_machine_to_cluster_exception(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_exception)
    monkeypatch.setattr(machine_data, "machine_with_name_in_cluster_exists", mock_ret_false)
    monkeypatch.setattr(machine_data, "create_machine", mock_ret_string)
    resp = client.post('/cluster/add_machine', data=json.dumps({'cluster_id': 'abcd1234', 'name': 'machine', 'ip': '127.0.0.1',
                                                     'instance_type': 'GPU', 'tags': ['py-server', 'flask']}),
                       content_type='application/json')
    assert resp.status_code == 500


def test_get_machine_details_id_success(client, monkeypatch):
    monkeypatch.setattr(machine_data, "get_machine_record", mock_empty_dict)
    resp = client.get('/machine/details/id?machine_id=machine123')
    assert resp.status_code == 200


def test_get_machine_details_id_doesnt_exist(client, monkeypatch):
    monkeypatch.setattr(machine_data, "get_machine_record", mock_none)
    resp = client.get('/machine/details/id?machine_id=machine123')
    assert resp.status_code == 400


def test_get_machine_details_id_exception(client, monkeypatch):
    monkeypatch.setattr(machine_data, "get_machine_record", mock_exception)
    resp = client.get('/machine/details/id?machine_id=machine123')
    assert resp.status_code == 500


def test_remove_machine_success(client, monkeypatch):
    monkeypatch.setattr(machine_data, "get_machine_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "delete_machine", mock_none)
    resp = client.delete('/cluster/remove_machine?machine_id=machine1234')
    assert resp.status_code == 200


def test_remove_machine_doesnt_exist(client, monkeypatch):
    monkeypatch.setattr(machine_data, "get_machine_record", mock_none)
    monkeypatch.setattr(machine_data, "delete_machine", mock_none)
    resp = client.delete('/cluster/remove_machine?machine_id=machine1234')
    assert resp.status_code == 400


def test_remove_machine_exception(client, monkeypatch):
    monkeypatch.setattr(machine_data, "get_machine_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "delete_machine", mock_exception)
    resp = client.delete('/cluster/remove_machine?machine_id=machine1234')
    assert resp.status_code == 500


def test_modify_cluster_machines_state_success(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "change_machines_status", mock_none)
    resp = client.put('/cluster/status/modify', data={'cluster_id': 'abcd1234', 'state': 'Running'})
    assert resp.status_code == 200


def test_modify_cluster_machines_state_cluster_doesnt_exist(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_none)
    monkeypatch.setattr(machine_data, "change_machines_status", mock_none)
    resp = client.put('/cluster/status/modify', data={'cluster_id': 'abcd1234', 'state': 'Running'})
    assert resp.status_code == 400


def test_modify_cluster_machines_state_wrong_state(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "change_machines_status", mock_none)
    resp = client.put('/cluster/status/modify', data={'cluster_id': 'abcd1234', 'state': 'Rebooting'})
    assert resp.status_code == 400


def test_modify_cluster_machines_state_exception(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "change_machines_status", mock_exception)
    resp = client.put('/cluster/status/modify', data={'cluster_id': 'abcd1234', 'state': 'Running'})
    assert resp.status_code == 500


def test_get_cluster_machine_list_success(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "get_machines_in_cluster", mock_empty_dict)
    resp = client.get('/cluster/machine/list?cluster_id=abcd123')
    assert resp.status_code == 200


def test_get_cluster_machine_list_cluster_doesnt_exist(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_none)
    monkeypatch.setattr(machine_data, "get_machines_in_cluster", mock_empty_dict)
    resp = client.get('/cluster/machine/list?cluster_id=abcd123')
    assert resp.status_code == 400


def test_get_cluster_machine_list_exception(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "get_machines_in_cluster", mock_exception)
    resp = client.get('/cluster/machine/list?cluster_id=abcd123')
    assert resp.status_code == 500


def test_get_cluster_machine_list_by_status_success(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "return_machines_by_state", mock_empty_dict)
    resp = client.get('/cluster/machine/list/status?cluster_id=abcd123&state=Running')
    assert resp.status_code == 200


def test_get_cluster_machine_list_by_status_cluster_doesnt_exist(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_none)
    monkeypatch.setattr(machine_data, "return_machines_by_state", mock_empty_dict)
    resp = client.get('/cluster/machine/list/status?cluster_id=abcd123&state=Running')
    assert resp.status_code == 400


def test_get_cluster_machine_list_by_status_wrong_state(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "return_machines_by_state", mock_empty_dict)
    resp = client.get('/cluster/machine/list/status?cluster_id=abcd123&state=Rebooting')
    assert resp.status_code == 400


def test_get_cluster_machine_list_by_status_exception(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "return_machines_by_state", mock_exception)
    resp = client.get('/cluster/machine/list/status?cluster_id=abcd123&state=Running')
    assert resp.status_code == 500


def test_modify_machine_state_success(client, monkeypatch):
    monkeypatch.setattr(machine_data, "get_machine_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "modify_status", mock_none)
    resp = client.put('/machine/status', data={'machine_id': 'machine123', 'state': 'Running'})
    assert resp.status_code == 200


def test_modify_machine_state_machine_doesnt_exist(client, monkeypatch):
    monkeypatch.setattr(machine_data, "get_machine_record", mock_none)
    monkeypatch.setattr(machine_data, "modify_status", mock_none)
    resp = client.put('/machine/status', data={'machine_id': 'machine123', 'state': 'Running'})
    assert resp.status_code == 400


def test_modify_machine_state_wrong_state(client, monkeypatch):
    monkeypatch.setattr(machine_data, "get_machine_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "modify_status", mock_none)
    resp = client.put('/machine/status', data={'machine_id': 'machine123', 'state': 'Rebooting'})
    assert resp.status_code == 400


def test_modify_machine_state_exception(client, monkeypatch):
    monkeypatch.setattr(machine_data, "get_machine_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "modify_status", mock_exception)
    resp = client.put('/machine/status', data={'machine_id': 'machine123', 'state': 'Running'})
    assert resp.status_code == 500


def test_modify_status_by_tags_success(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "change_machine_status_by_tags", mock_none)
    resp = client.put('/cluster/status/modify/tags', data=json.dumps({'cluster_id': 'abcd1234',
                                                                      'tags': ['py-server', 'django'],
                                                                      'state': 'Terminated'}),
                      content_type='application/json')
    assert resp.status_code == 200


def test_modify_status_by_tags_cluster_doesnt_exist(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_none)
    monkeypatch.setattr(machine_data, "change_machine_status_by_tags", mock_none)
    resp = client.put('/cluster/status/modify/tags', data=json.dumps({'cluster_id': 'abcd1234',
                                                                      'tags': ['py-server', 'django'],
                                                                      'state': 'Terminated'}),
                      content_type='application/json')
    assert resp.status_code == 400


def test_modify_status_by_tags_wrong_state(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "change_machine_status_by_tags", mock_none)
    resp = client.put('/cluster/status/modify/tags', data=json.dumps({'cluster_id': 'abcd1234',
                                                                      'tags': ['py-server', 'django'],
                                                                      'state': 'Stopped'}),
                      content_type='application/json')
    assert resp.status_code == 400


def test_modify_status_by_tags_exception(client, monkeypatch):
    monkeypatch.setattr(cluster_data, "get_cluster_record", mock_empty_dict)
    monkeypatch.setattr(machine_data, "change_machine_status_by_tags", mock_exception)
    resp = client.put('/cluster/status/modify/tags', data=json.dumps({'cluster_id': 'abcd1234',
                                                                      'tags': ['py-server', 'django'],
                                                                      'state': 'Terminated'}),
                      content_type='application/json')
    assert resp.status_code == 500
