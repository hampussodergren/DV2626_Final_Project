import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_json("properties.json")
data = data.sort_values(by="sold_at", ascending=False)
print(data.head())
print(data.columns.values.tolist())
print(data.loc[0:3])

import matplotlib.pyplot as plt
from datetime import datetime, timezone
import pandas as pd

# select only data for Villa and remove remove data without sale price
villa_data = data[(data['property_type'] == 'Villa') & (data['sold_at'] > 0)]

# onvert sold_at timestamps to datetime
villa_data['sold_at_date'] = villa_data['sold_at'].apply(
    lambda x: datetime.fromtimestamp(x, tz=timezone.utc)
)

# group by year and month and calculate average price
villa_data['year_month'] = villa_data['sold_at_date'].dt.to_period('M')
monthly_avg = villa_data.groupby('year_month')['price'].mean().reset_index()

# make averages for readable graph
monthly_avg['year_month'] = monthly_avg['year_month'].dt.to_timestamp()
monthly_avg['price_millions'] = monthly_avg['price'] / 1e6

# plot
plt.figure(figsize=(12, 6))
plt.plot(monthly_avg['year_month'], monthly_avg['price_millions'], linestyle='-', linewidth=2, label='Average Price')

plt.title('Average Villa Price Per Month Over Time')
plt.xlabel('Date')
plt.ylabel('Average Price (in Millions)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.show()
