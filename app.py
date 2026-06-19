import streamlit as st
from style_utils import apply_custom_style, add_footer, init_progress_state
import plotly.graph_objects as go
import json
import os

# Load questions database to count flashcards
parent_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(parent_dir, "questions_db.json")
try:
    with open(db_path, "r", encoding="utf-8") as f:
        db_data = json.load(f)
    total_flashcards = len(db_data.get("flashcards", []))
except Exception as e:
    total_flashcards = 130 # Fallback

# Load verilog database to count coding examples
v_db_path = os.path.join(parent_dir, "verilog_db.json")
try:
    with open(v_db_path, "r", encoding="utf-8") as f:
        v_db = json.load(f)
    total_verilog_examples = len(v_db)
except Exception as e:
    total_verilog_examples = 106 # Fallback

st.set_page_config(
    page_title="VLSI Interview & Learning Hub",
    page_icon="🎯",
    layout="wide"
)
# Apply premium styling
apply_custom_style()

# Initialize session state for student tracking
init_progress_state()

# Hero Section
st.markdown("""
    <div class="hero-section">
        <h1>🎯 VLSI Interview & Learning Hub</h1>
        <p>A Premium Academic & Placement Preparation Portal for VLSI Students</p>
    </div>
""", unsafe_allow_html=True)

# Main layout split
col1, col2 = st.columns([7, 5], gap="large")

