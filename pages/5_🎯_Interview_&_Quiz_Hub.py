import streamlit as st
from style_utils import apply_custom_style, add_footer, track_page_visit
import json
import os

st.set_page_config(page_title="Interview & Quiz Hub", page_icon="🎯", layout="wide")
apply_custom_style()

# Load questions database
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(parent_dir, "questions_db.json")
try:
    with open(db_path, "r", encoding="utf-8") as f:
        db_data = json.load(f)
except Exception as e:
    db_data = {"flashcards": [], "quiz": {}}

# Track page progress visit
track_page_visit("interview_cards_read") # Track general review

st.title("🎯 Interview Prep & Quiz Corner")

st.markdown("""
<div class="custom-card card-purple">
    <h4>Placement Evaluation Portal</h4>
    Prepare for top semiconductor placement drives. Access our high-yield interviewer flashcards 
    and test your concepts in the <b>Quiz Corner</b> across four core domains.
</div>
""", unsafe_allow_html=True)

tab_interview, tab_mock, tab_quiz, tab_tips = st.tabs(["💡 High-Yield Flashcards", "🤖 AI Mock Interviewer", "📝 Quiz Corner", "🏁 Placement Tips"])

# ==========================================
# TAB 1: INTERVIEW PREPARATION
# ==========================================
with tab_interview:
    st.header("VLSI Interview Preparation")
    st.write("Click on any card categories to expand and study high-yield technical Q&As. Your review progress is automatically saved.")
    
    # Initialize track dict for cards read
    if "interview_completed" not in st.session_state.progress:
        st.session_state.progress["interview_completed"] = {}
        
    def read_card(card_id):
        st.session_state.progress["interview_completed"][card_id] = True

    flashcards = db_data.get("flashcards", [])

    # Topic Filter
    all_topics = sorted(list(set(fc.get("topic", "General") for fc in flashcards)))
    selected_topic = st.selectbox("🎯 Filter Flashcards by Domain/Topic:", ["All Topics"] + all_topics, key="flashcard_topic_filter")
    
    if selected_topic != "All Topics":
        flashcards = [fc for fc in flashcards if fc.get("topic") == selected_topic]

    # 1. Basic Questions
    basic_cards = [fc for fc in flashcards if fc.get("category") == "Basic"]
    if basic_cards:
        st.subheader("🟢 Basic Placement Questions")
        for idx, card in enumerate(basic_cards, 1):
            with st.expander(f"Q{idx} ({card.get('topic', 'General')}): {card['question']}"):
                read_card(card["id"])
                st.info(f"**Answer:**\n\n{card['answer']}")

    # 2. Intermediate Questions
    intermediate_cards = [fc for fc in flashcards if fc.get("category") == "Intermediate"]
    if intermediate_cards:
        st.subheader("🟡 Intermediate Technical Questions")
        for idx, card in enumerate(intermediate_cards, 1):
            with st.expander(f"Q{idx} ({card.get('topic', 'General')}): {card['question']}"):
                read_card(card["id"])
                st.info(f"**Answer:**\n\n{card['answer']}")

    # 3. Advanced Questions
    advanced_cards = [fc for fc in flashcards if fc.get("category") == "Advanced"]
    if advanced_cards:
        st.subheader("🔴 Advanced Verification & Back-End Questions")
        for idx, card in enumerate(advanced_cards, 1):
            with st.expander(f"Q{idx} ({card.get('topic', 'General')}): {card['question']}"):
                read_card(card["id"])
                st.info(f"**Answer:**\n\n{card['answer']}")

