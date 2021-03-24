import json

from tests.scenarios import SCENARIO_USER

from pprint import pprint

def test_get_perfis(app, admin_login):
    with app.app_context():
        client = app.test_client()

        url = "/perfil/all"
        response = client.get(url, headers=admin_login)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200

def test_post_perfil(app, admin_login):
    with app.app_context():
        client = app.test_client()

        url = "/usuario/cadastro"
        response = client.post(url, data=json.dumps(SCENARIO_USER), headers=admin_login)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200

def test_view_perfil(app, admin_login):
    with app.app_context():
        client = app.test_client()

        url = "/usuario/all?email=" + SCENARIO_USER["email"]
        response = client.get(url, headers=admin_login)
        output = json.loads(response.get_data())
        assert response.status_code == 200
        assert not output["error"]
        assert output["itens"][0]

        id = output["itens"][0]["perfil_id"]

        url = "/perfil/view/" + str(id)
        response = client.get(url, headers=admin_login)
        output = json.loads(response.get_data())
        print(output)
        assert not output["error"]
        assert response.status_code == 200

def test_delete_perfil(app, created_login, admin_login):


    with app.app_context():

        client = app.test_client()

        id = created_login["id"]

        url = "/usuario/delete/" + str(id)
        response = client.delete(url, headers=created_login)
        output = json.loads(response.get_data())
        assert response.status_code == 200
        assert not output["error"]

        url = "/perfil/view/" + str(id)
        response = client.get(url, headers=admin_login)
        output = json.loads(response.get_data())
        assert output["error"]
        assert response.status_code == 200


