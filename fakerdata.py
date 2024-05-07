import pandas as pd
from faker import Faker
from datetime import datetime
import numpy as np

fake = Faker('uk-UA')

# Define the range of possible values
price_values = np.arange(40, 6001)
quantity_values = np.arange(1, 843)

# Define a probability distribution that favors smaller values
# Here we use a reciprocal function to make smaller values more likely
price_probs = 1.0 / price_values
quantity_probs = 1.0 / (quantity_values + 1)  # Add 1 to avoid division by zero

# Normalize the probabilities so they sum to 1
price_probs /= price_probs.sum()
quantity_probs /= quantity_probs.sum()

data ={
    'inv_num': [fake.ean8() for _ in range(200)],
    'price': np.random.choice(price_values, size=200, p=price_probs),
    'quantity': np.random.choice(quantity_values, size=200, p=quantity_probs),
    'warehouse': [fake.random_element(('A', 'B', 'C', 'D')) for _ in range(200)],
    'rating': [fake.random_int(min=1, max=10) for _ in range(200)],
}

# Generate date_added and date_updated
date_added = [fake.date_this_decade() for _ in range(200)]
date_updated = [fake.date_between_dates(date_start=date, date_end=datetime.today()) for date in date_added]
data['date_added'] = date_added
data['date_updated'] = date_updated

df = pd.DataFrame(data)

pd.options.display.width = 0
print(df.head(100))

df.to_excel('faker numbers.xlsx', index=False)