from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import resource, paginate
from app import Cargo


@app.route("/cargo/all", methods=["GET"])
@jwt_required
@resource("cargo-all")
def cargoAll():

    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get("rows_per_page", app.config["ROWS_PER_PAGE"], type=int)

    query = Cargo.query


    cargos, output = paginate(query, page, rows_per_page)

    for cargo in cargos:
        data = {}
        data["id"] = cargo.id
        data["nome"] = cargo.nome

        output["itens"].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#


@app.route("/cargo/view/<int:cargo_id>", methods=["GET"])
@jwt_required
@resource("cargo-view")
def cargoView(cargo_id: int):
    cargo = Cargo.query.get(cargo_id)

    if not cargo:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(cargo_id), "error": True}
        )

    data = {"error": False}
    data["id"] = cargo.id
    data["nome"] = cargo.nome

    data["cargo_id"] = cargo.cargo_id

    return jsonify(data)