with col1:
    st.markdown("""
        <div class="custom-card card-blue">
            <h3 class="highlight-title">🎓 Bridging Academia to Industry</h3>
            <p>Welcome to the ultimate learning space designed for ECE and VLSI engineering students. 
            This portal covers everything from core device fundamentals to advanced hardware description programming 
            and physical design flows, ensuring you are fully equipped for silicon industry interviews.</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("🚀 Feature Index & Curriculum")
    
    # Grid of Features
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        st.info("📘 **1. Introduction to VLSI**\nEvolution of ICs, SSI to ULSI classifications, Moore's Law, and industrial application sectors.")
        st.info("🧪 **2. CMOS Technology**\nFundamentals of NMOS & PMOS, Inverter VTC curves, I-V characteristics, and power dissipation models.")
        st.info("⚙️ **3. VLSI Design Flow**\nThe complete front-end to back-end ASIC design flow (RTL, Synthesis, Verification, Physical Design & STA).")
    with fcol2:
        st.info("💻 **4. Verilog HDL Basics & Examples**\nSyntax structures, modeling types, and **100+ core programming examples** with interactive simulation waveforms.")
        st.info("🎯 **5. Interview Prep & Quiz Corner**\nHigh-yield questions categorized by level (Basic, Intermediate, Advanced) and simulated evaluation quizzes.")

with col2:
    st.markdown("<h3 style='margin-top:0;'>📊 Student Learning Dashboard</h3>", unsafe_allow_html=True)
    
    # Calculate progress metrics
    p = st.session_state.progress
    core_completed = sum([p["intro_vlsi"], p["cmos_tech"], p["design_flow"], p["verilog_basics"]])
    verilog_examples_done = len([k for k, v in p["verilog_completed"].items() if v])
    interview_q_done = len([k for k, v in p["interview_completed"].items() if v])
    
    # Quiz completions
    quizzes_taken = sum([1 for score in p["quiz_scores"].values() if score is not None])
    max_quiz_score_100 = any([score == 100 for score in p["quiz_scores"].values() if score is not None])
    
    # Progress bars
    st.write(f"**Core Modules Read:** ({core_completed} / 4)")
    st.progress(core_completed / 4.0)
    
    st.write(f"**Verilog Examples Practiced:** ({verilog_examples_done} / {total_verilog_examples})")
    st.progress(verilog_examples_done / float(total_verilog_examples))
    
    st.write(f"**Interview Flashcards Reviewed:** ({interview_q_done} / {total_flashcards})")
    st.progress(interview_q_done / float(total_flashcards))
    
    st.write("")
    # Dynamic Quiz Strength chart
    if quizzes_taken > 0:
        categories = list(p["quiz_scores"].keys())
        scores = [p["quiz_scores"][cat] if p["quiz_scores"][cat] is not None else 0 for cat in categories]
        
        fig_dash = go.Figure(data=[
            go.Bar(name='Quiz Score (%)', x=categories, y=scores, 
                   marker_color='#8b5cf6', 
                   hovertemplate="Topic: %{x}<br>Score: %{y}%")
        ])
        fig_dash.update_layout(
            title="<b>Domain Quiz Strengths (%)</b>",
            yaxis_title="Score (%)",
            yaxis_range=[0, 105],
            margin=dict(l=0, r=0, t=40, b=0),
            height=200,
            template="plotly_white"
        )
        st.plotly_chart(fig_dash, use_container_width=True)
    else:
        st.info("💡 **Placement Check**: No quizzes taken yet. Complete the domain tests in the **Interview Prep & Quiz Corner** to map your technical strengths here!")
    
    st.divider()
    st.subheader("🏅 Achievement Badges")
    
    # Generate badges HTML
    badges_html = "<div class='badge-container'>"
    
    # Badge 1: Silicon Starter
    if p["intro_vlsi"]:
        badges_html += "<div class='badge badge-unlocked'>🏆 Silicon Starter</div>"
    else:
        badges_html += "<div class='badge badge-locked'>🔒 Silicon Starter</div>"
        
    # Badge 2: CMOS Wizard
    if p["cmos_tech"]:
        badges_html += "<div class='badge badge-unlocked'>🔬 CMOS Wizard</div>"
    else:
        badges_html += "<div class='badge badge-locked'>🔒 CMOS Wizard</div>"
        
    # Badge 3: Design Architect
    if p["design_flow"]:
        badges_html += "<div class='badge badge-unlocked'>⚙️ Design Architect</div>"
    else:
        badges_html += "<div class='badge badge-locked'>🔒 Design Architect</div>"
        
    # Badge 4: HDL Coder
    if p["verilog_basics"]:
        badges_html += "<div class='badge badge-unlocked'>💻 HDL Coder</div>"
    else:
        badges_html += "<div class='badge badge-locked'>🔒 HDL Coder</div>"
        
    # Badge 5: Verilog Virtuoso
    if verilog_examples_done >= 10:
        badges_html += "<div class='badge badge-unlocked'>⚡ Verilog Virtuoso</div>"
    else:
        badges_html += "<div class='badge badge-locked'>🔒 Verilog Virtuoso (10+ code examples)</div>"
        
    # Badge 6: Interview Pro
    if interview_q_done >= 8:
        badges_html += "<div class='badge badge-unlocked'>🎓 Interview Pro</div>"
    else:
        badges_html += "<div class='badge badge-locked'>🔒 Interview Pro (8+ cards read)</div>"
        
    # Badge 7: Quiz Champion
    if max_quiz_score_100:
        badges_html += "<div class='badge badge-unlocked'>🔥 Quiz Champion</div>"
    else:
        badges_html += "<div class='badge badge-locked'>🔒 Quiz Champion (100% on any quiz)</div>"
        
    badges_html += "</div>"
    
    st.markdown(badges_html, unsafe_allow_html=True)
    
    st.write("")
    if st.button("Reset Progress"):
        st.session_state.progress = {
            "intro_vlsi": False,
            "cmos_tech": False,
            "design_flow": False,
            "verilog_basics": False,
            "verilog_examples_count": 0,
            "verilog_completed": {},
            "interview_cards_read": 0,
            "interview_completed": {},
            "quiz_scores": {
                "VLSI Fundamentals": None,
                "CMOS Technology": None,
                "VLSI Design Flow": None,
                "Verilog Basics": None
            }
        }
        st.rerun()

st.divider()

# Quick Statistics
col_s1, col_s2, col_s3, col_s4 = st.columns(4)
with col_s1:
    st.metric(label="Total Coding Examples", value=f"{total_verilog_examples} Program Modules")
with col_s2:
    st.metric(label="High-Yield Q&As", value=f"{total_flashcards} Categorized Cards")
with col_s3:
    st.metric(label="Interactive Laboratories", value="2 Active Playgrounds")
with col_s4:
    st.metric(label="Self Evaluation", value="4 Domain Quizzes")

add_footer()
