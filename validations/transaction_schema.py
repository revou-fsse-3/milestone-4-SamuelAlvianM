transaction_schema = {
    "from_account_id": {"type": "integer", "required": True},
    "to_account_id": {"type": "integer", "required": True},
    "type_transaction": {"type": "string", "allowed": ["deposit", "withdrawal", "transfer"], "required": True},
    "amount": {"type": "number", "min": 0, "required": True},
    "description": {"type": "string"},
}