import os
from app import db
import sqlparse
from pprint import pprint

# rodar a partir da raiz
# python3 -m scripts.insertData
def populate():
    def insert(filePath, output):

        fd = open(os.path.dirname(__file__) + "/" + filePath, "r")
        sqlFile = fd.read()
        fd.close()

        sqlCommands = sqlFile.split(";")

        for command in sqlCommands:
            try:
                command = sqlparse.format(command, strip_comments=True)
                command = command.replace("\n", "")

                db.session.execute(command)
                output["saved"].append(command)
            except:
                output["skipped"].append(command)
                print("Command skipped: ", command)

    output = {"error": False, "message": "empty", "saved": [], "skipped": []}

    insert("db/cidade_uf.sql", output)

    insert("db/dml_acl.sql", output)

    try:
        db.session.commit()
        output["message"] = "Dados salvos com sucesso"
        print("\nOUTPUT: \n")
        pprint(output["skipped"])
    except:
        db.session.rollback()
        print("rollback feito")
        output["error"] = True
        output["message"] = "Erro na inserção"


if __name__ == "__main__":
    populate()
    print(os.path.dirname(os.path.abspath(__file__)))
    print(os.path.dirname(__file__))