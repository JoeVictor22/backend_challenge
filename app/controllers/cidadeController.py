from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import resource, paginate
from app import Cidade


@app.route("/cidade/all", methods=["GET"])
#@jwt_required
#@resource("cidade-all")
def cidadeAll():

    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get("rows_per_page", app.config["ROWS_PER_PAGE"], type=int)
    nome_filter = request.args.get("nome", None)
    query = Cidade.query

    if nome_filter != None:
        query = query.filter(Cidade.nome.ilike("%%{}%%".format(nome_filter)))

    cidades, output = paginate(query, page, rows_per_page)

    for cidade in cidades:
        data = {}
        data["id"] = cidade.id
        data["nome"] = cidade.nome
        data["estado__id"] = cidade.estado_id

        output["itens"].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#


@app.route("/cidade/view/<cidade_id>", methods=["GET"])
#@jwt_required
#@resource("cidade-view")
def cidadeView(cidade_id):

    cidade = Cidade.query.get(cidade_id)

    if not cidade:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(cidade_id), "error": True}
        )

    data = {"error": False}
    data["id"] = cidade.id
    data["nome"] = cidade.nome
    data["estado__id"] = cidade.estado_id


    return jsonify(data)
