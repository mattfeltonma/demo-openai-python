import logging
import sys
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential

def main():

    # Setup variables
    API_VERSION = "2023-12-01-preview"
    DEPLOYMENT_NAME = {{YOUR_MODEL_DEPLOYMENT_NAME}}
    AZURE_OPENAI_ENDPOINT = {{YOUR_AZURE_OPENAI_SERVICE_URL}}

    # If using a user-assigned managed identity you must set the client id
    MANAGED_IDENTITY_CLIENT_ID ={{YOUR_MANAGED_IDENTITY_CLIENT_ID}}


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
        token_provider = DefaultAzureCredential(
            managed_identity_client_id=MANAGED_IDENTITY_CLIENT_ID
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
