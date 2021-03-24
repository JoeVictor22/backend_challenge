import pytest
from app import app as _app, db as _db, Usuario
import json
from tests.scenarios import SCENARIO_USER

from sqlalchemy import text

from config import BASE_DIR

@pytest.fixture
def app():
    return _app

@pytest.fixture
def db(app):
    with app.app_context():
        _db.drop_all()
        _db.create_all()

        session = db.session()
        sql_file = open(BASE_DIR + "/utils/scripts/db/dml.sql", "r")
        escaped_sql = text(sql_file.read())
        session.execute(escaped_sql)
        session.flush()

        sql_file = open(BASE_DIR + "/utils/scripts/db/tests.sql", "r")
        escaped_sql = text(sql_file.read())
        session.execute(escaped_sql)
        session.commit()

        session.close()
        yield _db
        _db.drop_all()
        _db.session.commit()



@pytest.fixture
def admin_login(app):
    with app.app_context():
        client = app.test_client()

        url = "/auth"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {"email": "joelvictor1746@gmail.com", "senha": "1234"}
        response = client.post(url, data=json.dumps(data), headers=headers)


        res = json.loads(response.get_data())
        header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(res["access_token"])}

        assert response.status_code == 200

        return header

@pytest.fixture
def created_login(app):
    with app.app_context():
        client = app.test_client()

        url = "/auth"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {"email": SCENARIO_USER["email"], "senha": SCENARIO_USER["senha"]}
        response = client.post(url, data=json.dumps(data), headers=headers)

        res = json.loads(response.get_data())
        login_criado = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(res["access_token"])}

        url = "/me"
        response = client.get(url, headers=login_criado)
        output = json.loads(response.get_data())
        print(output)

        assert response.status_code == 200

        login_criado["id"] = output["id"]
        return login_criado