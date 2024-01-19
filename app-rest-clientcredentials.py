import logging
import sys
import os
import json
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

# Function that obtains an access token
def get_sp_access_token(client_id, client_credential, tenant_name, scopes):
    logging.info('Attempting to obtain an access token...')
    
    result = None
    app = ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_credential,
        authority=f"https://login.microsoftonline.com/{tenant_name}",
        verify=False
    )
    if not result:
        logging.info('No suitable token exists in cache. Obtaining a new one...')
        result = app.acquire_token_for_client(scopes=scopes)
        
    if "access_token" in result:
        logging.info('Access token successfully acquired')
        return result['access_token']
    else:
        logging.error('Unable to obtain access token')
        logging.error(f"Error was: {result['error']}")
        logging.error(f"Error description was: {result['error_description']}")
        logging.error(f"Error correlation_id was: {result['correlation_id']}")
        raise Exception('Failed to obtain access token')


def main():

    # Setup logging
    try:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
    except:
        logging.error('Failed to setup logging: ', exc_info=True)

    # Setup non-sensitive variables
    API_VERSION = "2023-12-01-preview"
    #DEPLOYMENT_NAME = {{YOUR_MODEL_DEPLOYMENT_NAME}}
    #AZURE_OPENAI_ENDPOINT = {{YOUR_AZURE_OPENAI_SERVICE_URL}}
    DEPLOYMENT_NAME = "test"
    AZURE_OPENAI_ENDPOINT = "openaimf.openai.azure.com"

    # Use dotenv library to load sensitive environmental variables from .secret file.
    # The variables loaded include AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, and AZURE_TENANT_ID.
    # These variables are used to obtain an access token for the Azure OpenAI Service.
    try:
        load_dotenv('.secrets')
    except:
        logging.error('Failed to load env variables: ', exc_info=True)

    # Obtain an access token
    try:
        token = get_sp_access_token(
            client_id = os.getenv('AZURE_CLIENT_ID'),
            client_credential = os.getenv('AZURE_CLIENT_SECRET'),
            tenant_name = os.getenv('AZURE_TENANT_ID'),
            scopes=[
                "https://cognitiveservices.azure.com/.default"
            ]
        )
    except:
        logging.info('Failed to obtain access token: ', exc_info=True)

    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        response = requests.post(
            url = f"https://{AZURE_OPENAI_ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version={API_VERSION}",
            headers = headers,
            json = {
                "messages": [
                    {
                        "role": "user",
                        "content": "Tell me a bedtime story"
                    }
                ],
                "max_tokens": 100
            },
        )
        print(json.loads(response.text)['choices'][0]['message']['content'])
    except:
        logging.error('Failed to inference: ', exc_info=True)


if __name__ == "__main__":
    main()
