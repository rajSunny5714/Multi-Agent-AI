🤖 Multi-Agent AI Research Assistant
An intelligent Multi-Agent AI Research Assistant that automates the complete research workflow using specialized AI agents.

The system searches the web, analyzes information, verifies facts, summarizes findings, and generates structured research reports with references.

🚀 Features
🔍 Intelligent Web Research
🤖 Multi-Agent Architecture
🧠 LLM-powered Analysis
📑 Automatic Report Generation
📚 Source Citation Support
⚡ Groq LLM Integration
🌐 Tavily Search API
💬 Interactive Chainlit Interface
🔐 User API Key Support (Fallback when demo quota is exhausted)
🏗️ Architecture
                User Query
                     │
                     ▼
             Research Coordinator
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
 Search Agent   Analysis Agent   Verification Agent
      │              │              │
      └──────────────┼──────────────┘
                     ▼
            Report Generation Agent
                     │
                     ▼
             Final Research Report


User Topic
    |
    ↓
Search Agent
    |
    ↓
Reader Agent
    |
    ↓
Writer Agent
    |
    ↓
Critic Agent
    |
    ↓
PDF Report





🛠 Tech Stack
Backend
Python
LangChain
Chainlit
Groq API
Tavily Search API
AI
Llama 3
Prompt Engineering
Agentic AI
Multi-Agent Workflow
Tools
Git
GitHub
VS Code
📂 Project Structure
multi-agent-ai-research-assistant/
│
├── agents/
├── tools/
├── prompts/
├── chains/
├── app.py
├── requirements.txt
├── README.md
└── .env.example
🔑 API Key Handling
The application includes a production-friendly API fallback.

Uses the developer demo API by default.
If the demo API quota is exhausted, users are prompted to enter their own free Groq API key.
No source code modifications are required.
📸 Demo
Add screenshots or GIFs here.

🎯 Future Improvements
PDF Export
Research History
Multiple LLM Support
Multi-Source Comparison
RAG Integration
Streaming Responses
Dark Mode
Docker Support
Cloud Deployment
🤝 Contributing
Contributions are welcome.

Feel free to fork the repository and submit pull requests.

📄 License
MIT License
