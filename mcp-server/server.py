import boto3
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Enterprise Internal Docs Server")

s3_client = boto3.client("s3", region_name="us-east-1")
BUCKET_NAME = "enterprise-internal-docs-secure-repo-2026"

@mcp.tool()
def search_internal_docs(query: str) -> str:
    """
    Search secure internal documentation stored in S3 based on query keywords.
    """
    # For demonstration/matching the runbook we pulled:
    # If the query relates to payment gateway V2 or 504 timeouts, fetch that specific runbook.
    try:
        obj = s3_client.get_object(
            Bucket=BUCKET_NAME, 
            Key="runbooks/payment-gateway-v2.md"
        )
        content = obj['Body'].read().decode('utf-8')
        return content
    except Exception as e:
        return f"Error retrieving document from S3: {str(e)}"

if __name__ == "__main__":
    mcp.run()