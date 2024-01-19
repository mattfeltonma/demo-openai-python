import logging
import sys
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI
from dotenv import load_dotenv

def main():

    # Setup logging
    try:
        logging.basicConfig(
            level=logging.ERROR,
            format='%asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
    except:
        logging.error('Failed to setup logging: ', exc_info=True)
        
    # Setup non-sensitive variables
    API_VERSION = "2023-12-01-preview"
    DEPLOYMENT_NAME = {{YOUR_MODEL_DEPLOYMENT_NAME}}
    AZURE_OPENAI_ENDPOINT = {{YOUR_AZURE_OPENAI_SERVICE_URL}}

    # Use dotenv library to load sensitive environmental variables from .secret file.
    # The variables loaded include AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, and AZURE_TENANT_ID.
    # These variables are used to obtain an access token for the Azure OpenAI Service.
    try:
        load_dotenv('.secrets')
    except:
        logging.error('Failed to load env variables: ', exc_info=True)

    # Obtain an access token
    try:
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(),
            "https://cognitiveservices.azure.com/.default"
        )
    except:
        logging.error('Failed to obtain access token: ', exc_info=True)

    # Perform a chat completion
    try:
        client = AzureOpenAI(
            api_version = API_VERSION,
            azure_endpoint= AZURE_OPENAI_ENDPOINT,
            azure_ad_token_provider=token_provider
        )
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "user",
                   "content": "Tell me a bedtime story"
                }
            ],
            max_tokens=100
        )
        print(response.choices[0].message.content)
        
    except:
        logging.error('Failed chat completion: ', exc_info=True)


if __name__ == "__main__":
    main()
