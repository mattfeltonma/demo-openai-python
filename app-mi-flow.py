import logging
import sys
import openai
from azure.identity import DefaultAzureCredential

def main():

    # Setup variables
    CLIENT_ID ={{YOUR_CLIENT_ID}}
    DEPLOYMENT_NAME = {{YOUR_MODEL_DEPLOYMENT_NAME}}
    OPENAI_BASE={{YOUR_AZURE_OPENAI_SERVICE_URL}}

    # Setup logging
    try:
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
    except:
        logging.error('Failed to setup logging: ', exc_info=True)

    try:
        # Obtain an access token
        logging.info('Attempting to obtain an access token...')
        credential = DefaultAzureCredential(managed_identity_client_id=CLIENT_ID)
        token = credential.get_token("https://cognitiveservices.azure.com/.default")

    except:
        logging.error('Failed to obtain access token: ', exc_info=True)

    try:
        # Setup OpenAI Variables
        openai.api_type = "azure_ad"
        openai.api_base = OPENAI_BASE
        openai.api_key = token.token
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
        logging.error('Failed to inference: ', exc_info=True)


if __name__ == "__main__":
    main()
