from pymongo import MongoClient
import spacy

# Connect to MongoDB
client = MongoClient("mongodb+srv://atharvabadhe:atharva@customerdatasetchatbot.v5b8c.mongodb.net/")
db = client["dataset"]  # Use the correct database name
collection = db["customer"]  # Use the correct collection name

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Chatbot functions
def get_all_customers():
    results = collection.find({}, {"CustomerID": 1, "_id": 0})  # Retrieve only CustomerID
    customer_ids = [result["CustomerID"] for result in results]
    return customer_ids

def get_all_transactions():
    results = collection.find()
    return list(results)

def get_total_customers():
    return len(collection.distinct("CustomerID"))

def get_total_transactions():
    return collection.count_documents({})

def get_latest_transactions(limit=10):
    results = collection.find().sort("PurchaseDate", -1).limit(limit)
    return list(results)

def get_transactions_by_customer(customer_id):
    query = {"CustomerID": customer_id}
    results = collection.find(query)
    return list(results)

def get_total_spent_by_customer(customer_id):
    query = {"CustomerID": customer_id}
    results = collection.find(query)
    total = sum(result["TransactionAmount"] for result in results)
    return total

def get_customers_by_location(location):
    query = {"Location": location}
    results = collection.find(query)
    return list(results)

def get_customers_with_min_transactions(min_transactions):
    pipeline = [
        {"$group": {"_id": "$CustomerID", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": min_transactions}}}
    ]
    results = collection.aggregate(pipeline)
    customer_ids = [result["_id"] for result in results]
    customers = collection.find({"CustomerID": {"$in": customer_ids}})
    return list(customers)

def get_highest_spending_customer():
    pipeline = [
        {"$group": {"_id": "$CustomerID", "total": {"$sum": "$TransactionAmount"}}},
        {"$sort": {"total": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0] if result else None

def get_transactions_above_amount(amount):
    query = {"TransactionAmount": {"$gt": amount}}
    results = collection.find(query)
    return list(results)

def get_transactions_below_amount(amount):
    query = {"TransactionAmount": {"$lt": amount}}
    results = collection.find(query)
    return list(results)

def get_average_transaction_amount():
    pipeline = [
        {"$group": {"_id": None, "average_amount": {"$avg": "$TransactionAmount"}}}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0]["average_amount"] if result else 0

def get_top_transactions(limit=5):
    results = collection.find().sort("TransactionAmount", -1).limit(limit)
    return list(results)

def get_transactions_in_range(min_amount, max_amount):
    query = {"TransactionAmount": {"$gte": min_amount, "$lte": max_amount}}
    results = collection.find(query)
    return list(results)

def get_transactions_by_product(product):
    # Ensure the product name is correctly formatted (e.g., "Product A")
    product = product.strip().title()  # Convert to title case (e.g., "product a" -> "Product A")
    query = {"ProductInformation": product}
    results = collection.find(query)
    return list(results)

def get_total_revenue_by_product(product):
    product = product.strip().title()  # Convert to title case
    pipeline = [
        {"$match": {"ProductInformation": product}},
        {"$group": {"_id": None, "total": {"$sum": "$TransactionAmount"}}}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0]["total"] if result else 0

def get_most_popular_product():
    pipeline = [
        {"$group": {"_id": "$ProductInformation", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0] if result else None

def get_product_with_highest_avg_transaction():
    pipeline = [
        {"$group": {"_id": "$ProductInformation", "average": {"$avg": "$TransactionAmount"}}},
        {"$sort": {"average": -1}},
        {"$limit": 1}
    ]
    result = list(collection.aggregate(pipeline))
    return result[0] if result else None

# Intent recognition
def extract_intent(text):
    if "all customers" in text or "all customer ids" in text or "show all customer ids" in text:
        return "all_customers"
    elif "all transactions" in text:
        return "all_transactions"
    elif "total customers" in text:
        return "total_customers"
    elif "total transactions" in text:
        return "total_transactions"
    elif "latest transactions" in text:
        return "latest_transactions"
    elif "transactions for customer" in text: #
        return "transactions_by_customer"
    elif "total spent by" in text: #
        return "total_spent_by_customer"
    elif "customers in" in text:
        return "customers_by_location"
    elif "customers with more than" in text: #
        return "customers_with_min_transactions"
    elif "highest spending customer" in text:
        return "highest_spending_customer"
    elif "transactions above" in text:
        return "transactions_above_amount"
    elif "transactions below" in text:
        return "transactions_below_amount"
    elif "average transaction amount" in text:
        return "average_transaction_amount"
    elif "top transactions" in text:
        return "top_transactions"
    elif "transactions between" in text:
        return "transactions_in_range"
    elif "transactions for product" in text: #<----
        return "transactions_by_product"
    elif "total revenue from" in text:
        return "total_revenue_by_product"
    elif "most popular product" in text:
        return "most_popular_product"
    elif "product with highest average transaction" in text:
        return "product_with_highest_avg_transaction"
    return None

# Chatbot logic
def format_transactions(transactions):
    """
    Format transactions as an HTML table.
    """
    if not transactions:
        return "No transactions found."

    table = "<table class='table table-bordered table-striped'><thead><tr>"
    table += "<th>Customer ID</th><th>Order ID</th><th>Product</th><th>Amount</th><th>Date</th><th>Location</th></tr></thead><tbody>"
    
    for transaction in transactions:
        table += f"<tr>"
        table += f"<td>{transaction['CustomerID']}</td>"
        table += f"<td>{transaction['OrderID']}</td>"
        table += f"<td>{transaction['ProductInformation']}</td>"
        table += f"<td>${transaction['TransactionAmount']:.2f}</td>"
        table += f"<td>{transaction['PurchaseDate']}</td>"
        table += f"<td>{transaction['Location']}</td>"
        table += f"</tr>"
    
    table += "</tbody></table>"
    return table

def chatbot_response(user_input):
    intent = extract_intent(user_input.lower())
    
    if intent == "all_customers":
        customers = get_all_customers()
        return f"All customer IDs: {', '.join(map(str, customers))}"
    
    elif intent == "all_transactions":
        transactions = get_all_transactions()
        return format_transactions(transactions)
    
    elif intent == "total_customers":
        total = get_total_customers()
        return f"Total customers: {total}"
    
    elif intent == "total_transactions":
        total = get_total_transactions()
        return f"Total transactions: {total}"
    
    elif intent == "latest_transactions":
        limit = 10
        transactions = get_latest_transactions(limit)
        return format_transactions(transactions)
    
    elif intent == "transactions_by_customer":
        customer_id = int(user_input.split()[-1])  # Extract customer ID from input
        transactions = get_transactions_by_customer(customer_id)
        return format_transactions(transactions)
    
    elif intent == "total_spent_by_customer":
        customer_id = int(user_input.split()[-1])  # Extract customer ID from input
        total = get_total_spent_by_customer(customer_id)
        return f"Total spent by customer {customer_id}: ${total:.2f}"
    
    elif intent == "customers_by_location":
        location = user_input.split("in")[-1].strip()
        customers = get_customers_by_location(location)
        return f"Customers in {location}: {', '.join(map(str, customers))}"
    
    elif intent == "customers_with_min_transactions":
        min_transactions = int(user_input.split("more than")[-1].strip())
        customers = get_customers_with_min_transactions(min_transactions)
        return f"Customers with more than {min_transactions} transactions: {', '.join(map(str, customers))}"
    
    elif intent == "highest_spending_customer":
        customer = get_highest_spending_customer()
        return f"Highest spending customer ID: {customer['_id']} (Total: ${customer['total']:.2f})"
    
    elif intent == "transactions_above_amount":
        amount = float(user_input.split("above")[-1].strip().replace("$", ""))
        transactions = get_transactions_above_amount(amount)
        return format_transactions(transactions)
    
    elif intent == "transactions_below_amount":
        amount = float(user_input.split("below")[-1].strip().replace("$", ""))
        transactions = get_transactions_below_amount(amount)
        return format_transactions(transactions)
    
    elif intent == "average_transaction_amount":
        average = get_average_transaction_amount()
        return f"The average transaction amount is ${average:.2f}"
    
    elif intent == "top_transactions":
        limit = 5
        transactions = get_top_transactions(limit)
        return format_transactions(transactions)
    
    elif intent == "transactions_in_range":
        min_amount = float(user_input.split("between")[-1].split("and")[0].strip().replace("$", ""))
        max_amount = float(user_input.split("and")[-1].strip().replace("$", ""))
        transactions = get_transactions_in_range(min_amount, max_amount)
        return format_transactions(transactions)
    
    elif intent == "transactions_by_product":
        product = user_input.split("product")[-1].strip()
        transactions = get_transactions_by_product(product)
        return format_transactions(transactions)
    
    elif intent == "total_revenue_by_product":
        product = user_input.split("from")[-1].strip()
        total = get_total_revenue_by_product(product)
        return f"Total revenue from {product}: ${total:.2f}"
    
    elif intent == "most_popular_product":
        product = get_most_popular_product()
        return f"Most popular product: {product['_id']} (Transactions: {product['count']})"
    
    elif intent == "product_with_highest_avg_transaction":
        product = get_product_with_highest_avg_transaction()
        return f"Product with highest average transaction: {product['_id']} (Average: ${product['average']:.2f})"
    
    else:
        return "I don't understand. Please try again."