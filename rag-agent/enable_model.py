import boto3
import json
from botocore.exceptions import ClientError

client = boto3.client('bedrock', region_name='us-east-1')

# 1. Submit Use Case Details
form_data = {
    "companyName": "Internal Dev",
    "companyWebsite": "https://example.com",
    "intendedUsers": "0",
    "industryOption": "Technology",
    "useCases": "Internal RAG and MCP server integration development for documentation workflows."
}

try:
    client.put_use_case_for_model_access(formData=json.dumps(form_data))
    print("✓ Successfully submitted Bedrock model use case details!")
except Exception as e:
    print(f"Note on use case submission: {e}")

# 2. Automatically Fetch Offers and Create Agreements for Anthropic Models
models_to_enable = [
    "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "anthropic.claude-sonnet-4-20250514-v1:0"
]

for model_id in models_to_enable:
    try:
        offers_response = client.list_foundation_model_agreement_offers(modelId=model_id)
        offers = offers_response.get('offers', [])
        if offers:
            offer_token = offers[0]['offerToken']
            client.create_foundation_model_agreement(modelId=model_id, offerToken=offer_token)
            print(f"✓ Agreement created successfully for: {model_id}")
        else:
            print(f"ℹ No active offers found to bind for {model_id}")
    except ClientError as e:
        print(f"Agreement status for {model_id}: {e.response['Error']['Message']}")