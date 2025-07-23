"""
Timetravel utilities for working with Snowflake's Time Travel feature.
"""

import pandas as pd
from typing import Optional, Union, Dict, Any, List, Tuple
import datetime
import re


def modify_from_clause_for_timetravel(query: str, time_travel_clause: str) -> str:
    """
    Modifies a SQL query to add time travel syntax to the FROM clause.
    
    Args:
        query: Original SQL query
        time_travel_clause: Time travel clause to add (e.g., "AT (TIMESTAMP => '2023-07-22 12:00:00')")
    
    Returns:
        Modified SQL query with time travel clause
    """
    # Regular expression to find FROM clauses
    # This handles both simple FROM statements and JOIN statements
    from_pattern = re.compile(r'from\s+([\w\._]+)\s', re.IGNORECASE)
    
    # Replace FROM clauses
    modified_query = from_pattern.sub(f'from \\1 {time_travel_clause} ', query)
    
    return modified_query


import typing
import hextoolkit
import pandas as pd

def sql_cell(
    source: str,
    data_connection_name: typing.Optional[str] = None,
    cast_decimals: bool = True,
) -> "pandas.DataFrame":
    """
    Args:
        source (str): SQL string to run against Data Connection.
        data_connection_name (Optional[str], optional): Data Connection to run `source` against. Defaults to None.
        cast_decimals (bool, optional): Whether or not to cast Decimal types to floats. Defaults to True.
    Returns:
        pandas.DataFrame: The result of running `source`.
    """
    if data_connection_name:
        hex_data_connection = hextoolkit.get_data_connection(data_connection_name)
        return hex_data_connection.query(source, cast_decimals=cast_decimals)
    return hextoolkit.query_dataframes(source, cast_decimals=cast_decimals)


def execute_query(
    query: str,
    data_connection_name: str = "Analytics",
    cast_decimals: bool = True
) -> pd.DataFrame:
    """
    Execute a SQL query using the provided connection.
    
    Args:
        connection: Snowflake connection object
        query: SQL query to execute
        params: Optional parameters for the query
    
    Returns:
        pandas DataFrame with the query results
    """
    if hasattr(connection, 'execute'):
        # Using Hex's connection
        return connection.execute(query, params)
    else:
        # Using standard snowflake-connector-python
        cursor = connection.cursor()
        cursor.execute(query, params or {})
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        return pd.DataFrame(data, columns=columns)


def query_at_time(
    query: str,
    timestamp: Union[str, datetime.datetime, int],
    db_name: str,
    data_connection_name: str = "Analytics",
    params: Optional[Dict[str, Any]] = None,
    cast_decimals: bool = True
) -> pd.DataFrame:
    """
    Execute a query against Snowflake using Time Travel to query data as of a specific time.
    
    Args:
        connection: Snowflake connection object (from hex_data_connection)
        query: SQL query to execute
        timestamp: Timestamp to query data at (can be string, datetime object, or days ago as int)
        params: Optional parameters for the query
    
    Returns:
        pandas DataFrame with the query results
    
    Example:
        >>> conn = connect()
        >>> # Using a specific timestamp
        >>> df = query_at_time(
        ...     conn,
        ...     "SELECT * FROM my_table",
        ...     timestamp="2023-07-22 12:00:00"
        ... )
        >>> # Using days ago (7 days ago)
        >>> df = query_at_time(
        ...     conn,
        ...     "SELECT * FROM my_table",
        ...     timestamp=7
        ... )
    """
    # Format timestamp based on type
    if isinstance(timestamp, int):
        # If timestamp is an integer, interpret as days ago
        time_travel_clause = f"AT (TIMESTAMP => DATEADD(DAY, -{timestamp}, CURRENT_TIMESTAMP()))"
    elif isinstance(timestamp, datetime.datetime):
        # If timestamp is a datetime object, format it
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        time_travel_clause = f"AT (TIMESTAMP => '{timestamp_str}')"
    else:
        # Assume timestamp is already a formatted string
        time_travel_clause = f"AT (TIMESTAMP => '{timestamp}')"
    
    # Modify the query to include time travel syntax
    time_travel_query = modify_from_clause_for_timetravel(query, time_travel_clause)
    
    # Execute the query
    return execute_query(connection, time_travel_query, params)


def query_at_offset(
    query: str,
    days_ago: int,
    db_name: str,
    data_connection_name: str = "Analytics",
    params: Optional[Dict[str, Any]] = None,
    cast_decimals: bool = True
)  -> pd.DataFrame:
    """
    Execute a query against Snowflake using Time Travel to query data as of N days ago.
    
    Args:
        connection: Snowflake connection object
        query: SQL query to execute
        days_ago: Number of days ago to query data from
        params: Optional parameters for the query
    
    Returns:
        pandas DataFrame with the query results
    
    Example:
        >>> conn = connect()
        >>> df = query_at_offset(
        ...     conn,
        ...     "SELECT * FROM my_table",
        ...     days_ago=7
        ... )
    """
    # Create time travel clause for days ago
    time_travel_clause = f"AT (TIMESTAMP => DATEADD(DAY, -{days_ago}, CURRENT_TIMESTAMP()))"
    
    # Modify the query to include time travel syntax
    time_travel_query = modify_from_clause_for_timetravel(query, time_travel_clause)
    
    # Execute the query
    return execute_query(connection, time_travel_query, params)


