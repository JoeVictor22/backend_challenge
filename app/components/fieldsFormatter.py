class CpfFormatter:
    def clean(self, cpf):

        if not cpf.isdigit():
            cpf = cpf.replace(".", "")
            cpf = cpf.replace("-", "")

        return cpf

    def format(self, cpf):

        if cpf == "":
            return ""

        return "%s.%s.%s-%s" % (cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])

class CepFormatter:

    def clean(self, cep):

        if not cep.isdigit():
            cep = cep.replace("-", "")

        return cep

    def format(self, cep):

        if cep == "":
            return ""

        return "%s-%s" % (cep[0:5], cep[5:8])

class PhoneFormatter:

    def clean(self, phone):

        if not phone.isdigit():
            phone = phone.replace("-", "")
            phone = phone.replace("(", "")
            phone = phone.replace(")", "")
            phone = phone.replace(" ", "")

        return phone

    def format(self, phone):

        if phone == "":
            return ""

        return "(%s) %s-%s" % (phone[0:2], phone[2:6], phone[6:11])


class PisFormatter:

    def clean(self, pis):

        if not pis.isdigit():
            pis = pis.replace("-", "")
            pis = pis.replace(".", "")
        return pis

    def format(self, pis):

        if pis == "":
            return ""

        return "%s.%s.%s-%s" % (pis[0:3], pis[3:8], pis[8:10], pis[10:11])


