account_schema = {
    'account_type': {'type': 'string', 'required': True, 'allowed': ['savings', 'trading', 'platinum']},
    'account_number': {'type': 'string', 'required': True, 'minlength': 5, 'maxlength': 20},
    'balance': {'type': 'float', 'required': True},  
}

