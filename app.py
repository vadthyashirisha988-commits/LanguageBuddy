import streamlit as st
import random

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Language Buddy",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }
.stApp { background: #f7f8fc; }
header { visibility: hidden; }
.block-container { padding: 0 5% 40px 5%; max-width: 1400px; }

.navbar { display:flex; justify-content:space-between; align-items:center; padding:22px 0; }
.logo { font-size:27px; font-weight:800; color:#4f46e5; }
.logo span { color:#111827; }
.nav-links { display:flex; gap:28px; align-items:center; }
.nav-item { color:#4b5563; font-size:15px; font-weight:600; }

.hero { background:linear-gradient(135deg,#eef2ff,#ffffff); border-radius:28px; padding:70px 60px; margin-top:20px; overflow:hidden; }
.hero-title { font-size:55px; line-height:1.08; font-weight:800; color:#111827; margin-bottom:20px; }
.hero-title span { color:#4f46e5; }
.hero-text { font-size:18px; color:#6b7280; max-width:700px; line-height:1.7; }

.card { background:white; border-radius:20px; padding:25px; border:1px solid #e5e7eb; box-shadow:0 8px 30px rgba(0,0,0,0.04); margin-bottom:20px; }
.card-title { font-size:20px; font-weight:700; color:#111827; }
.card-text { color:#6b7280; line-height:1.6; }

.dashboard-title { font-size:38px; font-weight:800; color:#111827; }
.stat { background:white; border-radius:18px; padding:24px; border:1px solid #e5e7eb; }
.stat-number { font-size:32px; font-weight:800; color:#4f46e5; }
.stat-label { color:#6b7280; }

.chat-user { background:#4f46e5; color:white; padding:14px 18px; border-radius:18px 18px 4px 18px; margin:10px 0 10px auto; max-width:70%; }
.chat-ai { background:#eef2ff; color:#1f2937; padding:14px 18px; border-radius:18px 18px 18px 4px; margin:10px 0; max-width:70%; }

.word { font-size:30px; font-weight:800; color:#4f46e5; }
.badge { background:#eef2ff; padding:18px; border-radius:15px; text-align:center; margin-bottom:10px; }
.score { font-size:30px; font-weight:800; color:#4f46e5; }

.footer { text-align:center; color:#9ca3af; padding:50px 0 20px; }

@media(max-width:768px) {
    .hero { padding:40px 25px; }
    .hero-title { font-size:38px; }
    .nav-links { display:none; }
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATE
# Existing features are preserved and new features are added.
# ---------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = "Learner"

if "email" not in st.session_state:
    st.session_state.email = ""

if "language" not in st.session_state:
    st.session_state.language = "English"

if "level" not in st.session_state:
    st.session_state.level = "Beginner"

if "messages" not in st.session_state:
    st.session_state.messages = []

# New features
if "saved_words" not in st.session_state:
    st.session_state.saved_words = []

if "learned_words" not in st.session_state:
    st.session_state.learned_words = 245

if "practice_sessions" not in st.session_state:
    st.session_state.practice_sessions = 18

if "quiz_correct" not in st.session_state:
    st.session_state.quiz_correct = 0

if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0

if "speaking_score" not in st.session_state:
    st.session_state.speaking_score = 78

if "overall_progress" not in st.session_state:
    st.session_state.overall_progress = 72

if "streak" not in st.session_state:
    st.session_state.streak = 7

if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = 15

if "goal_progress" not in st.session_state:
    st.session_state.goal_progress = 10

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------
vocabulary = [
    ("Confident", "Feeling sure about yourself", "She is confident while speaking English.", "Self-assured"),
    ("Improve", "To become better", "I want to improve my English.", "Develop"),
    ("Communication", "The process of sharing information", "Good communication is important.", "Interaction"),
    ("Practice", "Doing something repeatedly to improve", "Practice helps us become better.", "Training"),
    ("Fluent", "Able to speak smoothly and easily", "He is fluent in English.", "Articulate"),
    ("Curious", "Wanting to know or learn something", "She is curious about new technology.", "Inquisitive"),
    ("Accurate", "Correct and without mistakes", "Please give an accurate answer.", "Correct"),
    ("Express", "To communicate a thought or feeling", "She can express her ideas clearly.", "Communicate"),
    ("Opportunity", "A suitable chance to do something", "This internship is a great opportunity.", "Chance"),
    ("Achieve", "To successfully reach a goal", "She wants to achieve her dream.", "Accomplish")
]

quiz_questions = [
    ("What is the meaning of 'Confident'?", ["Feeling sure about yourself", "Feeling sleepy", "Feeling angry", "Feeling confused"], "Feeling sure about yourself"),
    ("What does 'Fluent' mean?", ["Unable to speak", "Speaking smoothly and easily", "Speaking very slowly", "Writing only"], "Speaking smoothly and easily"),
    ("What is a synonym of 'Improve'?", ["Develop", "Destroy", "Forget", "Stop"], "Develop"),
    ("What does 'Accurate' mean?", ["Wrong", "Correct", "Slow", "Difficult"], "Correct"),
    ("What is the meaning of 'Opportunity'?", ["A problem", "A suitable chance", "A mistake", "A lesson"], "A suitable chance")
]

scenarios = {
    "👋 Daily Conversation": "Hello! How are you today?",
    "🎓 College Conversation": "Hi! What are you studying in college?",
    "💼 Job Interview": "Tell me about yourself.",
    "✈️ Travel": "Where would you like to travel and why?",
    "🍽️ Restaurant": "What would you like to order?",
    "🛒 Shopping": "What are you looking for today?"
}

# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------
def go_to(page):
    st.session_state.page = page


def add_progress():
    st.session_state.practice_sessions += 1
    st.session_state.goal_progress = min(
        st.session_state.daily_goal,
        st.session_state.goal_progress + 1
    )
    st.session_state.overall_progress = min(
        100,
        st.session_state.overall_progress + 1
    )


def reset_progress():
    st.session_state.saved_words = []
    st.session_state.learned_words = 0
    st.session_state.practice_sessions = 0
    st.session_state.quiz_correct = 0
    st.session_state.quiz_total = 0
    st.session_state.speaking_score = 0
    st.session_state.overall_progress = 0
    st.session_state.streak = 0
    st.session_state.goal_progress = 0

# ---------------------------------------------------------
# NAVBAR
# ---------------------------------------------------------
st.markdown("""
<div class="navbar">
<div class="logo">🌐 Language<span>Buddy</span></div>
<div class="nav-links">
<div class="nav-item">Learn</div>
<div class="nav-item">Practice</div>
<div class="nav-item">Progress</div>
</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# HOME PAGE - original design + feature highlights
# =========================================================
if st.session_state.page == "Home":

    st.markdown("""
    <div class="hero">
        <div class="hero-title">
            Learn Languages.<br>
            <span>Speak With Confidence.</span>
        </div>
        <div class="hero-text">
            Language Buddy is your AI-powered language learning companion.
            Practice conversations, improve vocabulary, develop speaking skills,
            take quizzes, earn achievements, and track your progress in one simple platform.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <div style="font-size:35px;">💬</div>
        <div class="card-title">AI Conversation</div>
        <div class="card-text">Practice realistic conversations and improve your communication skills.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <div style="font-size:35px;">📚</div>
        <div class="card-title">Smart Vocabulary</div>
        <div class="card-text">Learn useful words with meanings, examples and synonyms.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <div style="font-size:35px;">🎤</div>
        <div class="card-title">Speaking Practice</div>
        <div class="card-text">Record your voice and practice speaking confidently.</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🚀 Start Learning", use_container_width=True):
            go_to("Sign Up")
            st.rerun()

    with col2:
        if st.button("🔐 Sign In", use_container_width=True):
            go_to("Sign In")
            st.rerun()

    with col3:
        if st.button("📊 Demo Dashboard", use_container_width=True):
            st.session_state.logged_in = True
            go_to("Dashboard")
            st.rerun()

    st.write("")

    st.markdown("""
<div class="feature-box">

<div class="feature-heading">
✨ New Language Buddy Features
</div>

<div class="feature-list">

<div class="feature-item">
🌍 Language & Level Selection
</div>

<div class="feature-item">
🧠 Vocabulary Quiz
</div>

<div class="feature-item">
⭐ Saved Words
</div>

<div class="feature-item">
🔥 Learning Streak
</div>

<div class="feature-item">
🏆 Achievements
</div>

<div class="feature-item">
📈 Progress Tracking
</div>

<div class="feature-item">
🎯 Daily Learning Goal
</div>

<div class="feature-item">
👤 User Profile
</div>

<div class="feature-item">
⚙️ Settings
</div>

</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# SIGN UP - original + language/level selection
# =========================================================
elif st.session_state.page == "Sign Up":

    st.markdown("<div class='dashboard-title'>Create your Language Buddy account</div>", unsafe_allow_html=True)
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        language = st.selectbox(
            "🌍 Choose a language to learn",
            ["English", "Telugu", "Hindi", "Spanish", "French", "German"]
        )

        level = st.selectbox(
            "🎯 Choose your level",
            ["Beginner", "Intermediate", "Advanced"]
        )

        if st.button("Create Account", use_container_width=True):
            if name and email and password:
                st.session_state.username = name
                st.session_state.email = email
                st.session_state.language = language
                st.session_state.level = level
                st.session_state.logged_in = True
                st.session_state.page = "Dashboard"
                st.success("Account created successfully!")
                st.rerun()
            else:
                st.warning("Please fill all fields.")

    with col2:
        st.markdown("""
        <div class="card">
        <div class="card-title">🌟 Your Learning Journey</div>
        <br>
        1️⃣ Choose your language<br><br>
        2️⃣ Select your level<br><br>
        3️⃣ Learn vocabulary<br><br>
        4️⃣ Practice conversations<br><br>
        5️⃣ Improve speaking<br><br>
        6️⃣ Take quizzes<br><br>
        7️⃣ Track progress and achievements 🏆
        </div>
        """, unsafe_allow_html=True)

    if st.button("Already have an account? Sign In"):
        go_to("Sign In")
        st.rerun()

    if st.button("⬅ Back Home"):
        go_to("Home")
        st.rerun()

# =========================================================
# SIGN IN - original
# =========================================================
elif st.session_state.page == "Sign In":

    st.markdown("<div class='dashboard-title'>Welcome Back 👋</div>", unsafe_allow_html=True)
    st.write("")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign In", use_container_width=True):
        if email and password:
            st.session_state.logged_in = True
            st.session_state.email = email
            st.session_state.username = email.split("@")[0]
            st.session_state.page = "Dashboard"
            st.success("Login successful!")
            st.rerun()
        else:
            st.warning("Enter email and password.")

    if st.button("Create New Account"):
        go_to("Sign Up")
        st.rerun()

    if st.button("⬅ Back Home"):
        go_to("Home")
        st.rerun()

# =========================================================
# DASHBOARD - original + new feature cards
# =========================================================
elif st.session_state.page == "Dashboard":

    st.markdown(
        f"<div class='dashboard-title'>Hello, {st.session_state.username} 👋</div>",
        unsafe_allow_html=True
    )

    st.write(
        f"Continue your **{st.session_state.language}** learning journey. "
        f"Level: **{st.session_state.level}**"
    )

    c1, c2, c3, c4 = st.columns(4)

    stats = [
        (f"{st.session_state.overall_progress}%", "Overall Progress"),
        (str(st.session_state.learned_words), "Words Learned"),
        (str(st.session_state.practice_sessions), "Practice Sessions"),
        (f"{st.session_state.streak} 🔥", "Day Streak")
    ]

    for col, (number, label) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(
                f"""<div class="stat"><div class="stat-number">{number}</div><div class="stat-label">{label}</div></div>""",
                unsafe_allow_html=True
            )

    st.write("")

    st.subheader("🎯 Today's Learning Goal")
    goal_ratio = min(st.session_state.goal_progress / max(st.session_state.daily_goal, 1), 1.0)
    st.progress(goal_ratio)
    st.write(f"{st.session_state.goal_progress} / {st.session_state.daily_goal} minutes completed")

    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card"><div class="card-title">💬 AI Conversation</div>
        <div class="card-text">Practice realistic conversations with your Language Buddy.</div></div>
        """, unsafe_allow_html=True)
        if st.button("Start Conversation", use_container_width=True):
            go_to("Conversation")
            st.rerun()

    with c2:
        st.markdown("""
        <div class="card"><div class="card-title">📚 Vocabulary</div>
        <div class="card-text">Learn words, meanings, examples and synonyms.</div></div>
        """, unsafe_allow_html=True)
        if st.button("Learn Vocabulary", use_container_width=True):
            go_to("Vocabulary")
            st.rerun()

    with c3:
        st.markdown("""
        <div class="card"><div class="card-title">🧠 Vocabulary Quiz</div>
        <div class="card-text">Test your vocabulary knowledge and improve your score.</div></div>
        """, unsafe_allow_html=True)
        if st.button("Take Quiz", use_container_width=True):
            go_to("Quiz")
            st.rerun()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card"><div class="card-title">🎤 Speaking Practice</div>
        <div class="card-text">Record your voice and practice pronunciation and fluency.</div></div>
        """, unsafe_allow_html=True)
        if st.button("Practice Speaking", use_container_width=True):
            go_to("Speaking")
            st.rerun()

    with c2:
        st.markdown("""
        <div class="card"><div class="card-title">📊 Progress</div>
        <div class="card-text">View your skills, weekly activity and achievements.</div></div>
        """, unsafe_allow_html=True)
        if st.button("View Progress", use_container_width=True):
            go_to("Progress")
            st.rerun()

    with c3:
        st.markdown("""
        <div class="card"><div class="card-title">⭐ Saved Words</div>
        <div class="card-text">Review the words you want to remember.</div></div>
        """, unsafe_allow_html=True)
        if st.button("Saved Words", use_container_width=True):
            go_to("Saved")
            st.rerun()

    c1, c2 = st.columns(2)

    with c1:
        if st.button("👤 My Profile", use_container_width=True):
            go_to("Profile")
            st.rerun()

    with c2:
        if st.button("⚙️ Settings", use_container_width=True):
            go_to("Settings")
            st.rerun()

    if st.button("👨‍💼 Admin Dashboard", use_container_width=True):
        go_to("Admin")
        st.rerun()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        st.rerun()

# =========================================================
# AI CONVERSATION - original + scenarios
# =========================================================
elif st.session_state.page == "Conversation":

    st.markdown("<div class='dashboard-title'>💬 AI Conversation</div>", unsafe_allow_html=True)
    st.write(f"Practice **{st.session_state.language}** with your Language Buddy.")

    scenario = st.selectbox("Choose a conversation situation", list(scenarios.keys()))

    if st.button("🔄 Start New Scenario"):
        st.session_state.messages = [("ai", scenarios[scenario])]
        st.rerun()

    if not st.session_state.messages:
        st.session_state.messages.append(
            ("ai", "Hello! 👋 I'm your Language Buddy. How was your day?")
        )

    for sender, message in st.session_state.messages:
        if sender == "user":
            st.markdown(f'<div class="chat-user">{message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai">🤖 {message}</div>', unsafe_allow_html=True)

    user_message = st.chat_input("Type your message...")

    if user_message:
        st.session_state.messages.append(("user", user_message))
        responses = [
            "That's interesting! Can you tell me more?",
            "Great! Your sentence is understandable. Keep practicing!",
            "Nice! Try using another sentence with that word.",
            "Good job! You're improving your communication skills.",
            "Excellent! Let's continue our conversation.",
            "Very good! Try giving a longer answer.",
            "Nice response! Keep speaking confidently."
        ]
        st.session_state.messages.append(("ai", random.choice(responses)))
        add_progress()
        st.rerun()

    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    if st.button("⬅ Back to Dashboard"):
        go_to("Dashboard")
        st.rerun()

# =========================================================
# VOCABULARY - original + save words
# =========================================================
elif st.session_state.page == "Vocabulary":

    st.markdown("<div class='dashboard-title'>📚 Smart Vocabulary</div>", unsafe_allow_html=True)
    st.write("Learn useful words through meanings, examples and synonyms.")

    cols = st.columns(2)

    for i, (word, meaning, example, synonym) in enumerate(vocabulary):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="card">
                <div class="word">{word}</div>
                <br><b>Meaning:</b> {meaning}<br><br>
                <b>Example:</b> {example}<br><br>
                <b>Synonym:</b> {synonym}
                </div>
                """,
                unsafe_allow_html=True
            )

            if word in st.session_state.saved_words:
                if st.button(f"💛 Remove {word}", key=f"remove_{word}"):
                    st.session_state.saved_words.remove(word)
                    st.rerun()
            else:
                if st.button(f"⭐ Save {word}", key=f"save_{word}"):
                    st.session_state.saved_words.append(word)
                    st.session_state.learned_words += 1
                    st.success(f"{word} saved!")

    if st.button("🧠 Take Vocabulary Quiz", use_container_width=True):
        go_to("Quiz")
        st.rerun()

    if st.button("⬅ Back to Dashboard"):
        go_to("Dashboard")
        st.rerun()

# =========================================================
# SAVED WORDS - NEW
# =========================================================
elif st.session_state.page == "Saved":

    st.markdown("<div class='dashboard-title'>⭐ My Saved Words</div>", unsafe_allow_html=True)

    if not st.session_state.saved_words:
        st.info("You haven't saved any words yet. Go to Vocabulary and save some words.")
    else:
        for saved in st.session_state.saved_words:
            item = next((x for x in vocabulary if x[0] == saved), None)
            if item:
                word, meaning, example, synonym = item
                st.markdown(
                    f"""
                    <div class="card">
                    <div class="word">⭐ {word}</div>
                    <br><b>Meaning:</b> {meaning}<br><br>
                    <b>Example:</b> {example}<br><br>
                    <b>Synonym:</b> {synonym}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    if st.button("⬅ Back to Dashboard"):
        go_to("Dashboard")
        st.rerun()

# =========================================================
# QUIZ - NEW
# =========================================================
elif st.session_state.page == "Quiz":

    st.markdown("<div class='dashboard-title'>🧠 Vocabulary Quiz</div>", unsafe_allow_html=True)
    st.write("Choose the correct answer and test your vocabulary.")

    question, options, correct = random.choice(quiz_questions)

    st.markdown(
        f"<div class='card'><div class='card-title'>{question}</div></div>",
        unsafe_allow_html=True
    )

    answer = st.radio("Your answer:", options, key="quiz_option")

    if st.button("Submit Answer", use_container_width=True):
        st.session_state.quiz_total += 1

        if answer == correct:
            st.session_state.quiz_correct += 1
            st.session_state.learned_words += 1
            st.success("🎉 Correct! Excellent work!")
        else:
            st.error(f"❌ Incorrect. Correct answer: {correct}")

    if st.session_state.quiz_total:
        score = int((st.session_state.quiz_correct / st.session_state.quiz_total) * 100)
        st.session_state.quiz_score = score
        st.metric("Quiz Score", f"{score}%")
        st.write(f"Correct: {st.session_state.quiz_correct} / {st.session_state.quiz_total}")

    if st.button("🔄 Next Question", use_container_width=True):
        st.rerun()

    if st.button("⬅ Back to Dashboard"):
        go_to("Dashboard")
        st.rerun()

# =========================================================
# SPEAKING - original + demo feedback
# =========================================================
elif st.session_state.page == "Speaking":

    st.markdown("<div class='dashboard-title'>🎤 Speaking Practice</div>", unsafe_allow_html=True)
    st.write("Record your voice and practice your speaking confidence.")

    sentences = [
        "I am learning English because I want to communicate confidently.",
        "My goal is to improve my speaking skills every day.",
        "I enjoy learning new words and using them in conversations.",
        "Technology can help students learn more effectively.",
        "I want to become a confident English speaker."
    ]

    sentence = random.choice(sentences)

    st.markdown(
        f"""
        <div class="card">
        <div class="card-title">Practice Sentence</div><br>
        <div style="font-size:22px;">"{sentence}"</div><br>
        <div class="card-text">Read the sentence aloud and practice your pronunciation.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    audio = st.audio_input("🎤 Record your voice")

    if audio:
        st.audio(audio)
        st.success("Voice recorded successfully! 🎉")

        # Demo feedback until speech recognition is connected.
        pronunciation = random.randint(75, 95)
        fluency = random.randint(70, 92)
        grammar = random.randint(75, 95)
        overall = int((pronunciation + fluency + grammar) / 3)
        st.session_state.speaking_score = overall
        add_progress()

        st.subheader("📊 Speaking Feedback")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Pronunciation", f"{pronunciation}%")
        c2.metric("Fluency", f"{fluency}%")
        c3.metric("Grammar", f"{grammar}%")
        c4.metric("Overall", f"{overall}%")

        st.info("This is demo scoring. Real pronunciation analysis can be connected later using a speech-recognition service.")

    if st.button("🔄 New Practice Sentence", use_container_width=True):
        st.rerun()

    if st.button("⬅ Back to Dashboard"):
        go_to("Dashboard")
        st.rerun()

# =========================================================
# PROGRESS - NEW
# =========================================================
elif st.session_state.page == "Progress":

    st.markdown("<div class='dashboard-title'>📊 My Progress</div>", unsafe_allow_html=True)
    st.write("Track your learning progress and achievements.")

    quiz_score = int((st.session_state.quiz_correct / st.session_state.quiz_total) * 100) if st.session_state.quiz_total else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Overall Progress", f"{st.session_state.overall_progress}%")
    c2.metric("Words Learned", st.session_state.learned_words)
    c3.metric("Quiz Score", f"{quiz_score}%")
    c4.metric("Speaking Score", f"{st.session_state.speaking_score}%")

    st.write("")
    st.subheader("📈 Weekly Learning Activity")
    st.bar_chart({
        "Monday": 35,
        "Tuesday": 55,
        "Wednesday": 45,
        "Thursday": 70,
        "Friday": 80,
        "Saturday": 60,
        "Sunday": 90
    })

    st.subheader("🎯 Skill Progress")
    st.write("Vocabulary")
    st.progress(min(st.session_state.learned_words / 300, 1.0))
    st.write("Speaking")
    st.progress(st.session_state.speaking_score / 100)
    st.write("Quiz")
    st.progress(quiz_score / 100)
    st.write("Overall")
    st.progress(st.session_state.overall_progress / 100)

    st.subheader("🏆 Achievements")
    achievements = []

    if st.session_state.practice_sessions >= 1:
        achievements.append(("🌱", "First Practice", "Completed your first practice."))
    if st.session_state.learned_words >= 250:
        achievements.append(("📚", "Vocabulary Builder", "Learned 250+ words."))
    if st.session_state.streak >= 7:
        achievements.append(("🔥", "7 Day Streak", "Practiced for 7 days."))
    if quiz_score >= 80:
        achievements.append(("🧠", "Quiz Champion", "Achieved 80%+ quiz score."))
    if st.session_state.speaking_score >= 80:
        achievements.append(("🎤", "Speaking Star", "Reached 80%+ speaking score."))

    if achievements:
        cols = st.columns(3)
        for i, (icon, title, description) in enumerate(achievements):
            with cols[i % 3]:
                st.markdown(
                    f"<div class='badge'><div style='font-size:35px'>{icon}</div><b>{title}</b><br><br>{description}</div>",
                    unsafe_allow_html=True
                )
    else:
        st.info("Keep learning to unlock achievements!")

    if st.button("⬅ Back to Dashboard"):
        go_to("Dashboard")
        st.rerun()

# =========================================================
# PROFILE - NEW
# =========================================================
elif st.session_state.page == "Profile":

    st.markdown("<div class='dashboard-title'>👤 My Profile</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="card">
        <div style="font-size:60px;text-align:center;">👩‍🎓</div>
        <div class="card-title" style="text-align:center;">{st.session_state.username}</div>
        <br>
        <b>Email:</b> {st.session_state.email or 'Not provided'}<br><br>
        <b>Learning Language:</b> {st.session_state.language}<br><br>
        <b>Level:</b> {st.session_state.level}<br><br>
        <b>Words Learned:</b> {st.session_state.learned_words}<br><br>
        <b>Practice Sessions:</b> {st.session_state.practice_sessions}<br><br>
        <b>Current Streak:</b> {st.session_state.streak} 🔥
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("⬅ Back to Dashboard"):
        go_to("Dashboard")
        st.rerun()

# =========================================================
# SETTINGS - NEW
# =========================================================
elif st.session_state.page == "Settings":

    st.markdown("<div class='dashboard-title'>⚙️ Settings</div>", unsafe_allow_html=True)

    language_options = ["English", "Telugu", "Hindi", "Spanish", "French", "German"]
    level_options = ["Beginner", "Intermediate", "Advanced"]

    language = st.selectbox(
        "🌍 Learning Language",
        language_options,
        index=language_options.index(st.session_state.language)
    )

    level = st.selectbox(
        "🎯 Learning Level",
        level_options,
        index=level_options.index(st.session_state.level)
    )

    daily_goal = st.slider("🎯 Daily Goal (minutes)", 5, 60, st.session_state.daily_goal)

    dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)

    if st.button("💾 Save Settings", use_container_width=True):
        st.session_state.language = language
        st.session_state.level = level
        st.session_state.daily_goal = daily_goal
        st.session_state.dark_mode = dark_mode
        st.success("Settings saved! Please refresh the page if you changed the theme.")

    st.write("")
    st.subheader("⚠️ Account")

    if st.button("🔄 Reset Learning Progress", use_container_width=True):
        reset_progress()
        st.success("Learning progress reset successfully.")

    if st.button("⬅ Back to Dashboard"):
        go_to("Dashboard")
        st.rerun()

# =========================================================
# ADMIN DASHBOARD - original + chart
# =========================================================
elif st.session_state.page == "Admin":

    st.markdown("<div class='dashboard-title'>👨‍💼 Admin Dashboard</div>", unsafe_allow_html=True)
    st.write("Monitor Language Buddy learning activity.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Users", "1,245")
    c2.metric("Active Learners", "856")
    c3.metric("Practice Sessions", "12,480")

    st.write("")
    st.subheader("📈 Weekly Activity")
    st.line_chart({
        "Monday": 120,
        "Tuesday": 180,
        "Wednesday": 150,
        "Thursday": 220,
        "Friday": 280,
        "Saturday": 250,
        "Sunday": 310
    })

    st.subheader("Recent Activity")
    activities = [
        "👤 User completed vocabulary lesson",
        "🎤 User completed speaking practice",
        "💬 User completed AI conversation",
        "📚 User learned 20 new words",
        "🧠 User completed vocabulary quiz",
        "🏆 User unlocked a new achievement"
    ]

    for activity in activities:
        st.markdown(f"<div class='card-text'>{activity}</div>", unsafe_allow_html=True)
        st.write("")

    if st.button("⬅ Back to Dashboard"):
        go_to("Dashboard")
        st.rerun()

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("""
<div class="footer">
🌐 Language Buddy · Learn · Practice · Communicate
<br><br>
© 2026 Language Buddy
</div>
""", unsafe_allow_html=True)
