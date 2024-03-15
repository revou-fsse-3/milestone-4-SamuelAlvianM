

product_schema = {
    'name': {
        'type': 'string',
        'required': True
    },
    'price': {
        'type': 'integer',
        'min': 1,
        'required': True
    },
    'description': {
        'type': 'string',
        'required': True,
        'minlength':1
    }
}