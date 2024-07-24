from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import re
import argparse
from urllib.parse import urljoin
from colorama import Fore, init

init(autoreset=True)

def initialize_driver():
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/local/bin/geckodriver") 
    return webdriver.Firefox(service=service, options=options)

def fetch_js_files(driver, url):
    driver.get(url)
    script_elements = driver.find_elements(By.TAG_NAME, "script")
    link_elements = driver.find_elements(By.XPATH, "//link[@rel='preload' and @as='script']")
    
    js_files = [script.get_attribute('src') for script in script_elements if script.get_attribute('src') and script.get_attribute('src').endswith('.js')]
    js_files.extend([link.get_attribute('href') for link in link_elements if link.get_attribute('href').endswith('.js')])

    js_files = list(set(filter(None, js_files))) 
    return [urljoin(url, js_file) for js_file in js_files]

def extract_cognito_info(content, source):
    patterns = {
        'userPoolClientId': r'userPoolClientId["\']?\s*:\s*["\']([a-zA-Z0-9-_]+)["\']',
        'userPoolId': r'userPoolId["\']?\s*:\s*["\']([a-z]{2}-[a-z]+-\d+_[a-zA-Z0-9-_]+)["\']',
        'client_id': r'client_id["\']?\s*:\s*["\']([a-zA-Z0-9-_]+)["\']',
        'IdentityPoolId': r'IdentityPoolId["\']?\s*:\s*["\']([a-zA-Z0-9-_]+)["\']',
        'userPoolWebClientId': r'userPoolWebClientId["\']?\s*:\s*["\']([a-zA-Z0-9-_]+)["\']',
    }

    cognito_info = {key: re.findall(pattern, content) for key, pattern in patterns.items()}

    if any(cognito_info.values()):
        print(f"{Fore.GREEN}\nFound Cognito info in: {Fore.WHITE}{source}")
        for key, values in cognito_info.items():
            if values:
                for value in values:
                    print(f"{Fore.MAGENTA}{key}: {Fore.WHITE}{value}")

def process_page(driver, url):
    url = ensure_http_prefix(url)
    try:
        driver.get(url)
        main_content = driver.page_source
        extract_cognito_info(main_content, url)

        js_files = fetch_js_files(driver, url)
        for js_file in js_files:
            try:
                driver.get(js_file)
                js_content = driver.page_source
                extract_cognito_info(js_content, js_file)
            except Exception as e:
                print(f"{Fore.RED}Error fetching JS file: {Fore.WHITE}{js_file} - {e}")
    except Exception as e:
        print(f"{Fore.RED}Error fetching main page: {Fore.WHITE}{url} - {e}")

def ensure_http_prefix(url):
    return 'https://' + url if not url.startswith(('http://', 'https://')) else url

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl web pages for JavaScript files and extract Amazon Cognito information.")
    parser.add_argument("-u", "--url", help="The URL of the web page to crawl")
    parser.add_argument("-f", "--file", help="A file containing a list of URLs to crawl")
    args = parser.parse_args()

    driver = initialize_driver()
    try:
        if args.url:
            process_page(driver, args.url)
        elif args.file:
            try:
                with open(args.file, 'r') as f:
                    urls = [line.strip() for line in f.readlines()]
                    for url in urls:
                        if url:
                            process_page(driver, url)
            except FileNotFoundError:
                print(f"{Fore.RED}Error: File {args.file} not found.")
        else:
            print(f"{Fore.YELLOW}INFO: Please provide either a URL with -u or a file with -f.")
    finally:
        driver.quit()