# ==========================================
# TAB 2: AI MOCK INTERVIEWER
# ==========================================
with tab_mock:
    st.header("🤖 Interactive AI Mock Interviewer")
    st.write("Simulate a live hardware technical screening with an automated interviewer from a top silicon company.")
    
    # Initialize mock stage variables
    if "mock_stage" not in st.session_state:
        st.session_state.mock_stage = "setup" # setup, interview, report
    if "mock_company" not in st.session_state:
        st.session_state.mock_company = "Intel"
    if "mock_q_index" not in st.session_state:
        st.session_state.mock_q_index = 0
    if "mock_responses" not in st.session_state:
        st.session_state.mock_responses = []
    if "mock_evals" not in st.session_state:
        st.session_state.mock_evals = []
        
    mock_questions = {
        "Intel": [
            {
                "q": "1. Explain how you would fix a hold time violation on a clock tree path.",
                "keywords": ["buffer", "delay path", "data path", "delay buffer"],
                "tip": "To fix hold, you need to increase data path delay by inserting delay buffers on the path. Lowering clock frequency does NOT fix hold violations."
            },
            {
                "q": "2. Write the formula for dynamic capacitive switching power and explain the parameters.",
                "keywords": ["C", "V", "f", "alpha", "frequency", "capacitance", "supply"],
                "tip": "The formula is P = alpha * C * Vdd^2 * f, where alpha is activity factor, C is load capacitance, Vdd is voltage, and f is clock frequency."
            },
            {
                "q": "3. What is latch-up in CMOS logic and how do you prevent it in layout?",
                "keywords": ["guard ring", "substrate tap", "parasitic", "SCR", "bipolar", "PNP", "NPN"],
                "tip": "Latch-up is caused by parasitic BJT structures forming an SCR path between VDD and GND. Prevent it by using guard rings and tap cells."
            }
        ],
        "NVIDIA": [
            {
                "q": "1. Define setup time and describe what happens to the output if it is violated.",
                "keywords": ["metastable", "metastability", "stable", "before the clock", "active edge"],
                "tip": "Setup time is the minimum time data must be stable before the clock edge. Violations cause the output to go metastable."
            },
            {
                "q": "2. Explain the differences between blocking (=) and non-blocking (<=) assignments in Verilog.",
                "keywords": ["sequential", "combinational", "parallel", "race condition", "always", "blocking", "non-blocking"],
                "tip": "Blocking assignments evaluate sequentially for combinational logic. Non-blocking evaluate in parallel, preventing sequential race conditions."
            },
            {
                "q": "3. What is Clock Domain Crossing (CDC) and how do you safely synchronize a single-bit signal?",
                "keywords": ["synchronizer", "two-stage", "flip-flop", "metastability", "asynchronous"],
                "tip": "CDC occurs when signals pass between async clock domains. A single-bit signal is synchronized using a multi-stage (2-FF) shift register synchronizer."
            }
        ],
        "Qualcomm": [
            {
                "q": "1. List the three regions of operation for a MOSFET and describe the gate-to-source voltage (Vgs) condition for each.",
                "keywords": ["cutoff", "linear", "triode", "saturation", "Vgs", "Vds", "Vth"],
                "tip": "Regions are: Cutoff (Vgs < Vth), Linear/Triode (Vgs >= Vth, Vds < Vgs - Vth), and Saturation (Vgs >= Vth, Vds >= Vgs - Vth)."
            },
            {
                "q": "2. Write the equations showing how clock skew affects the maximum clock frequency (setup constraint) and hold constraint.",
                "keywords": ["skew", "Tclk", "Th", "Tsu", "combination", "delay"],
                "tip": "For setup: Tclk >= Tcq + Tcomb + Tsu - Tskew. For hold: Tcq + Tcomb >= Th + Tskew. Skew changes the timing margins."
            },
            {
                "q": "3. Explain the Gajski-Kuhn Y-Chart. Name its three domains.",
                "keywords": ["behavioral", "structural", "physical", "geometric", "abstraction"],
                "tip": "The Y-Chart describes VLSI design across three domains: Behavioral (functionality), Structural (gates/blocks), and Physical (geometric placement)."
            }
        ]
    }
    
    if st.session_state.mock_stage == "setup":
        st.subheader("Configure Interview Session")
        st.write("Choose the target hardware corporation and start the screening:")
        
        comp_select = st.selectbox("Select Target Company:", ["Intel", "NVIDIA", "Qualcomm"], key="comp_select")
        
        if st.button("Start Screening"):
            st.session_state.mock_company = comp_select
            st.session_state.mock_stage = "interview"
            st.session_state.mock_q_index = 0
            st.session_state.mock_responses = []
            st.session_state.mock_evals = []
            st.rerun()
            
    elif st.session_state.mock_stage == "interview":
        comp = st.session_state.mock_company
        q_idx = st.session_state.mock_q_index
        questions_pool = mock_questions[comp]
        current_q = questions_pool[q_idx]
        
        st.subheader(f"Screening Session: {comp} | Question {q_idx + 1} of {len(questions_pool)}")
        
        # Display interviewer avatar card
        st.markdown(f"""
        <div style="background-color:#0f172a; padding:1.5rem; border-radius:16px; border-left:6px solid #8b5cf6; margin-bottom:1.5rem; color:white;">
            <b style="color:#a78bfa;">🎙️ Principal Architect ({comp} Interviewer):</b><br>
            <span style="font-size:1.15rem; font-weight:500;">"{current_q['q']}"</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer form
        with st.form(key=f"mock_ans_form_{q_idx}"):
            user_ans = st.text_area("Type your technical explanation below:", height=150, placeholder="Explain clearly in technical terms...")
            submit_ans = st.form_submit_button("Submit Answer")
            
        if submit_ans:
            if len(user_ans.strip()) < 10:
                st.warning("⚠️ Please provide a detailed technical response.")
            else:
                # Grade answer using simple keyword evaluation
                matched_kw = [kw for kw in current_q["keywords"] if kw.lower() in user_ans.lower()]
                kw_score = len(matched_kw) / len(current_q["keywords"])
                
                if kw_score >= 0.7:
                    grade = "Excellent"
                    color = "#10b981"
                elif kw_score >= 0.3:
                    grade = "Acceptable"
                    color = "#f59e0b"
                else:
                    grade = "Incomplete / Weak"
                    color = "#ef4444"
                    
                st.session_state.mock_responses.append(user_ans)
                st.session_state.mock_evals.append({
                    "question": current_q["q"],
                    "answer": user_ans,
                    "grade": grade,
                    "color": color,
                    "tip": current_q["tip"],
                    "matched": matched_kw
                })
                
                # Advance stage
                if q_idx + 1 < len(questions_pool):
                    st.session_state.mock_q_index += 1
                else:
                    st.session_state.mock_stage = "report"
                st.rerun()
                
    elif st.session_state.mock_stage == "report":
        st.subheader("📋 Screening Performance Report Card")
        st.write(f"Company Profile: **{st.session_state.mock_company} Technical Screening**")
        
        # Display grades
        score_count = 0
        for idx, item in enumerate(st.session_state.mock_evals):
            if item["grade"] == "Excellent":
                score_count += 2
            elif item["grade"] == "Acceptable":
                score_count += 1
                
        total_score = len(st.session_state.mock_evals) * 2
        pct = int((score_count / total_score) * 100)
        
        st.markdown(f"""
        <div class="custom-card card-purple">
            <h3 style="margin-top:0;">Overall Performance: {pct}%</h3>
            <p>Your screening profile has been calculated based on keyword density and technical depth checks.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed feedback cards
        for idx, item in enumerate(st.session_state.mock_evals):
            st.markdown(f"""
            <div style="background-color:white; padding:1.5rem; border-radius:16px; border:1px solid #e2e8f0; border-left:6px solid {item['color']}; margin-bottom:1rem;">
                <b style="color:#0f172a;">Q{idx+1}: {item['question']}</b><br>
                <p style="color:#64748b; font-size:0.9rem; margin-top:0.25rem;">Your response: <i>"{item['answer']}"</i></p>
                <b style="color:{item['color']};">Grade: {item['grade']}</b><br>
                <p style="margin-top:0.5rem; color:#0f172a;"><b>📝 Interview Coach Tip:</b> {item['tip']}</p>
            </div>
            """, unsafe_allow_html=True)
            
        if pct >= 80:
            st.success("🎉 Placement Recommended! Your profile is highly competitive. Keep this up for real company drives.")
        else:
            st.info("💡 Keep studying! Read the high-yield flashcards to address missing concepts and try again.")
            
        if st.button("Reset Mock Interview"):
            st.session_state.mock_stage = "setup"
            st.rerun()

# ==========================================
# TAB 3: QUIZ CORNER
# ==========================================
with tab_quiz:
    st.header("Quiz Corner")
    st.write("Select a topic to test your knowledge. Score 100% on any topic to unlock the **Quiz Champion** badge!")
    
    quiz_topic = st.selectbox(
        "Select Quiz Domain:",
        ["VLSI Fundamentals", "CMOS Technology", "VLSI Design Flow", "Verilog Basics"]
    )
    
    # Define questions database
    quiz_db = db_data.get("quiz", {})

    # Load questions based on selection
    q_list = quiz_db[quiz_topic]
    
    # Store quiz state variables to prevent reruning resets
    quiz_key = f"quiz_{quiz_topic.lower().replace(' ', '_')}"
    submitted_key = f"{quiz_key}_submitted"
    
    if submitted_key not in st.session_state:
        st.session_state[submitted_key] = False
        
    with st.form(key=f"form_{quiz_key}"):
        user_selections = []
        for i, question in enumerate(q_list):
            st.markdown(f"**{i+1}. {question['q']}**")
            # Selectbox for answer
            choice = st.radio("Choose option:", question["opts"], key=f"{quiz_key}_q{i}", label_visibility="collapsed")
            user_selections.append(choice)
            
        submit_btn = st.form_submit_button("Submit Quiz")
        
    if submit_btn or st.session_state[submitted_key]:
        st.session_state[submitted_key] = True
        
        # Calculate score
        correct_count = 0
        for i, question in enumerate(q_list):
            if user_selections[i] == question["ans"]:
                correct_count += 1
                
        pct = int((correct_count / len(q_list)) * 100)
        
        # Save score in global progress tracker
        st.session_state.progress["quiz_scores"][quiz_topic] = pct
        
        st.subheader(f"📊 Your Score: {correct_count} / {len(q_list)} ({pct}%)")
        
        if pct == 100:
            st.success("🎉 Perfect Score! You have unlocked the **Quiz Champion** badge on the dashboard!")
        elif pct >= 70:
            st.info("👍 Good job! Review the explanations below to get a perfect score.")
        else:
            st.error("❌ Review the material and try again to improve your score.")
            
        # Explanations
        for i, question in enumerate(q_list):
            with st.expander(f"Review Question {i+1} Details"):
                if user_selections[i] == question["ans"]:
                    st.success(f"Correct! Ans: {question['ans']}")
                else:
                    st.error(f"Your Ans: {user_selections[i]} | Correct: {question['ans']}")
                st.write(f"**Explanation:** {question['exp']}")
                
        if st.button("Retake Quiz", key=f"reset_{quiz_key}"):
            st.session_state[submitted_key] = False
            st.rerun()

# ==========================================
# TAB 3: PLACEMENT TIPS
# ==========================================
with tab_tips:
    st.header("💡 Placement Interview Pro-Tips")
    st.markdown(r"""
    To stand out in competitive hardware placement interviews (Intel, NVIDIA, Qualcomm, AMD, TSMC), keep the following in mind:
    
    1. **Master the Waveforms**: 
       Semiconductor interviewers *love* timing diagrams. When explaining setup/hold times or FSM transitions, draw clock cycles and state variables. Visual answers prove you understand hardware behavior.
       
    2. **Write Synthesizable Verilog**: 
       Always write code that can be synthesized into real logic. Do not write software-like code (avoid arbitrary delays `#5`, loops that cannot unroll, or multi-driven nets). Remember: *every line of code translates into gates or flip-flops*.
       
    3. **Setup and Hold calculations are mandatory**: 
       Expect numerical problems on STA paths. Be comfortable with:
       $$T_{clk} \ge T_{cq\_max} + T_{comb\_max} + T_{su}$$
       $$T_{cq\_min} + T_{comb\_min} \ge T_h + T_{skew}$$
       Know exactly how clock skew shifts these equations.
       
    4. **Explain from first principles**: 
       If asked why PMOS is wider than NMOS, don't just say 'because of mobility'. Explain hole/electron scattering, effective mass, charge carrier velocity saturation, and why it is critical for symmetrical gate delay transitions.
    """)

add_footer()
