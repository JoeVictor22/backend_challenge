import json

from tests.scenarios import SCENARIO_USER

from pprint import pprint

def test_get_usuarios(app, admin_login):
    with app.app_context():
        client = app.test_client()

        url = "/usuario/all"
        response = client.get(url, headers=admin_login)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200

def test_post_usuario(app, admin_login):
    with app.app_context():
        client = app.test_client()

        url = "/usuario/add"
        response = client.post(url, data=json.dumps(SCENARIO_USER), headers=admin_login)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200

def test_view_usuario(app, admin_login, created_login):
    with app.app_context():
        client = app.test_client()

        id = created_login["id"]

        url = "/usuario/view/" + str(id)
        response = client.get(url, headers=admin_login)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200


def test_delete_usuario(app, admin_login, created_login):
    with app.app_context():
        client = app.test_client()

        id = created_login["id"]
        url = "/usuario/delete/" + str(id)
        response = client.delete(url, headers=admin_login)
        output = json.loads(response.get_data())
        assert response.status_code == 200
        assert not output["error"]

        url = "/usuario/view/" + str(id)
        response = client.get(url, headers=admin_login)
        output = json.loads(response.get_data())
        assert output["error"]
        assert response.status_code == 200


