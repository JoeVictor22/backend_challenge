import re
import datetime
from app import Messages
from app import fieldsFormatter

class ModelValidator():

    def __init__(self, formData):
        self.formData = formData
        self.fields = []
        self.inConstraints = {}
        self.lengthConstraints = {}

    # ------------------------------	--------------------------------------------------------------------#

    def addInConstraint(self, fieldName, values):
        self.inConstraints[fieldName] = values

    # --------------------------------------------------------------------------------------------------#

    def addLengthConstraint(self, fieldName, minLength, maxLength):
        self.lengthConstraints[fieldName] = {"min": minLength, "max": maxLength}

    # --------------------------------------------------------------------------------------------------#

    def addField(self, fieldName, fieldLabel, fieldType, required=False):
        fld = {
            "type": fieldType,
            "name": fieldName,
            "label": fieldLabel,
            "required": required
        }

        self.fields.append(fld)

    # --------------------------------------------------------------------------------------------------#

    def validate(self):

        errors = {
            "fields": {},
            "form": [],
            "has": False
        }

        for field in self.fields:
            if not field['name'] in self.formData or field['name'] == '' or field['name'] == ' ':
                self.formData.update({
                    field['name']: None
                })

            if not field["name"] in errors["fields"]:

                if field["required"]:
                    if not self.hasValue(field["name"]):
                        errors["fields"][field["name"]] = {
                            "message": Messages.FORM_REQUIRED_ERROR
                        }
                        errors["has"] = True
                        continue
                elif self.formData[field["name"]] is None:
                    continue

                if field['name'] in self.lengthConstraints and self.formData[field['name']] is not None:
                    lengthField = len(self.formData[field['name']])
                    minConstr = self.lengthConstraints[field['name']]['min']
                    maxConstr = self.lengthConstraints[field['name']]['max']

                    if lengthField < minConstr or lengthField > maxConstr:
                        errors['fields'][field['name']] = {
                            "message": Messages.FORM_LENGTH_ERROR.format(field['label'], minConstr, maxConstr)
                        }
                        errors['has'] = True

                if field['name'] in self.inConstraints:

                    if not self.formData[field['name']] in self.inConstraints:
                        strValues = "("

                        for key in self.inConstraints[field['name']]:
                            strValues += "{} - {}, ".format(key, self.inConstraints[field['name']][key])

                        strValues = strValues[:-2] + ")"
                        errors['fields'][field['name']] = {
                            "message": Messages.FORM_IN_ERROR.format(field['label'], strValues)
                        }
                        errors['has'] = True

                if field['type'] == 'email':

                    if not self.emailValidate(self.formData[field['name']]):
                        errors['fields'][field['name']] = {
                            "message": Messages.FORM_FIELD_ERROR
                        }
                        errors['has'] = True

                if field['type'] == 'cpf':

                    if not self.cpfValidate(self.formData[field['name']]):
                        errors['fields'][field['name']] = {
                            "message": Messages.FORM_FIELD_ERROR
                        }
                        errors['has'] = True

                if field['type'] == 'integer':

                    if not self.integerValidate(self.formData[field['name']]):
                        errors['fields'][field['name']] = {
                            "message": Messages.FORM_FIELD_ERROR
                        }
                        errors['has'] = True

                if field['type'] == 'boolean':

                    valor = self.formData[field['name']]

                    if valor == "Sim" or valor == "true" or valor == "True":
                        self.formData[field['name']] = True
                    elif valor == "Não" or valor == "false" or valor == "False":
                        self.formData[field['name']] = False

                    if not self.booleanValidate(self.formData[field['name']]):
                        errors['fields'][field['name']] = {
                            "message": Messages.FORM_FIELD_ERROR
                        }
                        errors['has'] = True


        return errors

    # --------------------------------------------------------------------------------------------------#

    def hasValue(self, fieldName):
        return (
                fieldName in self.formData
                and self.formData[fieldName] is not None
                and self.formData[fieldName] != ""
                and self.formData[fieldName] != " ")

    # --------------------------------------------------------------------------------------------------#

    def emailValidate(self, email):
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) != None:
            return True
        return False

    # --------------------------------------------------------------------------------------------------#

    def booleanValidate(self, boolean):

        return boolean == True or boolean == False


    # --------------------------------------------------------------------------------------------------#

    def cpfValidate(self, cpf):
        cpf_invalidos = [11 * str(i) for i in range(10)]

        if cpf in cpf_invalidos:
            return False

        if not cpf.isdigit():
            cpf = cpf.replace(".", "")
            cpf = cpf.replace("-", "")

        if len(cpf) < 11:
            return False

        if len(cpf) > 11:
            return False

        selfcpf = [int(x) for x in cpf]
        cpf = selfcpf[:9]

        while len(cpf) < 11:
            r = sum([(len(cpf) + 1 - i) * v for i, v in [(x, cpf[x]) for x in range(len(cpf))]]) % 11

            if r > 1:
                f = 11 - r
            else:
                f = 0

            cpf.append(f)

        return bool(cpf == selfcpf)


    # --------------------------------------------------------------------------------------------------#

    def integerValidate(self, integer):
        try:
            integer = int(integer)
            return True
        except:
            return False

    # --------------------------------------------------------------------------------------------------#
