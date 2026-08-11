Enterprise RAG & MCP Pipeline
A secure, agentic Retrieval-Augmented Generation (RAG) and Model Context Protocol (MCP) pipeline designed for automated technical troubleshooting. This project integrates Amazon Bedrock (Nova Lite) for intelligence, FastMCP for secure tool orchestration, and an Amazon S3 enterprise repository for ground-truth documentation storage.  
MD
+ 1

🏗️ Architecture & Component Flow
Plaintext
[ User / Chat Client (client.py) ] 
       │ (Multi-turn Prompt & History)
       ▼
[ Amazon Bedrock (Nova Lite) ] ──(Tool Request)──► [ FastMCP Server (server.py) ]
       ▲                                                        │
       └───────────────(Retrieved Context / Tool Result)────────┘
                                                                │ (S3 API Call)
                                                                ▼
                                                   [ Secure S3 Bucket Repository ]
Client (client.py): Manages the interactive multi-turn conversation loop, maintains state history, and handles agentic tool-calling payloads required by Amazon Bedrock.  
MD

Server (server.py): A high-performance FastMCP server exposing secure enterprise data tools (e.g., retrieving technical runbooks directly from cloud storage).  
MD

Data Repository (AWS S3): Hosts verified markdown troubleshooting runbooks (e.g., payment-gateway-v2.md), ensuring model responses are grounded in authoritative documentation.  
MD

Intelligence Layer (Amazon Bedrock): Utilizes the us.amazon.nova-lite-v1:0 foundation model to parse user queries, invoke tools dynamically, and synthesize accurate technical solutions.  
MD

📂 Repository Structure
Plaintext
enterprise-rag-mcp-pipeline/
│
├── rag-agent/
│   └── client.py          # Multi-turn interactive chat agent and Bedrock handler
├── mcp-server/
│   └── server.py          # FastMCP server handling secure S3 document retrieval
└── README.md              # Project documentation and setup guide
⚙️ Prerequisites
Python 3.10+

AWS CLI configured with active credentials and permissions for:

s3:GetObject / s3:ListBucket

bedrock:InvokeModel

Amazon Bedrock Access: Model access enabled for Amazon Nova Lite (us.amazon.nova-lite-v1:0) in your target region (us-east-1).

🚀 Installation & Setup
1. Clone & Set Up the Environment
Bash
git clone https://github.com/your-username/enterprise-rag-mcp-pipeline.git
cd enterprise-rag-mcp-pipeline

# Create and activate virtual environment
python -m venv venv
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
# On macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install boto3 fastmcp
2. Configure AWS Credentials
Ensure your environment can authenticate with AWS:

Bash
aws configure
(Verify your default region matches your Bedrock and S3 resource deployment, e.g., us-east-1).

3. Running the Pipeline
Start the MCP Server:
Ensure your FastMCP server is active to handle inbound tool execution requests from the client.

Bash
python mcp-server/server.py
Launch the Interactive Chat Client:
Open a separate terminal window, activate your virtual environment, and start the agent loop:

Bash
cd rag-agent
python client.py
💡 Example Usage Session
Plaintext
=== Enterprise RAG MCP Agent Initialized ===
Type your questions below. Type 'exit' or 'quit' to end the session.

>> How do I fix 504 Gateway Timeouts in Payment Gateway V2?

User: How do I fix 504 Gateway Timeouts in Payment Gateway V2?
[Agent executing MCP tool 'search_internal_docs' with args: {'query': '504 Gateway Timeouts in Payment Gateway V2'}]

Assistant:
Based on the retrieved runbook, a 504 Gateway Timeout in Payment Gateway V2 can be resolved by:
1. **Upstream Acquirer Latency**: Increase API Gateway timeout from 30s to 45s.
2. **Database Connection Pool Exhaustion**: Scale up RDS Aurora or tune connection pool size (minimum: 50, maximum: 200) in `application.yml`.
3. **Lambda Cold Starts**: Enable provisioned concurrency for critical transaction processing functions.
🛡️ Key Features & Engineering Highlights
Strict Tool-Calling Architecture: Fully complies with Amazon Bedrock’s converse API schema requirements, ensuring seamless payload formatting between user prompts, model tool requests, and tool results.  
MD

Stateful Multi-Turn Memory: Preserves message history across interactive sessions for seamless context-aware troubleshooting.  
MD

Cloud-Native Grounding: Eliminates hallucinations by fetching live markdown runbooks directly from secure S3 object storage during runtime.  
MD