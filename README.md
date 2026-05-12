# HR Policy RAG Assistant

This project implements a Retrieval-Augmented Generation (RAG) chatbot for HR policies at InnoTech Solutions.  
Employees can ask HR-related questions, and the assistant retrieves relevant policy documents from ChromaDB before generating grounded answers using OpenAI GPT models.  

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Set your API key: `export OPENAI_API_KEY=your_key_here`
3. Run the assistant: `python hr_policy_rag.py`
