import json 

def search_kb(query: str) -> str:
    """
    Search for a query in the knowledge base. Knowledge base includes documents about daily transaction limits, transaction fees, how to create a new bank account.

    Args:
        query (str): The search query. Documents are in english and document search works best with english queries.

    Returns:
        str: A JSON representation of A list of matching entries from the knowledge base.
    """
    results = [
        {"id": "1", "title": "Daily Transaction Limits", "content": "The daily transaction limit is $10,000."},
        {"id": "2", "title": "Transaction Fees", "content": "Transaction fees are $2 per transaction."},
        {"id": "3", "title": "Creating a New Account", "content": "To create a new account, you can use mobile app account creation feature or visit a branch to talk to a representative."},
        {"id": "4", "title": "Account Closure", "content": "You cannot close an account using the mobile app. To close an account, please visit a branch or call customer service."},
    ]
    return json.dumps(results)