import json 

accounts=[{"id": 1234, "name": "primary","balance": 1100.0}, {"id": 456, "name": "2000 savings", "balance": 0.0}, {"id": 333, "name": "wife savings", "balance": 1250.0}]
transactions = {1234: [{"id": "tx1", "amount": 100, "description": "Deposit"}, {"id": "tx2", "amount": -50, "description": "Withdrawal"}],
               456: [{"id": "tx1", "amount": 100, "description": "Deposit"}, {"id": "tx2", "amount": -10, "description": "Withdrawal"}],
               333: [{"id": "tx1", "amount": 10, "description": "Deposit"}, {"id": "tx2", "amount": -50, "description": "Withdrawal"}]
               }

balances = {1234: 1100.0, 456: 0.0, 333: 1250.0}

from pydantic import BaseModel, Field
from typing import List, Dict
class Account(BaseModel):
    """Represents user bank account."""
    id: int = Field(description="Account id")
    name: str = Field(description="Account name")
    balance: float = Field(description="Account balance")

def list_bank_accounts() -> str:
    """
    Returns a JSON-encoded list of bank accounts for the current user.

    Each account has:   
        - id (int)
        - name (str)
        - balance (float)
    
    Example return value:
    '[{"id": 135, "name": "Checking", "balance": 1250.75}, {"id": 467, "name": "Savings", "balance": 9800.50}]'

    Use this function to retrieve account IDs and related information for further operations.
    """
    return json.dumps(accounts)

def list_bank_transactions(account_id: int) -> str:
    """
    Returns a JSON-encoded list of transactions for the given bank account. Transactions will be in the reverse recency order, meaning oldest record will be listed first, most recent will be last.

    Args:
        account_id (int): The ID of the bank account. If not known, use the list_bank_accounts() function to get valid account IDs.

    Returns:
        str: A JSON string representing a list of transactions.
            Each transaction includes:
                - id (str): The unique transaction ID.
                - amount (float): The transaction amount (positive for deposits, negative for withdrawals).
                - description (str): A short description of the transaction.
                
    Example return value:
    '[{"id": "txn_001", "amount": -50.0, "description": "Grocery Store"}]'
    """
    if account_id not in transactions:
        return json.dumps({"error": f"No such account id: {account_id}"})
    
    return json.dumps(transactions[account_id])

def get_account_balance(account_id: int) -> str:
    """
    Returns the current balance of a specific bank account as a JSON object.

    Args:
        account_id (int): The ID of the bank account. If not known, use the list_bank_accounts() function to get valid account IDs.

    Returns:
        str: A JSON string representing the balance, or an error message.
            Successful example: '{"balance": 1200.50}'
            Error example: '{"error": "No such account id: acc_invalid"}'
    """
    if account_id not in balances:
        return json.dumps({"error": f"No such account id: {account_id}"})
    
    return json.dumps({"balance": balances[account_id]})
