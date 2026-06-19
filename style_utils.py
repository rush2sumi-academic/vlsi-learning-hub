import streamlit as st

def apply_custom_style():
    # Load Outfit Font
    st.markdown("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
        <style>
        /* Base page styling */
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
            background-color: #f7fafc;
            color: #1a202c;
        }
        
        /* Heading styling */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            color: #0f172a;
        }
        
        /* Premium Hero Section */
        .hero-section {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #3b82f6 100%);
            color: white;
            padding: 3.5rem 2rem;
            border-radius: 24px;
            margin-bottom: 2.5rem;
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15), 0 8px 10px -6px rgba(15, 23, 42, 0.15);
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            animation: heroSlideIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        @keyframes heroSlideIn {
            from {
                opacity: 0;
                transform: translateY(-15px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .hero-section h1 {
            color: #ffffff !important;
            font-size: 2.8rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            letter-spacing: -0.025em;
        }
        
        .hero-section p {
            font-size: 1.25rem;
            opacity: 0.9;
            font-weight: 400;
            max-width: 800px;
            margin: 0 auto;
        }
        
        /* Custom card styling */
        .custom-card {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            margin-bottom: 1.5rem;
            border: 1px solid #e2e8f0;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            animation: cardFadeIn 0.5s ease-out;
        }
        
        @keyframes cardFadeIn {
            from {
                opacity: 0;
                transform: translateY(12px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .custom-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 10px 10px -5px rgba(0, 0, 0, 0.03);
            border-color: #94a3b8;
        }
        
        /* Card left-border accent colors */
        .card-blue { border-left: 6px solid #3b82f6; }
        .card-green { border-left: 6px solid #10b981; }
        .card-amber { border-left: 6px solid #f59e0b; }
        .card-purple { border-left: 6px solid #8b5cf6; }
        .card-indigo { border-left: 6px solid #6366f1; }
        
        /* Badge UI elements */
        .badge-container {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .badge {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.25rem;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.9rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s ease;
        }
        
        .badge:hover {
            transform: scale(1.05);
        }
        
        .badge-locked {
            background-color: #f1f5f9;
            color: #94a3b8;
            border: 1px dashed #cbd5e1;
        }
        
        .badge-unlocked {
            background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
            color: #0369a1;
            border: 1px solid #7dd3fc;
        }
        
        /* Highlight labels */
        .highlight-title {
            color: #0f172a;
            font-weight: 700;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* Streamlit overrides */
        .stButton>button {
            border-radius: 12px;
            font-weight: 600;
            background-color: #3b82f6;
            color: white;
            border: none;
            padding: 0.5rem 1.5rem;
            transition: all 0.2s;
        }
        .stButton>button:hover {
            background-color: #2563eb;
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.2);
        }
        
        /* Sidebar styling override */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
        }
        [data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }
        
        </style>
    """, unsafe_allow_html=True)

def init_progress_state():
    if "progress" not in st.session_state:
        st.session_state.progress = {
            "intro_vlsi": False,
            "cmos_tech": False,
            "design_flow": False,
            "verilog_basics": False,
            "verilog_examples_count": 0,
            "verilog_completed": {}, # Dict to track which of the 15 examples have been run/verified
            "interview_cards_read": 0,
            "interview_completed": {}, # Dict of card keys read
            "quiz_scores": {
                "VLSI Fundamentals": None,
                "CMOS Technology": None,
                "VLSI Design Flow": None,
                "Verilog Basics": None
            }
        }

def track_page_visit(page_key):
    init_progress_state()
    if page_key in st.session_state.progress:
        st.session_state.progress[page_key] = True

def add_footer():
    st.markdown("---")
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        st.caption("© 2026 VLSI Learning Hub | SRM Institute of Science and Technology")
    with col2:
        st.caption("Developed by: **Dr. Sumitra V** (ECE Dept)")
    with col3:
        st.caption("Powered by Streamlit")
