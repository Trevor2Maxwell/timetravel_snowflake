"""
Example Hex notebook showing how to use the snowflake_timetravel package.

This demonstrates how to:
1. Install the package from GitHub
2. Connect to Snowflake using Hex's built-in connection
3. Run time travel queries
4. Create visualizations comparing current and historical data
"""

# Install the package from GitHub
# %pip install git+https://github.com/Trevor2Maxwell/snowflake_timetravel.git@main

# Import the package
import snowflake_timetravel as stt
import pandas as pd

# Get a connection to Snowflake using Hex's built-in connection
# This will automatically detect if we're in dev or prod environment
conn = stt.connect()

# Example 1: Simple time travel query (7 days ago)
# ----------------------------------------------
query = """
select 
    DATE_TRUNC('MONTH', TRANSACTION_DATE) AS PERIOD
    , sum(AMOUNT::float/100)::int as SUM
    , count(*) COUNT
    , min(API_CREATE_DATE)::date API_MIN_CREATE_DATE
    , min(CREATED_AT)::date DB_MIN_CREATE_DATE
    , max(API_LAST_CHANGE_DATE)::date API_MAX_UPDATE_DATE
from TRANSACTIONS
where 
    PRACTICE_ID = {{practice_id}}
    AND IS_PAYMENT = 'false'
    AND TRANSACTION_DATE <= current_date
    AND TRANSACTION_DATE >= DATEADD(YEAR, -4, CURRENT_DATE)
    AND API_REMOVED_DATE IS NULL
group by 1
order by 1 desc
"""

# Get data from 7 days ago
historical_df = stt.query_at_offset(conn, query, days_ago=7)

# Get current data
current_df = conn.execute(query)

# Example 2: Using the compare_timetravel function
# ----------------------------------------------
# This does the same as above but in a single function call
current_df, historical_df = stt.compare_timetravel(conn, query, days_ago=7)

# Example 3: Create a visualization comparing the data
# ----------------------------------------------
fig = stt.visualize_comparison(
    current_df=current_df,
    historical_df=historical_df,
    x_column='PERIOD',
    y_column='SUM',
    current_label='Active Total Revenue',
    historical_label='Snowflake Time travel 7 Days Ago Total Revenue',
    title='Revenue Comparison: Current vs 7 Days Ago',
    chart_type='both'  # Creates both bar and line charts
)

# Display the figure in Hex
fig.show()

# Example 4: More complex query with parameters
# ----------------------------------------------
parameterized_query = """
select 
    DATE_TRUNC('MONTH', TRANSACTION_DATE) AS PERIOD
    , sum(AMOUNT::float/100)::int as SUM
    , count(*) COUNT
from TRANSACTIONS
where 
    PRACTICE_ID = :practice_id
    AND IS_PAYMENT = :is_payment
    AND TRANSACTION_DATE <= current_date
    AND TRANSACTION_DATE >= DATEADD(YEAR, :years_back, CURRENT_DATE)
    AND API_REMOVED_DATE IS NULL
group by 1
order by 1 desc
"""

params = {
    'practice_id': 12345,  # Replace with actual practice ID
    'is_payment': 'false',
    'years_back': -4
}

# Compare data with parameters
current_df, historical_df = stt.compare_timetravel(
    conn, 
    parameterized_query, 
    days_ago=7, 
    params=params
)

# Create visualization
fig = stt.visualize_comparison(
    current_df=current_df,
    historical_df=historical_df,
    x_column='PERIOD',
    y_column='SUM',
    current_label='Current Revenue',
    historical_label='7 Days Ago Revenue'
)

# Display the figure
fig.show()

# Example 5: Using the TimeTravelResult model for more advanced usage
# ----------------------------------------------
from snowflake_timetravel.models import TimeTravelResult
import datetime

# Create a TimeTravelResult object
result = TimeTravelResult(
    data=historical_df,
    query_time=datetime.datetime.now(),
    timestamp=f"DATEADD(DAY, -7, CURRENT_TIMESTAMP())",
    metadata={
        'query': query,
        'practice_id': 12345  # Replace with actual practice ID
    }
)

# Use the model's methods
print(f"Row count: {result.row_count}")

# Save to CSV if needed
# result.to_csv('historical_data.csv')
