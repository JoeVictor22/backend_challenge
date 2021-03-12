from app import ModelValidator, Messages
from app import Usuario


class UsuarioValidator(ModelValidator):
    def __init__(self, formData):
        super().__init__(formData)
        self.addFields()
        self.addConstraints()

    # --------------------------------------------------------------------------------------------------#

    def addFields(self):
        super().addField("nome", "Nome", "text", required=True)
        super().addField("email", "Email", "email", required=True)
        super().addField("cargo_id", "Cargo", "integer", required=True)
        super().addField("senha", "Senha", "senha", required=True)

    # --------------------------------------------------------------------------------------------------#

    def addConstraints(self):
        super().addLengthConstraint("nome", 2, 255)
        super().addLengthConstraint("email", 5, 255)
        super().addLengthConstraint("password", 6, 255)

    # --------------------------------------------------------------------------------------------------#

    def validateEmail(self):
        errors = {"fields": {}, "form": [], "has": False}

        if super().hasValue("email"):
            user = Usuario.query.filter(Usuario.email == self.formData["email"]).first()
            if user != None:
                errors["form"].append({"message": Messages.FORM_USER_ALREADY_EXISTS})
                errors["has"] = True

        return errors

