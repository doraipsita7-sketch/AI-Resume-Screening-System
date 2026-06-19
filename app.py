import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

from predict import predict_job
from database.db import save_candidate, clear_database
from database.db import conn, cursor
from utils.extractor import extract_email, extract_phone, extract_skills


# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="🤖",
    layout="wide"
)

# ================= CUSTOM CSS =================

st.markdown("""
<style>

    [data-testid="collapsedControl"] {
        display: none;
    }

/* ================= BACKGROUND ================= */
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* ================= HERO HEADER ================= */
.hero {
    background: linear-gradient(135deg, #e50914, #141414);
    padding: 45px;
    border-radius: 25px;
    text-align: center;
    box-shadow: 0 15px 50px rgba(0,0,0,0.7);
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 38px;
    margin: 0;
}

.hero p {
    font-size: 18px;
    opacity: 0.8;
}

/* ================= GENERAL CARD ================= */
.card {
    background: rgba(20, 20, 20, 0.95);
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.5);
    margin-bottom: 20px;
    border-left: 4px solid #e50914;
}

/* ================= METRIC CARDS ================= */
.metric-card {
    background: linear-gradient(145deg, #1f1f1f, #0d0d0d);
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 8px 30px rgba(229,9,20,0.25);
    transition: all 0.3s ease;
    border: 1px solid rgba(255,255,255,0.05);
}

.metric-card:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow: 0 15px 40px rgba(229,9,20,0.6);
}

/* ================= SKILL TAGS ================= */
.skill-card {
    display: inline-block;
    background: #e50914;
    color: white;
    padding: 8px 14px;
    margin: 5px;
    border-radius: 25px;
    font-size: 14px;
    font-weight: 500;
    box-shadow: 0 5px 12px rgba(0,0,0,0.3);
    transition: 0.2s;
}

.skill-card:hover {
    background: #ff1e1e;
    transform: scale(1.08);
}

/* ================= SIDEBAR ================= */
section[data-testid="stSidebar"] {
    background: #0b0b0b;
}

/* ================= BUTTONS ================= */
.stButton > button {
    background: #e50914;
    color: white;
    border-radius: 10px;
    padding: 10px 18px;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    background: #ff1e1e;
    transform: scale(1.05);
}

/* ================= INPUT BOX ================= */
input, textarea {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# ================= SKILLS =================


skills_df = pd.read_csv("dataset/skills.csv")
skills_list = skills_df["Skill"].tolist()

# ================= SIDEBAR =================
st.set_page_config(
    page_title="AI Resume System",
    layout="wide",
    initial_sidebar_state="expanded"
)




st.sidebar.title("🤖 AI Resume System")

menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "💼 Job Vacancy", "📤 Upload Resume", "🗄 Database", "🏆 AI Ranking", "📊 Dashboard"]
)




# ================= HOME PAGE =================

if menu == "🏠 Home":


    import streamlit as st

    st.markdown("""
        <style>

        .stApp {
            background: linear-gradient(135deg, #0b0f1a, #1a2a3a);
        }

        .block-container {
            padding: 0rem;
        }

        .title {
            position: absolute;
            bottom: 180px;
            left: 50px;
            font-size: 53px;
            font-weight: bold;
            color: white;
            text-shadow: 0px 0px 30px #00ffe5;
            cursor: pointer;
        }

        .subtitle {
            position: absolute;
            bottom: 150px;
            left: 50px;
            font-size: 20px;
            color: #d0d0d0;
            max-width: 500px;
            cursor: pointer;
        }

        .tag {
            position: absolute;
            bottom: 90px;
            left: 50px;
            padding: 8px 16px;
            border-radius: 20px;
            background: rgba(0,255,255,0.15);
            border: 1px solid #00ffe5;
            color: #00ffe5;
            font-size: 15px;
            cursor: pointer;
        }

        </style>
    """, unsafe_allow_html=True)

    # ✅ IMAGE (CORRECT STREAMLIT WAY - NO img src)
    st.image("images/b1.jpeg", use_container_width=True)

    # OVERLAY TEXT (on top of image)
    st.markdown("""
        <div class="title">AI Resume Screening System</div>
        <div class="subtitle">
            Smart Resume Screening using NLP & Machine Learning
        </div>
        <div class="tag">NLP • ML • AI AUTOMATION</div>
    """, unsafe_allow_html=True)


#======================================Job Vacancy==============================
elif menu == "💼 Job Vacancy":

    st.markdown("""
    <style>

    .job-header{
        background: linear-gradient(135deg,#00c6ff,#0072ff,#001f4d);
        padding:20px;
        border-radius:20px;
        color:white;
        text-align:center;
        margin-bottom:20px;
        box-shadow:0 0 25px rgba(0,198,255,0.4);
    }

    .job-box{
        background: rgba(255,255,255,0.06);
        padding:12px;
        border-radius:12px;
        border:1px solid rgba(0,198,255,0.3);
        text-align:center;
        transition:0.3s;
        box-shadow:0 0 10px rgba(0,198,255,0.1);
        margin:10px;   /* SPACE FIX */
    }

    .job-box:hover{
        transform:scale(1.05);
        box-shadow:0 0 25px rgba(0,198,255,0.4);
        border-left:4px solid #00e6ff;
    }

    .job-title{
        font-size:18px;
        font-weight:bold;
        color:#00e6ff;
    }

    .job-skill{
        font-size:18px;
        color:white;
        opacity:0.8;
    }

    .count-box{
        background: rgba(0,198,255,0.12);
        padding:15px;
        border-radius:15px;
        text-align:center;
        border:1px solid rgba(0,198,255,0.3);
        margin-bottom:15px;
    }

    </style>
    """, unsafe_allow_html=True)

    # ================= HEADER =================
    st.markdown("""
    <div class="job-header">
        <h2>💼 Job Vacancy Board</h2>
        <p>Available Jobs List</p>
    </div>
    """, unsafe_allow_html=True)

    job_roles = {
    "Python Dev": ["python", "sql", "flask"],
    "Data Analyst": ["sql", "pandas", "excel"],
    "ML Engineer": ["machine learning", "numpy", "pandas"],
    "Web Developer": ["html", "css", "javascript"]
}
    # ================= TOTAL COUNT FIX =================
    st.markdown(f"""
    <div class="count-box">
        <h2>{len(job_roles)}</h2>
        <p>Total Job Vacancies</p>
    </div>
    """, unsafe_allow_html=True)

    # ================= GRID LAYOUT =================

    col1, col2 = st.columns(2)

    for i, (role, skills) in enumerate(job_roles.items()):

        with col1 if i % 2 == 0 else col2:

            st.markdown(f"""
            <div class="job-box">
                <div class="job-title">💼 {role}</div>
                <div class="job-skill">{", ".join(skills)}</div>
            </div>
            """, unsafe_allow_html=True)




# ================= UPLOAD PAGE =================

elif menu == "📤 Upload Resume":


    st.markdown("""
                
    <div style="
        background: linear-gradient(135deg,#00c6ff,#0072ff,#001f4d);
        padding:35px;
        border-radius:25px;
        color:white;
        text-align:center;
        margin-bottom:25px;
        box-shadow:0 0 30px rgba(0,198,255,0.5);
    ">
    <h1 style="color:white;">📤 Resume Upload & Analysis</h1>
    <p style="color:white;font-size:18px;">
    Upload candidate resume and extract information automatically
    </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose Resume (PDF)",
        type=["pdf"]
    )

    skills_list = ["Python","SQL","Machine Learning","Pandas","NumPy","HTML","CSS"]

    job_roles = {
    "Python Dev": ["python", "sql"],
    "Data Analyst": ["python", "pandas", "sql"],
    "ML Engineer": ["python", "machine learning", "numpy"]
}


    import os

    # resume folder create if not exists
    if not os.path.exists("resume"):
        os.makedirs("resume")

    # save uploaded file
    if uploaded_file is not None:
        file_path = os.path.join("resume", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("📁 Resume saved successfully in resume folder")
        

    if uploaded_file is not None:

        pdf_reader = PdfReader(uploaded_file)

        text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text


        # ================= EMAIL / PHONE =================
        email = extract_email(text)
        phone = extract_phone(text)


        
       # ================= SKILLS =================
        skill_list = ["python", "java", "html", "css", "sql", "machine learning"]

        # extract skills (KEEP AS LIST)
        found_skills = extract_skills(text, skill_list)
        found = [s.lower().strip() for s in found_skills]
        required_skills = {
            "python": 2,
            "sql": 2,
            "machine learning": 3,
            "pandas": 2,
            "numpy": 1,
            "html": 1,
            "css": 1
        }

        total_weight = sum(required_skills.values())
        earned = 0

        for skill, weight in required_skills.items():
            if skill in found:
                earned += weight

        score = int((earned / total_weight) * 100)

        
        # ================= SCORE CALCULATION =================

        required_skills = ["python","sql","machine learning","html","css","pandas","numpy"]

        found = [s.lower() for s in found_skills]

        matched_skills = [skill for skill in required_skills if skill in found]

        if len(required_skills) == 0:
            score = 0
        else:
            score = int((len(matched_skills) / len(required_skills)) * 100)


        # ================= STATUS =================
        if len(found_skills) == 0:
            score = 0
            status = "Rejected"
        elif score >= 60:
            status = "Selected"
        else:
            status = "Rejected"

        #======================PREDICT JOB=================
        predicted_job = predict_job(text)


        # ================= SCORE =================
        # score = 85


        # ================= STATUS =================
        
        if len(found_skills) == 0:
            final_job = "No Skills Found"
        elif score < 40:
            final_job = "Fresher"
        else:
            final_job = predicted_job

        # ================= JOB PREDICTION =================
        predicted_job = predict_job(text)

        # safe conversion (ONLY IF NEEDED)
        if isinstance(predicted_job, list):
            predicted_job = ", ".join(predicted_job)

        if isinstance(email, list) and len(email) > 0:
            email = email[0]
        else:
            email = "Not Found"

        if isinstance(phone, list) and len(phone) > 0:
            phone = phone[0]
        else:
            phone = "Not Found"


        # ================= DEBUG (optional) =================
        print("EMAIL:", email, type(email))
        print("PHONE:", phone, type(phone))
        print("SKILLS:", found_skills, type(found_skills))
        print("SCORE:", score, type(score))
        print("STATUS:", status, type(status))
        print("JOB:", predicted_job, type(predicted_job))


        # ================= SAVE TO DB =================
        
        st.success(f"🤖 AI Predicted Job Role: {predicted_job}")
        st.success("✅ Resume Uploaded Successfully")
                
       

        st.markdown("")
        st.markdown("---")

        st.markdown("## 📄 Extracted Resume Text")
        st.markdown("""
        <style>

        /* Resume Text Area Styling */
        .stTextArea textarea{
            background: linear-gradient(135deg,#0a0f2c,#0d1b3d,#0a2540) !important;
            color:white !important;
            border-radius:15px !important;
            border:1px solid rgba(255,255,255,0.1) !important;
            transition:all 0.3s ease !important;
            font-size:14px !important;
        }         
                    

        /* Hover Effect */
        .stTextArea textarea:hover{
            box-shadow:0 0 25px rgba(0,198,255,0.6) !important;
            border:1px solid #00c6ff !important;
            transform:scale(1.01);
        }

        /* Focus effect (click karne par bhi glow) */
        .stTextArea textarea:focus{
            box-shadow:0 0 30px rgba(0,198,255,0.7) !important;
            border:1px solid #00c6ff !important;
            outline:none !important;
        }

        </style>
        """, unsafe_allow_html=True)

        st.write(text)

        st.text_area(
            label="Resume Text",
            value=text,
            height=400
        )

        # Email Extraction
        emails = extract_email(text)

        # Phone Extraction
        phones = extract_phone(text)

        # found_skills = extract_skills(text)

        st.markdown("") 
        st.markdown("")
        st.markdown("")


        #============================Candidate Information============
        st.markdown("""
        <style>

        .info-card{
            background: linear-gradient(135deg,#0a0f2c,#0d1b3d,#0a2540);
            padding:8px;
            border-radius:15px;
            color:white;
            text-align:center;
            border:1px solid rgba(255,255,255,0.08);
            transition:all 0.4s ease;
            cursor:pointer;
        }

        .info-card:hover{
            transform:translateY(-6px) scale(1.02);
            box-shadow:0 0 25px rgba(0,198,255,0.5);
            border:1px solid #00c6ff;
        }

        </style>
        """, unsafe_allow_html=True)

        st.markdown("## 📊 Candidate Information")
        st.markdown("")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="info-card">
                <h4>📧 Email</h4>
                <p>{emails[0] if emails else 'Not Found'}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="info-card">
                <h4>📞 Phone</h4>
                <p>{phones[0] if phones else 'Not Found'}</p>
            </div>
            """, unsafe_allow_html=True)

        # Skills Extraction
        found_skills = extract_skills(text, skills_list)


        #======================Extracted Skills======================
        st.markdown("")
        st.markdown("") 
        st.markdown("""
        <style>

        .skill-card{
            cursor:pointer;
            transition:all 0.4s ease;
            background: linear-gradient(135deg,#0a0f2c,#0d1b3d,#0a2540);
            color:white;
        }

        .skill-card:hover{
            # transform:translateY(-8px) scale(1.05);
            # box-shadow:0 0 30px rgba(168,85,247,0.75);
            # border:1px solid #c084fc;
          
            transform:translateY(-5px);
            box-shadow:0 0 20px rgba(0,198,255,0.5);
            border:1px solid #00c6ff;
        }
        </style>
        """, unsafe_allow_html=True)


        st.markdown("## 🧠 Extracted Skills")
        st.markdown("")

        if found_skills:

            cols = st.columns(len(found_skills))

            for i, skill in enumerate(found_skills):

                with cols[i]:

                    st.markdown(
                        f"""
                        <div class="skill-card" style="
                        background: linear-gradient(135deg,#4f46e5,#7c3aed,#9333ea);
                        color:white;
                        padding:10px 12px;
                        border-radius:20px;
                        text-align:center;
                        font-size:13px;
                        font-weight:bold;
                        border:1px solid rgba(255,255,255,0.08);
                        ">
                        ⚡ {skill}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        else:
            st.warning("⚠ No Skills Found")
    
        # ================= JOB MATCHING =================
        st.markdown("")     
        st.markdown("")
        st.markdown("## 💼 Job Matching")
        st.markdown("""
        <style>            

        .job-card{
            background: linear-gradient(135deg,#0a0f2c,#0d1b3d,#0a2540);
            padding:20px;
            border-radius:18px;
            text-align:center;
            transition:0.4s;
            margin-bottom:15px;
            border:1px solid rgba(255,255,255,0.08);
        }

        .job-card:hover{
            transform:translateY(-8px);
            box-shadow:0 0 25px rgba(0,198,255,0.5);
            border:1px solid #00c6ff;
        }

        .job-name{
            color:white;
            font-size:20px;
            font-weight:bold;
            margin-bottom:10px;
        }

        .job-score{
            color:#00c6ff;
            font-size:32px;
            font-weight:bold;
        }

        .job-skill{
            color:#cbd5e1;
            font-size:14px;
            margin-top:8px;
        }

        </style>
        """, unsafe_allow_html=True)

        # st.markdown("""
        # <h1 style="
        # text-align:center;
        # # font-size:25px;
        # # font-weight:bold;
        # color:white;
        # margin-bottom:20px;
        # text-align:left;
        # ">
        # 💼 Job Matching
        # </h1>
        # """, unsafe_allow_html=True)
        
    

        #=============================Job Matching=================

        # ================= JOB ROLES =================
        job_roles = {
            "Python Dev": ["Python", "SQL"],
            "Data Analyst": ["Python", "Pandas", "SQL"],
            "ML Engineer": ["Python", "Machine Learning", "NumPy"],
            "Web Developer": ["HTML", "CSS"]
        }

        job_scores = {}

        col1, col2 = st.columns(2)

        for i, (job, req_skills) in enumerate(job_roles.items()):

            matched = [
                skill for skill in req_skills
                if skill.lower() in found
            ]

            score_job = 0

            for skill in req_skills:
                if skill.lower() in found:
                    score_job += 1

            score_percent = int((score_job / len(req_skills)) * 100)

            job_scores[job] = score_percent

            card = f"""
            <div class="job-card">
                <div class="job-name">💼 {job}</div>
                <div class="job-score">{score_percent}%</div>
                <div class="job-skill">
                    ✅ {len(matched)} / {len(req_skills)} Skills Matched
                </div>
            </div>
            """

            if i % 2 == 0:
                col1.markdown(card, unsafe_allow_html=True)
            else:
                col2.markdown(card, unsafe_allow_html=True)


        if job_scores:
            best_job = max(job_scores, key=job_scores.get)
            best_score = job_scores[best_job]
        else:
            best_job = "Not Found"
            best_score = 0


        status = "Selected" if best_score >= 60 else "Rejected"

        # ================= FINAL RESULT UI (STYLISH BOX) =================
        st.markdown("") 
        st.markdown("")
        st.markdown("")  
        st.markdown("## 📈 Final Result")

        st.markdown(f"""
        <style>

        .result-box {{
            background: linear-gradient(135deg,#0f172a,#1e293b);
            padding: 25px;
            border-radius: 18px;
            text-align: center;
            color: white;
            box-shadow: 0 0 20px rgba(0,198,255,0.3);
            transition: 0.3s ease;
            margin-top: 10px;
        }}

        .result-box:hover {{
            transform: translateY(-5px);
            box-shadow: 0 0 35px rgba(0,198,255,0.6);
        }}

        .result-title {{
            font-size: 22px;
            font-weight: bold;
            color: #00c6ff;
        }}

        .result-score {{
            font-size: 40px;
            font-weight: bold;
            margin: 10px 0;
        }}

        .result-status {{
            font-size: 18px;
            margin-top: 5px;
        }}

        </style>

        <div class="result-box">
            <div class="result-title">🏆 Best Matching Role</div>
            <div class="result-score">{best_job}</div>
            <div class="result-title">📊 Score: {best_score}%</div>
            <div class="result-status">{status}</div>
        </div>
        """, unsafe_allow_html=True)


        # ================= SAVE TO DATABASE =================
        save_candidate(
            email,
            phone,
            ", ".join(found_skills),
            best_score,
            status,
            best_job
        )
        st.markdown("")
        st.markdown("")  

        st.success("✅ Resume Processed Successfully")
                
#--------------------DATABASE------------------

elif menu == "🗄 Database":

    import pandas as pd

    st.markdown("""
        <style>

        .stApp {
            background: linear-gradient(135deg, #050b1a, #0a1f3d, #0d2b4f);
        }

        .title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: #00e6ff;
            text-shadow: 0px 0px 20px #00e6ff;
            margin-bottom: 20px;
        }

        .stDataFrame {
            background: rgba(255,255,255,0.05) !important;
            border-radius: 18px !important;
            border: 1px solid rgba(0,230,255,0.3) !important;
        }

        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="title">🗄 Candidate Database</div>',
        unsafe_allow_html=True
    )

    cursor.execute("""
    SELECT email, phone, skills, job_role, score, status
    FROM candidates
    """)

    data = cursor.fetchall()

    if len(data) == 0:
        st.warning("No Data Found")

    else:

        df = pd.DataFrame(
            data,
            columns=[
                "Email",
                "Phone",
                "Skills",
                "Predicted Job",
                "Job Score",
                "Status"
            ]
        )

        # Download CSV
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download CSV",
            data=csv,
            file_name="candidate_database.csv",
            mime="text/csv"
        )

        # Show Table
        st.dataframe(
            df,
            use_container_width=True
        )
    

#====================================AI Ranking=================================

elif menu == "🏆 AI Ranking":

    import pandas as pd

    st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(135deg, #0a0f2c, #0d1b3d, #0a2540);
    }

    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #00e6ff;
        margin-bottom: 25px;
        text-shadow: 0 0 20px #00e6ff;
    }

    .box {
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(0,230,255,0.3);
        box-shadow: 0 0 10px rgba(0,230,255,0.2);
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title">🏆 AI Resume Ranking Dashboard</div>', unsafe_allow_html=True)

    # ================= FILTER =================
    only_selected = st.checkbox("🌟 Show Only Selected Candidates")

    # ================= FETCH DATA =================
    cursor.execute("SELECT email, phone, skills, score, status, job_role FROM candidates")
    data = cursor.fetchall()

    # sort by score
    ranked = sorted(data, key=lambda x: x[3], reverse=True)

    chart_list = []

    # ================= LOOP =================
    for i, row in enumerate(ranked, start=1):

        email, phone, skills, score, status, job_role = row

        if only_selected and status != "Selected":
            continue

        # 🥇 TOP 3 MEDALS
        if i == 1:
            medal = "🥇"
        elif i == 2:
            medal = "🥈"
        elif i == 3:
            medal = "🥉"
        else:
            medal = f"#{i}"

        chart_list.append((email, score))

        # ================= CARD =================
        st.markdown(f"""
        <div class="box">

        <h3>{medal} Rank {i}</h3>

        📧 Email: {email}  
        📱 Phone: {phone}  
        🧠 Skills: {skills}  

        📊 Score: {score}%  
        📌 Status: {status}  
        🏆 Job Role: {job_role}

        </div>
        """, unsafe_allow_html=True)

        st.progress(int(score))

    # ================= CHART =================
    if chart_list:

        st.markdown("## 📈 Score Comparison Chart")

        df = pd.DataFrame(chart_list, columns=["Candidate", "Score"])

        st.bar_chart(df.set_index("Candidate"))

    


#=================================Dashboard=============================

elif menu == "📊 Dashboard":

    st.markdown("""
    <style>

    .dashboard-header{
        background: linear-gradient(135deg,#00c6ff,#0072ff,#001f4d);
        padding:35px;
        border-radius:25px;
        color:white;
        text-align:center;
        margin-bottom:25px;
        box-shadow:0 0 30px rgba(0,198,255,0.5);
    }

    .glass-card{
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(10px);
        padding:20px;
        border-radius:15px;
        text-align:center;
        border:1px solid rgba(0,230,255,0.3);
        transition:0.3s;
    }

    .glass-card:hover{
        transform:translateY(-6px);
        box-shadow:0 0 25px rgba(0,230,255,0.5);
        border-left:5px solid #00e6ff;
    }

    .value{
        font-size:32px;
        font-weight:bold;
        color:#00e6ff;
    }

    .label{
        color:white;
        font-size:16px;
    }

    </style>
    """, unsafe_allow_html=True)

    # ================= HEADER =================
    st.markdown("""
    <div class="dashboard-header">
        <h1>🤖 AI Resume Screening Dashboard</h1>
        <p>Smart Candidate Analysis • NLP • AI Ranking System</p>
    </div>
    """, unsafe_allow_html=True)

    # ================= STATS =================
    cursor.execute("SELECT COUNT(*) FROM candidates")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM candidates WHERE status='Selected'")
    selected = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM candidates WHERE status='Rejected'")
    rejected = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(score) FROM candidates")
    avg = cursor.fetchone()[0] or 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="value">{total}</div>
            <div class="label">👥 Total Candidates</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="value">{selected}</div>
            <div class="label">✅ Selected</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="value">{rejected}</div>
            <div class="label">❌ Rejected</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="value">{avg:.1f}</div>
            <div class="label">📈 Average Score</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ================= TOP CANDIDATE =================
    st.subheader("🏆 Top Candidate")

    cursor.execute("""
        SELECT email, score
        FROM candidates
        ORDER BY score DESC
        LIMIT 1
    """)

    top = cursor.fetchone()

    if top:
        st.markdown(f"""
        <div style="
        background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
        padding:25px;
        border-radius:20px;
        cursor: pointer;
        border-left:6px solid #00e6ff;
        color:white;
        box-shadow:0 0 25px rgba(0,230,255,0.3);
        ">
            <h2 style="color:#00e6ff;">🏆 Top Candidate</h2>
            <p style="font-size:18px;">📧 {top[0]}</p>
            <p style="font-size:22px;font-weight:bold;">⭐ Score: {top[1]}</p>
        </div>
        """, unsafe_allow_html=True)


    st.markdown("""
<style>

/* Main table container */
[data-testid="stDataFrame"]{
    border-radius:18px;
    overflow:hidden;
    border:1px solid rgba(0,230,255,0.3);
    box-shadow:0 0 20px rgba(0,198,255,0.15);
}

/* Header styling */
thead tr th{
    background: linear-gradient(135deg,#0a1f3d,#0072ff) !important;
    color:#00e6ff !important;
    font-size:15px;
    font-weight:bold;
}

/* Row hover effect */
tbody tr:hover{
    background: rgba(0,198,255,0.08) !important;
    transform: scale(1.01);
    transition:0.2s;
}

/* Row spacing */
tbody tr td{
    padding:10px !important;
    color:white;
}

</style>
""", unsafe_allow_html=True)
    st.markdown("---")

    # ================= RECENT 5 =================
    st.subheader("🕒 Recent Candidates")

    cursor.execute("""
        SELECT email, phone, skills, score, status, job_role
        FROM candidates
        ORDER BY id DESC
        LIMIT 5
    """)
    
    data = cursor.fetchall()

    import pandas as pd

    df = pd.DataFrame(
        data,
        columns=["Email","Phone","Skills","Score","Status","Job Role"]
    )

    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # ================= DOWNLOAD CSV =================
    st.subheader("⬇ Export Data")


    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        # label="📥 Download CSV Report",
          "⬇ Download CSV",
        data=csv,
        file_name="AI_Resume_Data.csv",
        mime="text/csv",
        use_container_width=True
    )

