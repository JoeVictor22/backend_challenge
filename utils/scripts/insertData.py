from app import db
from config import BASE_DIR

from sqlalchemy import exc, text

# rodar a partir da raiz
# python3 -m scripts.insertData
def populate():
    def insert(filePath):


        sql_file = open(BASE_DIR + filePath, "r")
        escaped_sql = text(sql_file.read())
        db.session.execute(escaped_sql)

        try:
            db.session.commit()
        except exc.IntegrityError:
            print("Ocorreram errors ao executar o seguinte script: " + filePath)


    insert("/utils/scripts/db/cidade_uf.sql")
    insert("/utils/scripts/db/rules.sql")

    # insert("/utils/scripts/db/test_data.sql")


if __name__ == "__main__":
    populate()
