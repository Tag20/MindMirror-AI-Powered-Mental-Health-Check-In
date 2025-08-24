import streamlit as st
import pandas as pd
import json
import difflib #Used to compare sequence - string matching beween User Input and Dataset
from groq import Groq

# --- App Setup ---
st.set_page_config(layout="wide")

Groq_API = "Replace with you API"
client = Groq(
    api_key= Groq_API,
)

# --- Load and Process Dataset ---
@st.cache_data(show_spinner=False)
def load_emotion_data():
    df = pd.read_csv("go_emotions_dataset.csv")
    emotion_labels = df.columns[3:]
    emotion_entries = []
    for _, row in df.iterrows():
        emotions = [emotion for emotion in emotion_labels if row[emotion] == 1]
        if emotions:
            emotion_entries.append({
                "text": row["text"],
                "emotions": emotions
            })
    return emotion_entries

emotion_knowledge_base = load_emotion_data()

# --- Retrieval ---
def retrieve_emotion_insights(user_text, top_k=3):
    texts = [entry["text"] for entry in emotion_knowledge_base]
    matches = difflib.get_close_matches(user_text, texts, n=top_k, cutoff=0.1) # Explained in Import
    return [entry for entry in emotion_knowledge_base if entry["text"] in matches]

# --- Session State ---
if "mh_step" not in st.session_state:
    st.session_state.mh_step = 0
    st.session_state.mh_answers = []
    st.session_state.mh_finished = False
    st.session_state.chat_history = []
if "current_question" not in st.session_state:
    st.session_state.current_question = None

# --- Embedded Conversation Example ---
example_convo = [
    {"user": "Tired, Fustrated and Hungry since today is my fast haha", "assistant": "Do you think the hunger is amplifying your emotions, or is it more about something else that’s been building up lately?"},
    {"user": "Yeah, I am bugged up that I scored less in an exam because I took it too lightly when I could have easily scored more if I had just worked on it. Because of over confidence I lost my touch...", "assistant": "What do you think your overconfidence came from — was it a past success, a distraction, or maybe a belief that it wouldn’t be that hard?"},
    {"user": "Yeah it was past success, I just got the highest placement in clg and since it was my last sem and my last exam I had like 0 motivation....", "assistant": "Now that you’ve had that wake-up call — how are you planning to carry this new mindset forward?"},
    {"user": "Yes I am", "assistant": "On days when motivation dips again, what’s something you can remind yourself of — a thought, a goal, a feeling — that’ll help you refocus and not fall into the same pattern again?"},
    {"user": "Idk maybe a minor setback always reminds you of what you are capable of and what you can achieve if you work with your full potential"}
]

# --- Get Next Question with Deep Emotional Reasoning ---
def get_next_question_with_rag(answers):
    last_answer = answers[-1]
    retrieved = retrieve_emotion_insights(last_answer)
    context = "\n".join([f"- \"{r['text']}\" → {', '.join(r['emotions'])}" for r in retrieved])
    example_str = "\n".join([f"User: {item['user']}\nAssistant: {item['assistant']}" for item in example_convo if 'assistant' in item])

    prompt = [
        {
            "role": "system",
            "content": (
                "You are a compassionate and thoughtful mental health assistant. "
                "You ask a series of 5 deep, emotionally intelligent follow-up questions to help the user reflect. "
                "Use context from past answers and emotional nuance."
                f"\n\nHere are past emotional examples for guidance:\n{context}"
                f"\n\nHere is a sample of how the conversation should look:\n{example_str}"
            )
        },
        {
            "role": "user",
            "content": f"The user just said:\n\"{last_answer}\"\n\nAsk the next thoughtful and emotion-driven question."
        }
    ]

    response = client.chat.completions.create(
        messages=prompt,
        model="llama3-70b-8192",
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# --- UI ---
st.title("🧠 Mental Health Check-In")
st.markdown("Answer 5 thoughtful questions and receive a reflection on your emotional state.")

# --- Show past conversation in proper flow ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.mh_step < 5 and not st.session_state.mh_finished:
    if st.session_state.current_question is None:
        if st.session_state.mh_step == 0:
            question = "How have you been feeling emotionally over the past few days?"
        else:
            question = get_next_question_with_rag(st.session_state.mh_answers)
        st.session_state.current_question = question
        st.session_state.chat_history.append({"role": "assistant", "content": question})
        st.rerun()

    question = st.session_state.current_question
    user_input = st.chat_input("Your response...")

    if user_input:
        st.session_state.mh_answers.append(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.mh_step += 1
        st.session_state.current_question = None
        st.rerun()

elif st.session_state.mh_step == 5 and not st.session_state.mh_finished:
    with st.spinner("Analyzing your responses..."):
        all_retrieved = [retrieve_emotion_insights(ans) for ans in st.session_state.mh_answers]
        flat = [item for sublist in all_retrieved for item in sublist]
        context = "\n".join([f"- \"{item['text']}\" → {', '.join(item['emotions'])}" for item in flat])

        prompt = [
            {"role": "system", "content": f"You are a compassionate assistant. Based on these examples:\n{context}"},
            {"role": "user", "content": f"The user answered:\n{json.dumps(st.session_state.mh_answers)}\nSummarize their emotional state and offer kind support or advice."}
        ]

        try:
            response = client.chat.completions.create(
                messages=prompt,
                model="llama3-70b-8192",
                temperature=0.3
            )
            summary = response.choices[0].message.content.strip()
            st.session_state.chat_history.append({"role": "user", "content": "That’s all my answers."})
            st.session_state.chat_history.append({"role": "assistant", "content": summary})
            st.session_state.mh_finished = True
            st.rerun()
        except Exception as e:
            st.error(f"Something went wrong: {e}")

elif st.session_state.mh_finished:
    with st.chat_message("assistant"):
        st.markdown("✅ You're all set! If you'd like to restart the session, click below.")

    if st.button("🔁 Restart"):
        st.session_state.mh_step = 0
        st.session_state.mh_answers = []
        st.session_state.mh_finished = False
        st.session_state.chat_history = []
        st.session_state.current_question = None
        st.rerun()