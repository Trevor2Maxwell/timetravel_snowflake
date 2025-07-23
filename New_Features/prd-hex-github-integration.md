# Product Requirements Document: Hex-GitHub Integration

## Introduction/Overview

This project aims to streamline the development workflow between Windsurf IDE and Hex notebooks by creating a seamless integration between locally developed code (managed in GitHub) and Hex notebooks. The goal is to enable data analysts to write and maintain code in their preferred IDE (Windsurf) while leveraging Hex's visualization capabilities and secure Snowflake connection for company-wide deployment, eliminating the need for manual code copying and pasting.

## Goals

1. Create a development workflow that allows code to be written and maintained in Windsurf IDE
2. Enable version control of code via GitHub
3. Establish an automated process to import the latest code into Hex notebooks
4. Eliminate manual copy-pasting of code between environments
5. Maintain Hex's secure connection to Snowflake for data access
6. Ensure company-wide accessibility of the final Hex application

## User Stories

1. As a data analyst, I want to develop code in Windsurf IDE so that I can leverage my preferred development environment and tools.
2. As a data analyst, I want my code changes to be automatically reflected in Hex notebooks so that I don't have to manually copy-paste code.
3. As a data analyst, I want to version control my code in GitHub so that I can track changes and collaborate with others.
4. As a team member, I want to access the final Hex application with its visualizations so that I can analyze data without needing to understand the underlying code.

## Functional Requirements

1. The system must allow users to develop Python code in Windsurf IDE.
2. The system must structure the code as a proper Python package that can be installed via pip.
3. The system must integrate with GitHub for version control.
4. The system must provide a mechanism to automatically import the latest code from GitHub into Hex notebooks.
5. The system must preserve Hex's secure connection to Snowflake.
6. The system must allow for company-wide access to the published Hex application.
7. The system must update the Hex notebook with the latest code changes when the notebook is run.
8. The system must provide clear documentation on how to set up and use this workflow.

## Non-Goals (Out of Scope)

1. The system will not handle or store sensitive credentials.
2. The system will not modify Hex's core functionality.
3. The system will not automate the deployment of code to production environments beyond Hex.
4. The system will not handle data transformation or analysis logic - this remains the responsibility of the developer.
5. The system will not provide a GUI for managing the integration - it will be code/configuration based.

## Technical Considerations

1. The code should be structured as a proper Python package with setup.py or pyproject.toml.
2. The package should be installable via pip directly from GitHub (e.g., `pip install git+https://github.com/username/repo.git`).
3. For private repositories, appropriate authentication mechanisms must be configured in Hex.
4. The package should be compatible with the Python version used in Hex.
5. The package should handle dependencies appropriately to avoid conflicts with Hex's environment.
6. The integration should work with Snowflake's connection in Hex.

## Success Metrics

1. **Primary**: Ability to commit code changes in Windsurf IDE and see those changes reflected in Hex without manual copying.
2. **Secondary**: Reduction in time spent on code maintenance and synchronization between environments.
3. **Tertiary**: Increased code reuse across multiple Hex notebooks.

## Open Questions

1. What is the current Python version used in Hex, and are there any package compatibility issues to consider?
2. Are there any size limitations for packages that can be installed in Hex?
3. How frequently will the code need to be updated in Hex? (On every run, daily, weekly?)
4. Will multiple team members be contributing to the codebase, requiring branch management strategies?
5. Are there any specific Snowflake-related considerations for the package structure?
