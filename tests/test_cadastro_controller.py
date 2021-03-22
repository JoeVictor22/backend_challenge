import json

from tests.scenarios import SCENARIO_ADMIN, SCENARIO_USER

from pprint import pprint

def test_get_usuarios(app, db, login):

    with app.app_context():
        client = app.test_client()

        url = "/usuario/all"
        response = client.get(url, headers=login)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200

def test_post_usuario(app, db, login):

    with app.app_context():
        client = app.test_client()

        url = "/usuario/add"
        response = client.post(url, data=json.dumps(SCENARIO_ADMIN), headers=login)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert not output["message"] == "Ocorreram erros no preenchimento do formulário."
        assert response.status_code == 200

def test_view_usuario(app, db, login):

    with app.app_context():
        client = app.test_client()

        url = "/usuario/view/1"
        response = client.get(url, headers=login)
        output = json.loads(response.get_data())
        assert not output["error"]
        assert response.status_code == 200

def test_delete_usuario(app, login):
    with app.app_context():

        client = app.test_client()

        url = "/usuario/all?email=teste@gmail.com"
        response = client.get(url, headers=login)
        output = json.loads(response.get_data())
        assert response.status_code == 200
        assert not output["error"]
        assert output["itens"][0]


        id = output["itens"][0]["id"]
        url = "/usuario/delete/" + str(id)
        response = client.delete(url, headers=login)
        output = json.loads(response.get_data())
        assert response.status_code == 200
        assert not output["error"]

        url = "/usuario/view/" + str(id)
        response = client.get(url, headers=login)
        output = json.loads(response.get_data())
        assert output["error"]
        assert response.status_code == 200


