# cogninja Tool

**Cogninja CLI Tool** is a command-line utility that interacts with AWS Cognito to perform user sign-up, authenticate users, and obtain AWS credentials.

## Features

- **Sign Up**: Register a new user with Cognito.
- **Obtain Tokens**: Retrieve access and ID tokens after user authentication.
- **Get AWS Credentials**: Fetch AWS credentials using the Cognito Identity ID and tokens.
- **Interactive Menu**: A user-friendly CLI menu for input and output.

## Prerequisites

- Python 3.x
- AWS CLI configured with credentials
- `boto3` and `colorama` Python packages

## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Before running the script, ensure you have configured AWS CLI with the necessary credentials. You also need to provide the following details:

- **Cognito User Pool Client ID**
- **Cognito Identity ID**
- **AWS Region**

## Usage

Run the script with:

```bash
python cogninja.py
