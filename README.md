# Cogninja Tool

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

    ```
     git clone https://github.com/lv4rela/cogninja.git
     cd cogninja
    ```

2. Install the required Python packages:

    ```
    pip install -r requirements.txt
    ```

## Configuration

Before running the script, ensure you have configured AWS CLI with the necessary credentials. You also need to provide the following details:

- **Cognito User Pool Client ID**
- **Cognito Identity ID**
- **AWS Region**

## Usage

Run the script with:

```
python cogninja.py
```







#########################################################################################








# Web Crawler for JavaScript Files and Amazon Cognito Information

This script crawls web pages to find JavaScript files and extracts information related to Amazon Cognito from these files. It uses Selenium with Firefox in headless mode to perform web scraping and processing.

## Features

- **Crawl Web Pages:** Retrieve JavaScript files from the given URL.
- **Extract Cognito Information:** Search for specific patterns related to Amazon Cognito in JavaScript files.
- **Headless Operation:** Runs Firefox in headless mode to avoid GUI overhead.

## Requirements

- **Python 3.x**
- **GeckoDriver:** Required for Selenium with Firefox. [Download GeckoDriver](https://github.com/mozilla/geckodriver/releases)

## Dependencies

- **Selenium**
- **Colorama**
- **Requests**

## Installation

1. **Clone the repository:**

   ```
   git clone https://github.com/lv4rela/cogninja.git
   cd cogninja
   
   ```

## Usage

You can run the script with either a single URL or a file containing a list of URLs.

### Command-Line Arguments

- **`-u` or `--url`**: The URL of the web page to crawl.
- **`-f` or `--file`**: A file containing a list of URLs to crawl (one URL per line).

### Example Commands

**Crawl a single URL:**

```
python crawler.py -u https://www.example.com
```

**Crawl URLs from a file:**

```
python crawler.py -f urls.txt
```
