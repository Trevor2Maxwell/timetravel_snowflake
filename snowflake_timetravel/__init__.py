"""
Snowflake TimeTravel package for working with Snowflake's Time Travel feature.
"""

__version__ = '0.1.0'

# Import and expose key functions
from .utils.timetravel import (
    query_at_time,
    query_at_offset,
    compare_timetravel,
    visualize_comparison
)

__all__ = [
    'query_at_time',
    'query_at_offset',
    'compare_timetravel',
    'visualize_comparison',
]
