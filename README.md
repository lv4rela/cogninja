# Cogninja Tool

**Cogninja Tools**  Cogninja Tools: With Cogninja Tools, you can crawl web pages to find JavaScript files, extract information related to Amazon Cognito from these files, and interact with AWS Cognito to perform user sign-up, authenticate users, and obtain AWS credentials if the application is vulnerable to Cognito misconfiguration.

## About Aws Cognito

**Amazon Cognito** is a service provided by AWS that simplifies user authentication and access control for web and mobile applications. It offers secure and scalable user management, including user sign-up, sign-in, and access control, and integrates with other AWS services to provide a comprehensive authentication and authorization solution.

**Key Features**

- **User Pools**: Manage and authenticate users for your app. Users can sign up, sign in, and manage their profiles using built-in UI components or custom ones.
- **Identity Pools**: Provide temporary AWS credentials for users to access AWS resources directly, such as S3 buckets or DynamoDB tables.
- **Federation**: Support for federated identities from social identity providers (like Facebook or Google) or enterprise identity providers (like SAML-based systems).
- **Customizable Authentication Flows**: Tailor authentication processes to fit your application’s needs with custom workflows and triggers.

**Common Security Problems**

- Misconfigurations in Amazon Cognito can lead to significant security vulnerabilities. Some common security problems include:

- **Leaving Sign-Up Enabled**: If the sign-up feature is enabled without appropriate restrictions, unauthorized users may create accounts. This can be exploited to gain unauthorized access to the application or abuse the authentication system. To mitigate this risk, ensure that sign-up is restricted to trusted users or managed through custom workflows.

- **Improper Configuration of User Pool Settings**: Incorrect settings, such as weak password policies or inadequate multi-factor authentication requirements, can compromise security and lead to potential usability issues. It’s essential to configure these settings to adhere to best practices.

- **Misconfigured Identity Pools**: Problems with identity pool configuration, such as incorrect roles or policies, can restrict legitimate users from accessing AWS resources or inadvertently expose sensitive data. Properly configure roles and policies to ensure appropriate access control.

- **Insecure Custom Authentication Flows**: Custom authentication workflows or triggers that lack proper security measures can introduce vulnerabilities. These vulnerabilities may allow unauthorized access or result in data leakage. Secure custom flows by adhering to best practices and conducting thorough testing.

- **Unrestricted API Access**: Failing to secure API endpoints that interact with Cognito can expose sensitive user data or authentication mechanisms. Implement robust security measures to protect these endpoints from unauthorized access and potential attacks.
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
python cogninja.py \
  --user_pool_client_id abcdef1234567890abcdef1234567890 \
  --user_pool_id us-east-1_ExamplePoolId \
  --username john.doe@example.com \
  --password SecurePassword123! \
  --email john.doe@example.com \
  --region us-east-1 \
  --identity_pool_id us-east-1:12345678-1234-1234-1234-123456789012 \

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