def compare_timetravel(
    query: str,
    days_ago: int = 7,
    db_name: str = None,
    data_connection_name: str = "Analytics",
    params: Optional[Dict[str, Any]] = None,
    cast_decimals: bool = True
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Compare current data with data from N days ago using the same query.
    
    Args:
        connection: Snowflake connection object
        query: SQL query to execute
        days_ago: Number of days ago to compare with (default: 7)
        params: Optional parameters for the query
    
    Returns:
        Tuple of (current_data, historical_data) as pandas DataFrames
    
    Example:
        >>> conn = connect()
        >>> current_df, historical_df = compare_timetravel(
        ...     conn,
        ...     "SELECT * FROM my_table",
        ...     days_ago=7
        ... )
    """
    # Get historical data
    historical_data = query_at_offset(connection, query, days_ago, params)
    
    # Get current data
    current_data = execute_query(connection, query, params)
    
    return current_data, historical_data


def visualize_comparison(
    current_df: pd.DataFrame,
    historical_df: pd.DataFrame,
    x_column: str,
    y_column: str,
    current_label: str = 'Current Data',
    historical_label: str = 'Historical Data',
    title: str = 'Data Comparison',
    chart_type: str = 'both',
    date_format: str = '%b-%Y'
) -> 'plotly.graph_objects.Figure':
    """
    Create a visualization comparing current and historical data.
    
    Args:
        current_df: DataFrame with current data
        historical_df: DataFrame with historical data
        x_column: Column name for x-axis
        y_column: Column name for y-axis
        current_label: Label for current data series
        historical_label: Label for historical data series
        title: Chart title
        chart_type: Type of chart ('bar', 'line', or 'both')
        date_format: Format for date values if x_column contains dates
    
    Returns:
        Plotly Figure object
    
    Example:
        >>> current_df, historical_df = compare_timetravel(conn, query, days_ago=7)
        >>> fig = visualize_comparison(
        ...     current_df, 
        ...     historical_df,
        ...     x_column='PERIOD',
        ...     y_column='SUM',
        ...     current_label='Current Revenue',
        ...     historical_label='7 Days Ago Revenue',
        ...     chart_type='both'
        ... )
        >>> fig.show()
    """
    try:
        import plotly.graph_objects as go
    except ImportError:
        raise ImportError("Plotly is required for visualization. Install with 'pip install plotly'.")
    
    # Create figure
    fig = go.Figure()
    
    # Add traces based on chart type
    if chart_type in ['bar', 'both']:
        # Bar chart for historical data
        fig.add_trace(go.Bar(
            x=historical_df[x_column],
            y=historical_df[y_column],
            name=historical_label,
            marker=dict(color='#FFD100', opacity=0.2),
            hovertemplate=f'%{{x|{date_format}}}<br>{historical_label}: $%{{y:,.0f}}K<extra></extra>'
        ))
        
        # Bar chart for current data
        fig.add_trace(go.Bar(
            x=current_df[x_column],
            y=current_df[y_column],
            name=current_label,
            marker=dict(color='#00E0FF', opacity=0.2),
            hovertemplate=f'%{{x|{date_format}}}<br>{current_label}: $%{{y:,.0f}}K<extra></extra>'
        ))
    
    if chart_type in ['line', 'both']:
        # Line chart for historical data
        fig.add_trace(go.Scatter(
            x=historical_df[x_column],
            y=historical_df[y_column],
            mode='lines',
            name=f'{historical_label} Trend',
            line=dict(color='#FFD100', width=4),
            hovertemplate=f'%{{x|{date_format}}}<br>{historical_label}: $%{{y:,.0f}}K<extra></extra>'
        ))
        
        # Line chart for current data
        fig.add_trace(go.Scatter(
            x=current_df[x_column],
            y=current_df[y_column],
            mode='lines',
            name=f'{current_label} Trend',
            line=dict(color='#00E0FF', width=4),
            hovertemplate=f'%{{x|{date_format}}}<br>{current_label}: $%{{y:,.0f}}K<extra></extra>'
        ))
    
    # Layout updates
    fig.update_layout(
        title=title,
        barmode='overlay',
        xaxis=dict(
            title=x_column,
            tickformat=date_format,
            tickangle=90,
            autorange='reversed'  # Reverse x-axis to match descending sort
        ),
        yaxis=dict(
            title=y_column,
            tickformat=',.0f',
            tickprefix='$',
            ticksuffix='K'
        ),
        legend=dict(orientation='h', x=0.5, xanchor='center', y=1.1),
        hovermode='x unified',
        template='plotly_white',
        width=1500,
        height=600
    )
    
    return fig
