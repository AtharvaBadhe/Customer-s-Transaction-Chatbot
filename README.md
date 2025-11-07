# Customer Transaction Chatbot

A Python-based chatbot application that provides intelligent query capabilities over customer transaction data stored in MongoDB. The chatbot uses natural language processing to understand user queries and returns formatted results about customers, transactions, products, and revenue analytics.

## Features

### Query Capabilities

The chatbot supports a wide range of queries including:

**Customer Queries**
- Retrieve all customer IDs
- Get total number of customers
- Find customers by location
- Identify customers with minimum transaction counts
- Find the highest spending customer

**Transaction Queries**
- List all transactions
- Get total number of transactions
- Show latest transactions
- Find transactions by customer ID
- Get transactions above/below a specific amount
- Find transactions within a price range
- Calculate average transaction amount
- Display top transactions by amount

**Product Analytics**
- Show transactions for specific products
- Calculate total revenue by product
- Identify the most popular product
- Find product with highest average transaction value

## Technology Stack

- Python 3.x
- MongoDB (Cloud Atlas)
- spaCy (Natural Language Processing)
- PyMongo (MongoDB driver)

## Prerequisites

Before running the application, ensure you have the following installed:

```bash
pip install pymongo spacy
python -m spacy download en_core_web_sm
```

## Database Configuration

The application connects to a MongoDB Atlas cluster:

```python
mongodb+srv://atharvabadhe:atharva@customerdatasetchatbot.v5b8c.mongodb.net/
```

**Database Structure:**
- Database: `dataset`
- Collection: `customer`

**Document Schema:**
```json
{
  "CustomerID": "integer",
  "OrderID": "integer",
  "ProductInformation": "string",
  "TransactionAmount": "float",
  "PurchaseDate": "string",
  "Location": "string"
}
```

## Dataset

The application uses a dataset (`customer_data.csv`) containing:
- 1000+ transaction records
- Date range: April 11, 2023 - June 10, 2023
- Products: Product A, Product B, Product C, Product D
- Locations: New York, London, Paris, Tokyo
- Transaction amounts: $12.13 - $999.44

## Usage Examples

The chatbot understands natural language queries. Here are some example queries:

```
Show all customer IDs
List all transactions
How many customers are there?
What is the total number of transactions?
Show the latest 10 transactions
Find transactions for customer ID 1234
What is the total amount spent by customer ID 5678?
List customers in Tokyo
Show customers with more than 5 transactions
Who is the highest spending customer?
Show transactions above $500
List transactions below $100
What is the average transaction amount?
Show the top 5 transactions
List transactions between $200 and $800
Show transactions for product Product A
What is the total revenue from Product B?
What is the most popular product?
Which product has the highest average transaction?
```

## Response Format

The chatbot returns responses in two formats:

1. **Plain Text**: For aggregate data and simple queries
   - Customer counts, totals, averages
   - Single customer information

2. **HTML Tables**: For transaction lists
   - Formatted with Bootstrap styling
   - Columns: Customer ID, Order ID, Product, Amount, Date, Location
   - Easy to integrate into web interfaces

## Intent Recognition

The application uses keyword-based intent recognition to map user queries to appropriate database operations. The `extract_intent()` function identifies query patterns and routes them to the correct handler function.

## API Functions

### Customer Functions
- `get_all_customers()` - Returns list of all customer IDs
- `get_total_customers()` - Returns count of unique customers
- `get_customers_by_location(location)` - Filters customers by location
- `get_customers_with_min_transactions(min_transactions)` - Finds active customers
- `get_highest_spending_customer()` - Identifies top spender

### Transaction Functions
- `get_all_transactions()` - Returns all transaction records
- `get_total_transactions()` - Returns total transaction count
- `get_latest_transactions(limit)` - Gets most recent transactions
- `get_transactions_by_customer(customer_id)` - Customer transaction history
- `get_total_spent_by_customer(customer_id)` - Customer spending total
- `get_transactions_above_amount(amount)` - High-value transactions
- `get_transactions_below_amount(amount)` - Low-value transactions
- `get_transactions_in_range(min_amount, max_amount)` - Range filtering
- `get_average_transaction_amount()` - Calculates average
- `get_top_transactions(limit)` - Highest value transactions

### Product Functions
- `get_transactions_by_product(product)` - Product transaction history
- `get_total_revenue_by_product(product)` - Product revenue calculation
- `get_most_popular_product()` - Most frequently purchased product
- `get_product_with_highest_avg_transaction()` - Premium product identifier

## Limitations

- Query understanding is keyword-based (not true NLP)
- Requires exact product name formatting (e.g., "Product A")
- Customer IDs and amounts must be provided in specific formats
- No authentication or user management
- Database credentials are hardcoded

## Future Enhancements

- Implement true NLP using spaCy's entity recognition
- Add user authentication and session management
- Support for date range queries
- Export functionality (CSV, PDF)
- Integration with web framework (Flask/Django)
- Enhanced error handling and validation
- Support for fuzzy product name matching
- Real-time data updates
- Visualization of transaction trends

## License

This project is available for educational and commercial use.

## Author

Atharva Badhe

## Repository

https://github.com/AtharvaBadhe/Customer-s-Transaction-Chatbot
