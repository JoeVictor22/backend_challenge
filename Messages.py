REGISTER_SUCCESS_CREATED = "Cadastro de {} criado com sucesso."
REGISTER_SUCCESS_UPDATED = "Cadastro de {} atualizado com sucesso."
REGISTER_SUCCESS_DELETED = "Cadastro de {} excluído com sucesso."
REGISTER_CREATE_INTEGRITY_ERROR = (
    "Não foi possível criar o cadastro. Verifique os dados e tente novamente."
)
REGISTER_CHANGE_INTEGRITY_ERROR = (
    "Não foi possível modificar o cadastro. Verifique os dados e tente novamente."
)
REGISTER_DELETE_INTEGRITY_ERROR = (
    "Não foi possível excluir o cadastro. Verifique os dados e tente novamente."
)
REGISTER_NOT_FOUND = "Cadastro Cod. {} não encontrado no sistema."

FORM_VALIDATION_ERROR = "Ocorreram erros no preenchimento do formulário."
FORM_ADDITIONAL_VALIDATION_ERROR = "Ocorrrem erros no cadastro de {}."
FORM_GENERIC_INVALIDATION_ERROR = "O {} informado é inválido"
FORM_EMAIL_ERROR = FORM_GENERIC_INVALIDATION_ERROR.format("email")
FORM_CPF_ERROR = FORM_GENERIC_INVALIDATION_ERROR.format("CPF")
FORM_BOOLEAN_ERROR = FORM_GENERIC_INVALIDATION_ERROR.format("valor booleano")
FORM_DATE_MONTH_ERROR = FORM_GENERIC_INVALIDATION_ERROR.format("mês")
FORM_DATE_YEAR_ERROR = FORM_GENERIC_INVALIDATION_ERROR.format("ano")
FORM_DATE_ERROR = "A data informada é inválida."
FORM_REQUIRED_ERROR = "Campo não informado."
FORM_LENGTH_ERROR = "O campo {} deve ter no mínimo {} e no máximo {} caracteres."
FORM_IN_ERROR = "O campo {} pode assumir somente um dos valores: {}."
FORM_USER_ALREADY_EXISTS = "O nome de usuário informado já existe no sistema."

AUTH_USER_NOT_FOUND = "O usuário informado não está registrado."
AUTH_USER_PASS_ERROR = "A senha informada não corresponde com a do usuário."
AUTH_USER_DENIED = "O usuário não possui permissão para acessar a URL solicitada."

USER_INVALID_DELETE = "Não é permitido deletar esse usuário."


FORM_FIELD_ERROR = "Campo inválido."
