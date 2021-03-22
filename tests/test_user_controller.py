import json

from pprint import pprint

def test_get_usuarios(app, db, login):

    with app.app_context():
        client = app.test_client()

        url = "/usuario/all"
        response = client.get(url, headers=login)

        output = json.loads(response.get_data())
        print(output)

        assert not output["error"]
        assert response.status_code == 200


def test_view_usuario(app, db, login):

    with app.app_context():
        client = app.test_client()
        url = "/usuario/view/2"
        response = client.get(url, headers=login)

        output = json.loads(response.get_data())
        print(output)
        assert not output["error"]
        assert response.status_code == 200


'''
def test_delete_usuario(app, headers):
    from flask_jwt_extended import create_access_token

    with app.app_context():

        client = app.test_client()
        access_token = create_access_token(1)
        headers = {"Authorization": "Bearer {}".format(access_token)}

        url = "/usuario/delete/2"

        response = client.delete(url, headers=headers)

        output = json.loads(response.get_data())

        assert not outpu.get(["error")
        assert response.status_code == 200

        url = "/usuario/view/2"

        response = client.get(url, headers=headers)
        output = json.loads(response.get_data())
        print(output)

        assert not outpu.get(["error")
        assert response.status_code == 200
'''


def test_post_usuario(app, db, login):

    with app.app_context():
        client = app.test_client()

        url = "/usuario/add"

        data = {"email": "teste@gmail.com", "senha": "123456", "cargo_id": 2}
        response = client.post(url, data=json.dumps(data), headers=login)

        output = json.loads(response.get_data())
        print(output)
        assert not output["error"]
        assert not output["message"] == "Ocorreram erros no preenchimento do formulário."
        assert response.status_code == 200