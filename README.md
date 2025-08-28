<img width="1920" height="954" alt="image" src="https://github.com/user-attachments/assets/8da72dbb-d807-4dff-9844-fe4111aa4c65" />


# AI Medical Assistant  

AI Medical Assistant is a smart and interactive chatbot designed to provide **general medical guidance** using advanced AI models (powered by Groq).  
It gives structured responses in multiple steps, making it easy for users to understand their condition and take basic precautionary measures.  

⚠️ **Disclaimer:** This app provides *general medical information only*. It is **not a substitute** for professional medical advice, diagnosis, treatment, or emergency services. Always consult a doctor for serious health issues.  

---

## 🚀 Features
- 🧾 Stepwise medical guidance:
  1. Summary of the condition  
  2. Common causes  
  3. Safe home remedies  
  4. Prevention tips  
  5. Medicine suggestion  
  6. Doctor visit advice  

- 🎛️ Sidebar controls for:
  - API key input  
  - Temperature & token settings  
  - Clear chat option  
  - Download chat history  

- 💬 Interactive conversational interface  
- 📂 Secure local history storage  

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit  
- **Backend:** Python, LangChain, Groq API  
- **Environment:** `.env` for API keys  

---

Installation

Clone this repo:

git clone https://github.com/bushra-genai/Medical-AI-Assistant


Create a virtual environment and install dependencies:

pip install -r requirements.txt


Create a .env file in the project root with your API keys:

OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here

Usage

Run the app with:

streamlit run app.py


The app will open in your browser (default: http://localhost:8501
).


🔑 API Key Requirement

This app requires a Groq API key to work.

Get your free API key from Groq Console
.

Enter the key in the sidebar of the app under "API Key".

Your key will only be used locally in your session (not stored).

⚠️ Note: The developer’s API key is not shared.
Each user must provide their own Groq API key.


Developed By

Bushra Sarwar

License

This project is licensed under the MIT License — free to use, modify, and share.
