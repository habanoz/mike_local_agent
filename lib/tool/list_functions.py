import json 
import uuid
from typing import Dict

accounts=[{"id": 1234, "name": "primary","balance": 1100.0}, {"id": 456, "name": "2000 savings", "balance": 0.0}, {"id": 333, "name": "wife savings", "balance": 1250.0}]
transactions = {1234: [{"id": "tx1", "amount": 100, "description": "Deposit"}, {"id": "tx2", "amount": -50, "description": "Withdrawal"}],
               456: [{"id": "tx1", "amount": 100, "description": "Deposit"}, {"id": "tx2", "amount": -10, "description": "Withdrawal"}],
               333: [{"id": "tx1", "amount": 10, "description": "Deposit"}, {"id": "tx2", "amount": -50, "description": "Withdrawal"}]
               }

balances = {1234: 1100.0, 456: 0.0, 333: 1250.0}

memory: Dict[str, dict] = {}

def _new_memory_key(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

from pydantic import BaseModel, Field
from typing import List, Dict
class Account(BaseModel):
    """Represents user bank account."""
    id: int = Field(description="Account id")
    name: str = Field(description="Account name")
    balance: float = Field(description="Account balance")

def list_bank_accounts() -> str:
    """
    Returns a JSON-encoded list of bank accounts for the current user and a memory key for reference. 
    
    Use this function to retrieve a list of bank accounts associated with the user. The accounts are stored in memory for quick access with the given memoryKey. Use display_accounts if user wants to see the list of accounts in a formatted way.

    Each account has:   
        - id (int)
        - name (str)
        - balance (float)
    
    Example return value:
    '{"accounts": [{"id": 123, "name": "acct 1", "balance": 33.0}, {"id": 456, "name": "acct 2", "balance": 0.0}], "memoryKey": "accounts_12345678"}'

    Use this function to retrieve account IDs and related information for further operations. Accounts are stored in memory for quick access with the given memoryKey.
    """
    memory_key = _new_memory_key("accounts")
    memory[memory_key] = {"accounts": accounts}
    return json.dumps({"accounts": accounts, "memoryKey": memory_key})

def list_bank_transactions(account_id: int) -> str:
    """
    Returns a JSON-encoded list of transactions for the given bank account and a memory key for reference. Transactions will be in the reverse recency order, meaning oldest record will be listed first, most recent will be last.

    Args:
        account_id (int): The ID of the bank account. If not known, use the list_bank_accounts() function to get valid account IDs.

    Returns:
        str: A JSON string representing a list of transactions and a memory key.
            Each transaction includes:
                - id (str): The unique transaction ID.
                - amount (float): The transaction amount (positive for deposits, negative for withdrawals).
                - description (str): A short description of the transaction.
                
    Example return value:
    '{"transactions": [{"id": "tx1", "amount": 100, "description": "Deposit"}, {"id": "tx2", "amount": -50, "description": "Withdrawal"}], "memoryKey": "transactions_12345678"}'
    """
    if account_id not in transactions:
        return json.dumps({"error": f"No such account id: {account_id}"})
    
    memory_key = _new_memory_key(f"tx_{account_id}")
    memory[memory_key] = {"transactions": transactions[account_id], "account_id": account_id}
    return json.dumps({"transactions": transactions[account_id], "memoryKey": memory_key})

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

def display_accounts(memoryKey: str) -> str:
    """If user wants to see list of accounts call this function. This function returns a placeholder that will be replaced by downstream systems with a formatted table of accounts.
    
    Args:
        memoryKey (str): Memory key from list_bank_accounts() response
    
    Workflow:
        1. Call list_bank_accounts() to get accounts and memoryKey if not done already.
        2. Use the returned memoryKey and call this function to obtain a replacement string.
        3. The replacement string will be replaced by downstream systems with a formatted table of accounts.
    
    Returns: UI placeholder that gets replaced with formatted account table
    """
    return f"%to_be_replaced_accounts_{memoryKey}%"

def display_transactions(memoryKey: str) -> str:
    """If user wants to see list of transactions call this function. This function returns a placeholder that will be replaced by downstream systems with a formatted table of transactions.
    
    Args:
        memoryKey (str): Memory key from list_bank_transactions response
    
    Workflow:
        1. Call list_bank_transactions(acct_id) to get transactions and memoryKey if not done already.
        2. Use the returned memoryKey and call this function to obtain a replacement string.
        3. The replacement string will be replaced by downstream systems with a formatted table of transactions.
    
    Returns: UI placeholder that gets replaced with formatted transaction table
    """
    return f"%to_be_replaced_transactions_{memoryKey}%"