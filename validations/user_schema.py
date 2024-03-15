

user_schema = {
    'username': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 200},
    'email': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 200, 'regex': '[^@]+@[^@]+\.[^@]+'},
    'password': {'type': 'string', 'required': True, 'minlength': 5, 'maxlength': 200}
}


