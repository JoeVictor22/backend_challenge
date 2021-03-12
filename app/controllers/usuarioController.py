from app import app, db, Messages
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exc
from werkzeug.security import generate_password_hash
from . import resource, paginate
from app import Usuario
from app import UsuarioValidator
from app import fieldsFormatter


@app.route("/usuario/all", methods=["GET"])
@jwt_required
@resource("usuario-all")
def usuarioAll():

    page = request.args.get("page", 1, type=int)
    rows_per_page = request.args.get("rows_per_page", app.config["ROWS_PER_PAGE"], type=int)
    email_filter = request.args.get("email_filter", None)

    query = Usuario.query

    if email_filter != None:
        query = query.filter(Usuario.email.ilike("%%{}%%".format(email_filter)))

    usuarios, output = paginate(query, page, rows_per_page)

    for usuario in usuarios:
        data = {}
        data["id"] = usuario.id
        data["email"] = usuario.email
        data["pessoa_id"] = usuario.pessoa_id

        data["cargo_id"] = usuario.cargo_id

        output["itens"].append(data)

    return jsonify(output)


# --------------------------------------------------------------------------------------------------#


@app.route("/usuario/view/<usuario_id>", methods=["GET"])
@jwt_required
@resource("usuario-view")
def usuarioView(usuario_id):
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(usuario_id), "error": True}
        )

    data = {"error": False}
    data["id"] = usuario.id
    data["email"] = usuario.email
    data["pessoa_id"] = usuario.pessoa_id

    data["cargo_id"] = usuario.cargo_id

    return jsonify(data)

# --------------------------------------------------------------------------------------------------#

@app.route("/usuario/add", methods=["POST"])
@jwt_required
@resource("usuario-add")
def usuarioAdd():
    data = request.get_json()
    validator = UsuarioValidator(data)
    validator.addPasswordField()

    errors = validator.validate()

    if errors["has"]:
        return (
            jsonify(
                {
                    "message": Messages.FORM_VALIDATION_ERROR,
                    "error": errors["has"],
                    "errors": errors,
                }
            ),
            200,
        )

    errors = validator.validateUsername()

    if errors["has"]:
        return (
            jsonify(
                {
                    "message": Messages.FORM_VALIDATION_ERROR,
                    "error": errors["has"],
                    "errors": errors,
                }
            ),
            200,
        )

    hashed_pass = generate_password_hash(data["senha"], method="sha256")
    usuario = Usuario(
        email=data["email"],
        senha=hashed_pass,
        pessoa_id=data["pessoa_id"],
        cargo_id=data["cargo_id"],
    )

    db.session.add(usuario)

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_CREATED.format("Usuário"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Messages.REGISTER_CREATE_INTEGRITY_ERROR, "error": True}
        )


# --------------------------------------------------------------------------------------------------#


@app.route("/usuario/edit/<usuario_id>", methods=["PUT"])
@jwt_required
@resource("usuario-edit")
def usuarioEdit(usuario_id):
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(usuario_id), "error": True}
        )

    data = request.get_json()
    validator = UsuarioValidator(data)
    errors = validator.validate()

    if errors["has"]:
        return (
            jsonify(
                {
                    "message": Messages.FORM_VALIDATION_ERROR,
                    "error": errors["has"],
                    "errors": errors,
                }
            ),
            200,
        )

    usuario.email = data["email"]
    usuario.pessoa_id = data["pessoa_id"]
    usuario.cargo_id = data["cargo_id"]

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_UPDATED.format("Usuário"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {"message": Messages.REGISTER_CHANGE_INTEGRITY_ERROR, "error": True}
        )


# --------------------------------------------------------------------------------------------------#


@app.route("/usuario/delete/<usuario_id>", methods=["DELETE"])
@jwt_required
@resource("usuario-delete")
def usuarioDelete(usuario_id):
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify(
            {"message": Messages.REGISTER_NOT_FOUND.format(usuario_id), "error": True}
        )

    current_user = get_jwt_identity()
    usuario_logado = Usuario.query.get(current_user)
    
    # VALIDATE DELETE
    if usuario.id == usuario_logado.id:
        return jsonify(
            {"message": Messages.USER_INVALID_DELETE, "error": True})
    if usuario_logado.cargo_id != 1:
        return jsonify(
            {"message": Messages.USER_INVALID_DELETE, "error": True})
    if usuario.id == 1:
        return jsonify(
            {"message": Messages.USER_INVALID_DELETE, "error": True})

    db.session.delete(usuario)

    try:
        db.session.commit()
        return jsonify(
            {
                "message": Messages.REGISTER_SUCCESS_DELETED.format("Usuário"),
                "error": False,
            }
        )
    except exc.IntegrityError:
        return jsonify(
            {"message": Messages.REGISTER_DELETE_INTEGRITY_ERROR, "error": True}
        )
