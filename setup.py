from setuptools import setup, find_packages

setup(
    name="snowflake_timetravel",
    version="0.1.0",
    description="A package for Snowflake time travel functionality in Hex notebooks",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "snowflake-connector-python",
        # Add other dependencies as needed
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
)
