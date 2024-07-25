# Cogninja Tool

**Cogninja Tools**  Cogninja Tools: With Cogninja Tools, you can crawl web pages to find JavaScript files, extract information related to Amazon Cognito from these files, and interact with AWS Cognito to perform user sign-up, authenticate users, and obtain AWS credentials if the application is vulnerable to Cognito misconfiguration.

## Features

**Cogcrawling**
- **Crawl Web Pages:** Retrieve JavaScript files from the given URL.
- **Extract Cognito Information:** Search for specific patterns related to Amazon Cognito in JavaScript files.
- **Headless Operation:** Runs Firefox in headless mode to avoid GUI overhead.
**Cogninja**
- **Sign Up**: Register a new user with Cognito.
- **Obtain Tokens**: Retrieve access and ID tokens after user authentication.
- **Get AWS Credentials**: Fetch AWS credentials using the Cognito Identity ID and tokens.
- **Interactive Menu**: A user-friendly CLI menu for input and output.

## Prerequisites

- Python 3.x
- AWS CLI configured with credentials
- **GeckoDriver:** Required for Selenium with Firefox. [Download GeckoDriver](https://github.com/mozilla/geckodriver/releases)


## Dependencies

- **Selenium**
- **Requests**
- **boto3**
- **colorama**

## Installation

1. Clone the repository:

    ```
     git clone https://github.com/lv4rela/cogninja.git
     cd cogninja
    ```

2. Install the required Python packages:

    ```
    pip install -r requirements.txt
    ```

## Configuration

**Cogninja**

Before running the script, ensure you have got from **Cogcrawling** following details, or if you already have, just enjoy it:

- **Cognito User Pool Client Id**
- **Cognito Identity Pool Id**
- **AWS Region**

## Usage

**Cogninja**

Run the script with:

```
python cogninja.py
```
**Cogcrawling**

You can run the script with either a single URL or a file containing a list of URLs.

### Command-Line Arguments

- **`-u` or `--url`**: The URL of the web page to crawl.
- **`-f` or `--file`**: A file containing a list of URLs to crawl (one URL per line).

### Example Commands

**Crawl a single URL:**

```
python cogcrawling.py -u https://www.example.com
```

**Crawl URLs from a file:**

```
python cogcrawling.py -f urls.txt
```
