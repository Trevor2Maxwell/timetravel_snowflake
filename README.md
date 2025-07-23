# Snowflake TimeTravel

A Python package for working with Snowflake's Time Travel functionality in Hex notebooks.

## Overview

This package provides utilities for leveraging Snowflake's Time Travel capabilities within Hex notebooks. It allows data analysts to develop code in their preferred IDE (Windsurf), push changes to GitHub, and seamlessly import the latest code into Hex notebooks.

## Features

- Query Snowflake data at specific points in time using the AT clause
- Compare current data with historical data
- Visualize time travel comparisons with Plotly
- Seamless integration with Hex notebooks
- Automatic environment detection (dev/prod)

## Installation

### In Hex Notebooks

To install the latest version directly from GitHub:

```python
%pip install git+https://github.com/Trevor2Maxwell/snowflake_timetravel.git@main
```

For a specific version or branch:

```python
%pip install git+https://github.com/Trevor2Maxwell/snowflake_timetravel.git@v0.1.0
```

### For Local Development

Clone the repository and install in development mode:

```bash
git clone https://github.com/Trevor2Maxwell/snowflake_timetravel.git
cd snowflake_timetravel
pip install -e .
```

## Usage

### Basic Usage

```python
import snowflake_timetravel as stt

# Connect to Snowflake (using Hex's secure connection)
conn = stt.connect()

# Query data as of a specific time
df = stt.query_at_time(
    conn, 
    "SELECT * FROM my_table", 
    timestamp="2023-07-22 12:00:00"
)

# Query data from N days ago
df = stt.query_at_offset(
    conn,
    "SELECT * FROM my_table",
    days_ago=7
)

# Compare current data with data from 7 days ago
current_df, historical_df = stt.compare_timetravel(
    conn,
    "SELECT * FROM my_table",
    days_ago=7
)
```

### Visualization Example

```python
import snowflake_timetravel as stt

# Connect to Snowflake
conn = stt.connect()

# Query to run
query = """
    select 
        DATE_TRUNC('MONTH', TRANSACTION_DATE) AS PERIOD
        , sum(AMOUNT::float/100)::int as SUM
    from MY_TABLE
    where TRANSACTION_DATE <= current_date
    group by 1
    order by 1 desc
"""

# Compare current data with data from 7 days ago
current_df, historical_df = stt.compare_timetravel(conn, query, days_ago=7)

# Create visualization
fig = stt.visualize_comparison(
    current_df=current_df,
    historical_df=historical_df,
    x_column='PERIOD',
    y_column='SUM',
    current_label='Current Revenue',
    historical_label='7 Days Ago Revenue',
    title='Revenue Comparison: Current vs 7 Days Ago',
    chart_type='both'  # Creates both bar and line charts
)

# Display the figure in Hex
fig.show()
```

## GitHub Integration Guide

This section explains how to set up GitHub integration for the Snowflake TimeTravel package, allowing you to develop code in Windsurf IDE, version control it with GitHub, and import the latest code into Hex notebooks.

### Prerequisites

- GitHub account (your account: `Trevor2Maxwell`)
- Git installed on your local machine
- Your Snowflake TimeTravel package code

### Step 1: Create a GitHub Repository

1. Log in to your GitHub account at [github.com](https://github.com)
2. Click the "+" icon in the top-right corner and select "New repository"
3. Name your repository `snowflake_timetravel`
4. Add a description: "Python package for working with Snowflake's Time Travel feature in Hex notebooks"
5. Choose "Public" visibility (unless you need it to be private)
6. Check "Add a README file"
7. Choose "Add .gitignore" with the "Python" template
8. Click "Create repository"

### Step 2: Clone the Repository Locally

```bash
# Navigate to your desired directory
cd /Users/tmaxwell/Personal-Project-Directory

# Clone the repository
git clone https://github.com/Trevor2Maxwell/snowflake_timetravel.git

# If you already have the code locally, you can initialize git and add the remote
cd /Users/tmaxwell/Personal-Project-Directory/Snowflake_Timetravel_Hex_Workbook_Prod
git init
git remote add origin https://github.com/Trevor2Maxwell/snowflake_timetravel.git
```

### Step 3: Add Your Code to the Repository

```bash
# Add all files to git
git add .

# Commit the changes
git commit -m "Initial commit of Snowflake TimeTravel package"

# Push to GitHub
git push -u origin main
```

### Step 4: Set Up GitHub Actions (Optional)

You can set up GitHub Actions to automatically run tests, linting, and other checks when you push code. Create a file at `.github/workflows/python-package.yml`.

### Step 5: Install the Package in Hex Notebooks

Once your code is pushed to GitHub, you can install it directly in Hex notebooks:

```python
# Install the package from GitHub
%pip install git+https://github.com/Trevor2Maxwell/snowflake_timetravel.git@main

# Import and use the package
import snowflake_timetravel as stt
```

## Development Workflow

1. Develop and test code locally in your preferred IDE (Windsurf)
2. Commit and push changes to GitHub
3. In your Hex notebook, install the latest version using the pip command above
4. Import and use the package as normal

### Best Practices

1. **Feature Branches**: Create a new branch for each feature or bug fix
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Regular Commits**: Make small, focused commits with clear messages
   ```bash
   git commit -m "Add function to compare time travel results"
   ```

3. **Pull Requests**: Use pull requests to review code before merging to main

4. **Version Tags**: Tag important releases with version numbers
   ```bash
   git tag -a v0.1.0 -m "Initial release"
   git push origin v0.1.0
   ```

5. **Install Specific Versions**: In Hex, you can install specific versions:
   ```python
   # Install a specific tag
   %pip install git+https://github.com/Trevor2Maxwell/snowflake_timetravel.git@v0.1.0
   ```

## Troubleshooting

- **Authentication Issues**: If you have authentication issues, consider using SSH keys or a personal access token
- **Package Not Found**: Make sure your `setup.py` is correctly configured
- **Import Errors**: Check that your package structure matches what's expected in your imports
- **Hex Installation Issues**: If Hex has trouble installing from GitHub, try using a specific commit hash instead of `main`

## License

[MIT License](LICENSE)
