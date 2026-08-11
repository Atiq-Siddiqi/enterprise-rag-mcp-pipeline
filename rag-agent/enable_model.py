import boto3
import json
from botocore.exceptions import ClientError

# Initialize Bedrock client in your target deployment region
client = boto3.client('bedrock', region_name='us-east-1')

# 1. Submit Use Case Details (Required once per AWS account)
form_data = {
    "companyName": "Enterprise Solutions",
    "companyWebsite": "https://example.com",
    "intendedUsers": "50",
    "industryOption": "Technology",
    "useCases": "Internal RAG and MCP server integration development for automated technical document retrieval workflows."
}

try:
    client.put_use_case_for_model_access(formData=json.dumps(form_data))
    print("✓ Successfully submitted Bedrock model use case details!")
except Exception as e:
    print(f"ℹ Note on use case submission: {e}")

# 2. Automatically Fetch Offers and Create Agreements for Project Models
models_to_enable = [
    "us.amazon.nova-lite-v1:0"
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
            print(f"ℹ No active offers found to bind for {model_id} (Model may be natively available)")
    except ClientError as e:
        print(f"Agreement status for {model_id}: {e.response['Error']['Message']}")
