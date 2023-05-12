import logging
import sys
import os
import openai
from msal import ConfidentialClientApplication


def get_sp_access_token(client_id, client_credential, tenant_name, scopes):
    logging.info('Attempting to obtain an access token...')
    result = None
    print(tenant_name)
    app = ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_credential,
        authority=f"https://login.microsoftonline.com/{tenant_name}",
        verify=False
    )
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

    CLIENT_ID = {{YOUR_CLIENT_ID}}
    CLIENT_SECRET = {{YOUR_CLIENT_SECRET}}
    TENANT_ID = {{YOUR_TENANT_ID}}
    DEPLOYMENT_NAME = {{YOUR_MODEL_DEPLOYMENT_NAME}}
    OPENAI_BASE={{YOUR_AZURE_OPENAI_SERVICE_URL}}

    # Setup logging
    try:
        logging.basicConfig(
            level=logging.ERROR,
            format='%asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
    except:
        logging.error('Failed to setup logging: ', exc_info=True)

    try:
        # Obtain an access token
        token = get_sp_access_token(
            client_id=CLIENT_ID,
            client_credential=CLIENT_SECRET,
            tenant_name=TENANT_ID,
            scopes="https://cognitiveservices.azure.com/.default"
        )
    except:
        logging.error('Failed to obtain access token: ', exc_info=True)

    try:
        # Setup OpenAI Variables
        openai.api_type = "azure_ad"
        openai.api_base = OPENAI_BASE
        openai.api_key = token
        openai.api_version = "2023-03-15-preview"

        response = openai.ChatCompletion.create(
            engine=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "user",
                   "content": "Say this is a test"
                }
            ]
        )
        print(response.choices)

    except:
        logging.error('Failed to summarize file: ', exc_info=True)


if __name__ == "__main__":
    main()
