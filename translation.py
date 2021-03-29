def _(msg_id):
    translations = {
        'Value is not a valid float': 'O valor deve ser um ponto flutuante',
        'ensure this value has at least {limit_value} characters': 'Este campo deve possuir pelo menos {limit_value} caracteres',
        'Value is missing': "Valor não informado",
        "Type error": "Valor de tipo incorreto",
        'ensure this value has at most {limit_value} characters': 'Este campo deve possuir no máximo {limit_value} caracteres',
    }

    try:
        return translations[msg_id]
    except KeyError:
        return msg_id

error_messages = {
    'type_error': _("Type error"),
    'type_error.float': _('Value is not a valid float'),
    'value_error.missing': _("Value is missing"),
    'value_error.any_str.min_length': _('ensure this value has at least {limit_value} characters'),
    'value_error.any_str.max_length': _('ensure this value has at most {limit_value} characters')
}
