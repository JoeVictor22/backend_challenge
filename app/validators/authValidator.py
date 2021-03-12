from app import ModelValidator, Messages, fieldsFormatter
from app import Usuario, Pessoa, db
from sqlalchemy import or_
from pprint import pprint
from werkzeug.security import check_password_hash


class AuthValidator(ModelValidator):
    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()

    # --------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("email", "Email", "text", required=True)
        super().addField("senha", "Senha", "text", required=True)

    # --------------------------------------------------------------------------------------------------#

    def validate(self):
        errors = super().validate()

        if super().hasValue("email") and super().hasValue("senha"):

            cpf_pis = fieldsFormatter.CpfFormatter().clean(self.formData["email"])

            user = db.session.query(Usuario).join(Pessoa, Pessoa.id == Usuario.pessoa_id, isouter=True).filter(
                or_(
                    Usuario.email == self.formData["email"],
                    Pessoa.cpf == cpf_pis,
                    Pessoa.pis == cpf_pis
                    )
            ).first()


            if not user:
                errors["form"].append({"message": Messages.AUTH_USER_NOT_FOUND})
                errors["has"] = True
            elif not check_password_hash(user.senha, self.formData["senha"]):
                errors["form"].append({"message": Messages.AUTH_USER_PASS_ERROR})
                errors["has"] = True

            return errors
