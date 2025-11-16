
import pandas as pd

df = pd.read_csv('/Users/satheeswaranharikrishnan/Desktop/SmartTicket/customer_support_tickets.csv')
df.columns

import pandas as pd

# Load CSV and parse the date column
df = pd.read_csv('customer_support_tickets.csv', parse_dates=['Date of Purchase'])

# Rename it for simplicity
df.rename(columns={'Date of Purchase': 'Date'}, inplace=True)

# Quick check
df.info()
df.head()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load dataset (already uploaded to Colab)
df = pd.read_csv('customer_support_tickets.csv', parse_dates=['Date of Purchase'])
df.rename(columns={'Date of Purchase': 'Date'}, inplace=True)

# Quick look
print(df.shape)
df.info()
df.head(3)

# Check for missing values
df.isnull().sum().sort_values(ascending=False).head(10)

# Fill or drop missing values
df['Customer Age'].fillna(df['Customer Age'].median(), inplace=True)
df['Customer Gender'].fillna('Unknown', inplace=True)
df['Ticket Priority'].fillna('Medium', inplace=True)
df.dropna(subset=['Date'], inplace=True)

# Show missing values count per column (top 10)
missing_counts = df.isnull().sum().sort_values(ascending=False)
print(missing_counts.head(10))

# Show the percentage missing as well
pct_missing = (df.isnull().mean() * 100).sort_values(ascending=False)
print(pct_missing.head(10))

df.drop(['Resolution', 'Time to Resolution'], axis=1, inplace=True)

df['First Response Time'] = pd.to_datetime(df['First Response Time'], errors='coerce')

df['Response_Delay_Hours'] = (df['First Response Time'] - df['Date']).dt.total_seconds() / 3600

df['Response_Delay_Hours'].fillna(df['Response_Delay_Hours'].median(), inplace=True)

df.info()
df.describe()
df.head()

import matplotlib.pyplot as plt

daily_tickets = df.groupby('Date').size().reset_index(name='Ticket_Count')

plt.figure(figsize=(12,5))
plt.plot(daily_tickets['Date'], daily_tickets['Ticket_Count'])
plt.title('Daily Ticket Volume Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Tickets')
plt.grid(True)
plt.show()

df['Ticket Priority'].value_counts().plot(kind='bar', color='skyblue', figsize=(7,4))
plt.title('Tickets by Priority')
plt.xlabel('Priority')
plt.ylabel('Count')
plt.show()

# Aggregate ticket count by date
ticket_daily = df.groupby('Date').size().reset_index(name='Ticket_Count')

# Sort by date to ensure order
ticket_daily.sort_values('Date', inplace=True)

ticket_daily.head()

import matplotlib.pyplot as plt

plt.figure(figsize=(12,5))
plt.plot(ticket_daily['Date'], ticket_daily['Ticket_Count'], label='Ticket Count')
plt.title('Daily Ticket Volume')
plt.xlabel('Date')
plt.ylabel('Number of Tickets')
plt.legend()
plt.show()

from statsmodels.tsa.arima.model import ARIMA
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Use your daily ticket data
data = ticket_daily.set_index('Date')['Ticket_Count']

# Train/test split (80-20)
train_size = int(len(data) * 0.8)
train, test = data[:train_size], data[train_size:]

# Build ARIMA model
model = ARIMA(train, order=(5,1,0))  # (p,d,q) parameters
model_fit = model.fit()

# Forecast future values for test period
forecast = model_fit.forecast(steps=len(test))

# Evaluation
mae = mean_absolute_error(test, forecast)
rmse = np.sqrt(mean_squared_error(test, forecast))

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")

# Plot
plt.figure(figsize=(12,5))
plt.plot(train.index, train, label='Train')
plt.plot(test.index, test, label='Test')
plt.plot(test.index, forecast, label='Forecast', color='green')
plt.title('ARIMA Forecast on Ticket Volume')
plt.legend()
plt.show()