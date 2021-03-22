import pytest
from app import app as _app, db as _db, Usuario
import json

@pytest.fixture
def app():
    return _app

@pytest.fixture
def db(app):
    '''
    with app.app_context():
        _db.drop_all()
        _db.create_all()
        yield _db
        _db.drop_all()
        _db.session.commit()
    '''
@pytest.fixture
def login(app):
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

        return header