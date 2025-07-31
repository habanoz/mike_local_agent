import json 

accounts=[{"id": "123", "name": "primary","balance": 1000}, {"id": "456", "name": "2000 savings", "balance": 0}, {"id": "333", "name": "wife savings", "balance": 1000}]
trasactions = {"123": [{"id": "tx1", "amount": 100, "description": "Deposit"}, {"id": "tx2", "amount": -50, "description": "Withdrawal"}],
               "456": [{"id": "tx1", "amount": 100, "description": "Deposit"}, {"id": "tx2", "amount": -10, "description": "Withdrawal"}],
               "333": [{"id": "tx1", "amount": 10, "description": "Deposit"}, {"id": "tx2", "amount": -50, "description": "Withdrawal"}]
               }

balances = {"123": 1000, "456": 0, "333": 1000}

def list_bank_accounts() -> str:  
    """List bank accounts for the user. You can use this function to get the list of account ids. This can be useful to allow user to select an account for further operations.
    
    Returns:
        str: A JSON representation of list of accounts. Accounts are represented as a list of dictionaries with keys: id, name, balance.
    """
    return json.dumps(accounts)

def list_bank_transactions(account_id: str) -> str:  
    """List transactions for a given bank account. list_bank_accounts function can be used to get list of the account ids."""
    if account_id not in trasactions:
        return f"No such account id: {account_id}."
    
    return json.dumps(trasactions[account_id]) 

def get_account_balance(account_id: str) -> str:
    """Get the balance of a specific bank account. list_bank_accounts function can be used to get list of the account ids."""
    
    if account_id not in balances:
        return f"No such account id: {account_id}."
    
    return str(balances[account_id])
