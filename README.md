MindMirror is a Streamlit-based mental health assistant that engages users in a 5-step reflective conversation powered by Groq’s LLaMA 3 model and the GoEmotions dataset. It dynamically analyzes responses, retrieves emotional context, and asks empathetic follow-up questions to guide deeper self-reflection.

✨ Key Features:

🧠 Emotion-Aware Conversations: Uses retrieval-augmented generation (RAG) with GoEmotions dataset to add emotional intelligence to conversations.

💬 Adaptive Question Flow: AI dynamically adjusts follow-up questions based on user responses (not fixed prompts).

📖 Conversation Memory: Maintains session history for a natural chat flow.

❤️ Compassionate Reflection: At the end of 5 questions, generates a thoughtful summary of the user’s emotional state with supportive advice.

⚡ Groq-powered LLaMA 3 integration for ultra-fast response times.

Ideal for students, professionals, or anyone wanting structured self-reflection through short, AI-assisted check-ins.

🛠️ Tech Stack

Streamlit
 – Interactive frontend UI

Pandas
 – Data processing

GoEmotions Dataset
 – Emotional grounding

Groq
 – LLaMA 3 inference API

📂 Project Structure
mindmirror/

│── app.py                   # Main Streamlit app

│── go_emotions_dataset.csv  # GoEmotions dataset

│── requirements.txt         # Python dependencies

│── README.md                # Project documentation

💡 Example Conversation Flow

AI: How have you been feeling emotionally over the past few days?  

User: Tired and frustrated.  

AI: Do you think the tiredness is amplifying your frustration, or is it more about something deeper?  

User: More about deeper issues…  

... (5-step conversation continues)  

✅ AI: Based on your reflections, it sounds like you’re dealing with [emotion summary].  
Here are some supportive thoughts: [...]

⚠️ Disclaimer

MindMirror is not a medical tool.
It is intended for self-reflection and awareness only and should not replace professional mental health support.
If you are experiencing distress, please seek help from a qualified professional or call your local mental health helpline. ❤️
