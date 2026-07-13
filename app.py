import os
import time
import streamlit as st
import pandas as pd
import plotly.express as px

from notes_pdf import create_notes_pdf
from login import login, signup
from database import save_result, load_results
from pdf_reader import extract_text
from quiz_generator import generate_quiz
from pdf_report import create_pdf
from chatbot import ask_pdf
from notes_generator import generate_notes

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Academix",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# CSS
# --------------------------------------------------

def load_css():
    if os.path.exists("style.css"):
        with open("style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

load_css()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "logged_in": False,
    "username": "",
    "messages": [],
    "quiz": None,
    "pdf_text": "",
    "score": 0,
    "total": 0,
    "start_time": None,
    "submit_quiz": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

os.makedirs("uploads", exist_ok=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.image(
        "assets/logo.jpeg",
        width=200
    )

with col2:

    

    st.markdown("""
    <h1 style='text-align:center;color:#5c174e;'>
    Academix
    </h1>

    <h4 style='text-align:center;color:#8f3d7e;'>
    Your AI Powered Study Companion
    </h4>
    
    <h5 style='text-align:center;color:#b076a4;'>
    Learn • Practice • Improve
    </h5>
    """, unsafe_allow_html=True)

st.divider()

# --------------------------------------------------
# LOGIN
# --------------------------------------------------

if not st.session_state.logged_in:

    st.title("🔐 Login")

    menu = st.radio(
        "Choose",
        ["Login", "Signup"]
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if menu == "Signup":

        if st.button("Create Account"):

            if signup(username, password):

                st.success("Account created successfully!")

            else:

                st.error("Username already exists.")

    else:

        if st.button("Login"):

            if login(username, password):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success(f"Welcome {username} 👋")

                st.rerun()

            else:

                st.error("Invalid Username or Password")

    st.stop()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

import base64

def sidebar_logo():

    with open("assets/logo.jpeg", "rb") as f:

        data = base64.b64encode(
            f.read()
        ).decode()


    st.sidebar.markdown(
        f"""
        <div style="
        text-align:center;
        margin-bottom:20px;
        ">

        <img src="data:image/png;base64,{data}"
        width="120">

        </div>
        """,
        unsafe_allow_html=True
    )


sidebar_logo()

st.sidebar.markdown(
"""
<h2 style="
text-align:center;
color:white;
">
📚 Academix Menu
</h2>
""",
unsafe_allow_html=True
)

option = st.sidebar.radio(
    "",
    [
        "🏠 Home",
        "📝 Create Quiz",
        "📚 AI Notes",
        "📊 Dashboard",
        "💬 AI Chatbot"
    ]
)

st.sidebar.success(
    f"👋 Hello {st.session_state.username}"
)

if st.sidebar.button("🚪 Logout"):

    for key in [
        "quiz",
        "pdf_text",
        "messages"
    ]:

        if key in st.session_state:
            del st.session_state[key]

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()

# --------------------------------------------------
# HOME
# --------------------------------------------------

if option == "🏠 Home":

    st.header("Welcome to Academix 🚀")

    st.markdown("""

### 📄 Upload PDFs

Upload your notes or books.

---

### 🤖 AI Quiz

Generate MCQs automatically.

---

### 📊 Dashboard

Track your learning progress.

---

### 💬 AI Chatbot

Ask questions from your uploaded PDF.

---

### 📚 AI Notes

Generate concise study notes instantly.

""")

    st.info(
        "Use the sidebar to begin."
    )
# --------------------------------------------------
# CREATE QUIZ
# --------------------------------------------------

elif option == "📝 Create Quiz":

    st.header("📝 Create Quiz From PDF")

    uploaded_file = st.file_uploader(
        "Upload your study material PDF",
        type=["pdf"]
    )


    if uploaded_file:

        file_path = os.path.join(
            "uploads",
            uploaded_file.name
        )


        with open(file_path, "wb") as f:

            f.write(
                uploaded_file.getbuffer()
            )


        st.success(
            "PDF Uploaded Successfully ✅"
        )


        # Extract PDF text

        text = extract_text(file_path)


        if text is None or not text.strip():

            st.error(
                "Could not extract text from this PDF."
            )

            st.stop()


        # Save PDF text for chatbot and notes

        st.session_state.pdf_text = text


        # Reset chat for new PDF

        st.session_state.messages = []


        st.subheader(
            "📖 PDF Preview"
        )


        st.text_area(
            "Extracted Content",
            text[:1500],
            height=250
        )


        st.divider()


        # ------------------------------
        # TIMER
        # ------------------------------

        if st.session_state.start_time is None:

            st.session_state.start_time = time.time()


        TOTAL_TIME = 15 * 60


        elapsed = int(
            time.time()
            -
            st.session_state.start_time
        )


        remaining = TOTAL_TIME - elapsed


        if remaining <= 0:

            st.error(
                "⏰ Time finished! Submit your quiz."
            )

            st.session_state.submit_quiz = True


        else:

            mins = remaining // 60

            secs = remaining % 60


            st.warning(
                f"⏳ Time Left: {mins:02d}:{secs:02d}"
            )



        # ------------------------------
        # GENERATE QUIZ
        # ------------------------------

        if st.button("🤖 Generate Quiz"):


            with st.spinner(
                "Creating your quiz..."
            ):

                try:

                    st.session_state.quiz = generate_quiz(
                        text
                    )


                except Exception as e:

                    st.error(
                        "Quiz generation failed."
                    )

                    st.exception(e)

                    st.stop()



        # ------------------------------
        # DISPLAY QUIZ
        # ------------------------------

        if st.session_state.quiz:


            quiz = st.session_state.quiz


            st.success(
                "Quiz Ready 🎉"
            )


            answers = {}


            st.divider()


            for i, q in enumerate(quiz):


                st.subheader(
                    f"Question {i+1}"
                )


                answers[i] = st.radio(

                    q["question"],

                    q["options"],

                    index=None,

                    key=f"answer_{i}"

                )



            st.divider()



            submit = st.button(
                "✅ Submit Quiz"
            )


            if submit or st.session_state.submit_quiz:


                unanswered = [

                    i+1

                    for i, ans in answers.items()

                    if ans is None

                ]


                if unanswered:

                    st.warning(
                        "Please answer all questions: "
                        +
                        ", ".join(
                            map(
                                str,
                                unanswered
                            )
                        )
                    )

                    st.stop()



                score = 0



                st.header(
                    "📋 Result Analysis"
                )



                for i, q in enumerate(quiz):


                    if answers[i] == q["answer"]:


                        score += 1


                        st.success(
                            f"✅ Question {i+1} Correct"
                        )


                    else:


                        st.error(
                            f"❌ Question {i+1} Wrong"
                        )


                        st.write(
                            f"Correct Answer: **{q['answer']}**"
                        )


                        if "explanation" in q:

                            st.info(
                                q["explanation"]
                            )



                percentage = round(

                    score / len(quiz) * 100,

                    2

                )



                col1, col2 = st.columns(2)



                col1.metric(

                    "Score",

                    f"{score}/{len(quiz)}"

                )


                col2.metric(

                    "Percentage",

                    f"{percentage}%"

                )



                # Save database

                save_result(
                    st.session_state.username,
                    score,
                    len(quiz)
                )



                # Create PDF report

                pdf_file = create_pdf(

                    st.session_state.username,

                    score,

                    len(quiz),

                    quiz,

                    answers

                )


                with open(pdf_file, "rb") as file:


                    st.download_button(

                        "📄 Download Result PDF",

                        data=file,

                        file_name=pdf_file,

                        mime="application/pdf"

                    )



                # Dashboard data

                st.session_state.score = score

                st.session_state.total = len(quiz)



                # Reset timer

                st.session_state.start_time = None

                st.session_state.submit_quiz = False




            if st.button(
                "🔄 Generate New Quiz"
            ):

                st.session_state.quiz = None

                st.session_state.start_time = None

                st.rerun()
# --------------------------------------------------
# AI NOTES
# --------------------------------------------------

elif option == "📚 AI Notes":

    st.header("📚 AI Generated Study Notes")


    if not st.session_state.pdf_text:


        st.warning(
            "Please upload a PDF first from Create Quiz."
        )


    else:


        if st.button("✨ Generate Notes"):


            with st.spinner(
                "Creating notes..."
            ):


                try:

                    notes = generate_notes(
                        st.session_state.pdf_text
                    )

                    st.session_state.notes = notes


                except Exception as e:

                    st.error(
                        "Notes generation failed."
                    )

                    st.exception(e)



        if "notes" in st.session_state:


            st.markdown(
                st.session_state.notes
            )


            pdf_file = create_notes_pdf(
                st.session_state.notes
            )
            with open(pdf_file, "rb") as f:
                st.download_button(
                    "📄 Download Notes PDF",
                    
                    data=f,
                    file_name="Academix_Study_Notes.pdf",
                    mime="application/pdf"
                )



# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

elif option == "📊 Dashboard":


    st.header(
        "📊 Learning Dashboard"
    )


    results = load_results()



    if not results:


        st.info(
            "Complete a quiz to see progress."
        )


    else:


        user_results = [

            r for r in results

            if r.get("username") == st.session_state.username
        ]


        if not user_results:


            st.info(
                "No quiz attempts yet."
            )


        else:


            latest = user_results[-1]


            score = latest["score"]

            total = latest["total"]

            percentage = latest["percentage"]



            col1, col2, col3 = st.columns(3)


            col1.metric(

                "Latest Score",

                f"{score}/{total}"

            )


            col2.metric(

                "Percentage",

                f"{percentage}%"

            )


            col3.metric(

                "Attempts",

                len(user_results)

            )



            st.divider()



            df = pd.DataFrame(user_results)



            fig = px.line(

                df,

                x="date",

                y="percentage",

                markers=True,

                title="Progress Tracking"

            )


            st.plotly_chart(

                fig,

                use_container_width=True

            )



            st.success(
                "Keep improving 🚀"
            )




# --------------------------------------------------
# AI CHATBOT
# --------------------------------------------------

elif option == "💬 AI Chatbot":


    st.header(
        "💬 Chat With Your PDF"
    )


    if not st.session_state.pdf_text:


        st.warning(
            "Upload a PDF first."
        )


    else:


        # Previous messages

        for msg in st.session_state.messages:


            with st.chat_message(
                msg["role"]
            ):


                st.write(
                    msg["content"]
                )



        question = st.chat_input(

            "Ask something about your PDF..."

        )



        if question:


            st.session_state.messages.append(

                {

                    "role":"user",

                    "content":question

                }

            )


            with st.chat_message(
                "user"
            ):

                st.write(
                    question
                )



            with st.spinner(
                "🤖 Thinking..."
            ):


                answer = ask_pdf(

                    question,

                    st.session_state.pdf_text

                )



            st.session_state.messages.append(

                {

                    "role":"assistant",

                    "content":answer

                }

            )



            with st.chat_message(
                "assistant"
            ):


                st.write(
                    answer
                )



        if st.button(
            "🗑 Clear Chat"
        ):


            st.session_state.messages = []


            st.rerun()




# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()


st.markdown(
"""
<div style="
text-align:center;
padding:20px;
color:gray;
">

<h3 style="color:#690955;">
📚 Academix
</h3>

<p>
AI Powered Study Companion
</p>

<p>
Made with ❤️ by <b>Gargi</b>
</p>

<p>
Python • Streamlit • Groq AI • Plotly
</p>

</div>
""",
unsafe_allow_html=True
)





