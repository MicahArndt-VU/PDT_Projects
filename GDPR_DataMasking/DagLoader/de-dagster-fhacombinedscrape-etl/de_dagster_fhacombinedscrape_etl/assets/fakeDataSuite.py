from faker import Faker
import pandas as pd
import random

def generate_fake_df():
    # Initialize the fake data generator
    fake = Faker()

    # Initialize a data set
    data = [{# PII fields
        'user_id': fake.uuid4(),
        'name': fake.name(),
        'email': fake.email(),
        'phone_number': fake.phone_number(),
        'address': fake.address(),
    # Non-PII fields (e-commerce dim)
        'transaction_id': fake.uuid4(),
        'transaction_date': fake.date_this_year(),
        'product_name': fake.word().capitalize(),
        'product_category': random.choice(['Electronics', 'Clothing', 'Home', 'Books']),
        'quantity_purchased': random.randint(1, 5),
        'unit_price': round(random.uniform(5.0, 500.0), 2),
        'payment_method': random.choice(['Credit Card', 'PayPal', 'Debit Card']),
        'order_status': random.choice(['Completed', 'Shipped', 'Returned'])
    } for _ in range(1000)]
    df = pd.DataFrame(data)
    return df
