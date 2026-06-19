import streamlit as st
from style_utils import apply_custom_style, add_footer, track_page_visit

st.set_page_config(page_title="VLSI Design Flow", page_icon="⚙️", layout="wide")
apply_custom_style()

st.markdown("""
<style>
/* Style the active primary button with a premium Purple color */
div.stButton > button[kind="primary"] {
    background-color: #8b5cf6 !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 6px -1px rgba(139, 92, 246, 0.4) !important;
    font-weight: 700 !important;
}
div.stButton > button[kind="primary"]:hover {
    background-color: #7c3aed !important;
    box-shadow: 0 10px 15px -3px rgba(139, 92, 246, 0.5) !important;
}
/* Style the inactive secondary buttons with slate color */
div.stButton > button[kind="secondary"] {
    background-color: #f8fafc !important;
    color: #475569 !important;
    border: 1px solid #cbd5e1 !important;
    font-weight: 500 !important;
}
div.stButton > button[kind="secondary"]:hover {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    border-color: #94a3b8 !important;
}
</style>
""", unsafe_allow_html=True)

# Track that this page has been visited
track_page_visit("design_flow")

st.title("⚙️ VLSI Design Flow")

st.markdown("""
<div class="custom-card card-amber">
    <h4>ASIC & SoC Design Cycle</h4>
    Modern chips are incredibly complex, containing billions of transistors. To manage this complexity, 
    the semiconductor industry uses a structured <b>ASIC Design Flow</b> split into Front-End (Logical) 
    and Back-End (Physical) design. Explore each phase in detail below.
</div>
""", unsafe_allow_html=True)

# Define design flow steps
steps = [
    {
        "icon": "📝",
        "name": "1. System Specification",
        "desc": "Defining the chip's features, performance targets, power budget, interfaces, and architecture.",
        "inputs": "Marketing requirements, industry standards (e.g., PCIe, USB, ARM AMBA).",
        "outputs": "Architectural Specification, Micro-architectural Specification, Pin diagram.",
        "tasks": "Determine system-level blocks, interfaces, clock/reset strategies, power domains, and memory maps.",
        "tools": "SystemC, MATLAB, Python, C/C++ modeling.",
        "interview_tip": "Interviewers may ask about 'Hardware-Software co-design' or system memory interfaces (e.g., SRAM vs DRAM).",
        "image": "flow_spec.jpg"
    },
    {
        "icon": "💻",
        "name": "2. RTL Design",
        "desc": "Describing the digital system's behavior and structure in a hardware description language.",
        "inputs": "Micro-architectural specification.",
        "outputs": "Verilog/SystemVerilog RTL code, IP integration, Lint reports.",
        "tasks": "Write register-transfer level logic, handle Clock Domain Crossings (CDC), run linting checks, and define power control registers.",
        "tools": "Synopsys SpyGlass (Lint/CDC), Cadence JasperGold.",
        "interview_tip": "Expect questions on 'Blocking vs Non-blocking assignments', FSM coding patterns, and synchronizers for CDC.",
        "image": "flow_rtl.jpg"
    },
    {
        "icon": "✅",
        "name": "3. Functional Verification",
        "desc": "Ensuring the RTL design matches the system specification and is completely bug-free.",
        "inputs": "RTL design source files.",
        "outputs": "Testbench environment, simulation waveforms, coverage reports.",
        "tasks": "Develop testbenches using UVM (Universal Verification Methodology), write functional coverage, run formal verification proofs.",
        "tools": "Synopsys VCS, Cadence Xcelium, Siemens Questa Sim.",
        "interview_tip": "Common topics: Code Coverage (line, toggle, FSM) vs Functional Coverage, Assertions (SVA), and UVM components.",
        "image": "flow_verify.jpg"
    },
    {
        "icon": "⛓️",
        "name": "4. Logic Synthesis",
        "desc": "Translating the abstract human-readable RTL code into a gate-level netlist of physical standard cells.",
        "inputs": "RTL code, technology library (.lib), design constraints (.sdc).",
        "outputs": "Gate-level netlist (.v), area/power reports, pre-layout SDC.",
        "tasks": "Translation from HDL, mapping to target standard cells, gate-level optimizations for area, speed, and power.",
        "tools": "Synopsys Design Compiler (DC), Cadence Genus.",
        "interview_tip": "Be prepared to explain what .lib (timing library) and SDC (timing constraints) files contain, and the concept of logic optimization.",
        "image": "flow_synthesis.jpg"
    },
    {
        "icon": "🟧",
        "name": "5. Physical Design",
        "desc": "Transforming the logical gate-level netlist into a physical geometric layout of wires and transistors.",
        "inputs": "Gate-level netlist, physical cell libraries (LEF/GDS), design constraints (SDC).",
        "outputs": "Routed physical layout (GDSII / OASIS), parasitic RC netlists.",
        "tasks": "Floorplanning & Power Planning, Standard Cell Placement, Clock Tree Synthesis (CTS) to reduce skew, Global & Detail Routing, Parasitic Extraction (RC).",
        "tools": "Synopsys IC Compiler II (ICC2), Cadence Innovus, StarRC, Quantus.",
        "interview_tip": "Expect questions on: Clock Skew vs Jitter, IR Drop, Congestion during placement, and H-Tree Clock distribution.",
        "image": "flow_layout.jpg"
    },
    {
        "icon": "⏱️",
        "name": "6. Static Timing Analysis (STA)",
        "desc": "Mathematically validating that every signal in the design arrives at its destination within the clock constraints.",
        "inputs": "Gate-level netlist, parasitics (SPEF), cell delays, clock definition.",
        "outputs": "Setup and Hold timing violation reports, timing Slack.",
        "tasks": "Verify setup and hold checks across all PVT corners (Process, Voltage, Temperature), perform clock gating checks, sign-off timing.",
        "tools": "Synopsys PrimeTime, Cadence Tempus.",
        "interview_tip": "This is a key interview area! Master setup and hold equations, how to fix setup vs hold, and the concept of clock skew on timing.",
        "image": "flow_timing.jpg"
    },
    {
        "icon": "🏭",
        "name": "7. Fabrication",
        "desc": "The chemical and physical manufacturing process where the physical layout is printed onto silicon wafers.",
        "inputs": "Validated GDSII/OASIS design file.",
        "outputs": "Manufactured semiconductor dies on silicon wafers.",
        "tasks": "Photolithography mask preparation, oxidation, etching, ion implantation (doping), chemical vapor deposition, metallization.",
        "tools": "Semiconductor foundry processes (e.g., TSMC, Intel Foundry Services, Samsung).",
        "interview_tip": "You might be asked about wafer processing steps, photolithography resolution limits, and multi-patterning techniques.",
        "image": "flow_fabrication.jpg"
    },
    {
        "icon": "🎯",
        "name": "8. Testing & Debugging",
        "desc": "Evaluating the fabricated silicon chips to identify manufacturing defects before shipping to customers.",
        "inputs": "Fabricated silicon chips, ATPG test patterns.",
        "outputs": "Tested chips, yield analysis report.",
        "tasks": "Scan insertion during DFT, Memory Built-in Self Test (MBIST) execution, testing on Automatic Test Equipment (ATE).",
        "tools": "Synopsys TestMAX, Siemens Tessent, ATE hardware testers.",
        "interview_tip": "Understand the difference between defect (manufacturing physical fault) vs bug (design error), and what scan chains/ATPG do.",
        "image": "flow_testing.jpg"
    }
]

# Initialize active step in session state if not set
if "active_flow_step" not in st.session_state:
    st.session_state.active_flow_step = "1. System Specification"

# Clickable stepper buttons
st.subheader("🛠️ Step-by-Step ASIC Flow Explorer")
st.write("Click on any phase block below to explore its tasks, tools, inputs/outputs, and placement interview tips:")

short_names = ["1. Spec", "2. RTL", "3. Verify", "4. Synthesize", "5. Physical", "6. STA", "7. Fabricate", "8. Test"]
icons = ["📝", "💻", "✅", "⛓️", "🟧", "⏱️", "🏭", "🎯"]
cols = st.columns(8)

for idx, s in enumerate(steps):
    is_active = (s["name"] == st.session_state.active_flow_step)
    btn_type = "primary" if is_active else "secondary"
    btn_label = f"{icons[idx]} {short_names[idx]}"
    
    if cols[idx].button(
        btn_label,
        key=f"btn_flow_{idx}",
        type=btn_type,
        use_container_width=True
    ):
        st.session_state.active_flow_step = s["name"]
        st.rerun()

# Find selected step details
step = next(s for s in steps if s["name"] == st.session_state.active_flow_step)

# Two-column layout: details on the left, diagram on the right
col_details, col_diagram = st.columns([6, 5], gap="large")

with col_details:
    # Display selected step details in a custom card
    st.markdown(f"""
        <div class="custom-card card-indigo">
            <h3 style="margin-top:0; color:#4f46e5;">{step['icon']} {step['name']}</h3>
            <p style="font-size:1.15rem; color:#475569; font-weight:500;">{step['desc']}</p>
            <hr style="margin: 1.5rem 0; border: 0; border-top: 1px solid #e2e8f0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                <div>
                    <b style="color:#0f172a;">📥 Inputs:</b><br>
                    <span style="color:#334155;">{step['inputs']}</span>
                </div>
                <div>
                    <b style="color:#0f172a;">📤 Outputs:</b><br>
                    <span style="color:#334155;">{step['outputs']}</span>
                </div>
            </div>
            <div style="margin-top: 1.5rem;">
                <b style="color:#0f172a;">⚙️ Main Sub-Tasks:</b><br>
                <span style="color:#334155;">{step['tasks']}</span>
            </div>
            <div style="margin-top: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
                <b style="color:#0f172a;">🛠️ Industry Tools:</b>
                <code style="background-color:#f1f5f9; padding:0.25rem 0.5rem; border-radius:6px; color:#4f46e5;">{step['tools']}</code>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Display interview focus box
    st.markdown(f"""
        <div style="background-color:#fffbeb; padding:1.5rem; border-radius:16px; border:1px solid #fef3c7; border-left:6px solid #f59e0b; margin-bottom:2rem;">
            <h5 style="color:#d97706; margin-top:0; display:flex; align-items:center; gap:0.5rem;">
                💡 Placement Interview Focus Area
            </h5>
            <p style="color:#78350f; margin-bottom:0;">{step['interview_tip']}</p>
        </div>
    """, unsafe_allow_html=True)

with col_diagram:
    # Display the engineering diagram corresponding to the current step
    st.image(step["image"], caption=f"Technical Diagram: {step['name']} Phase Details", width="stretch")

# Synthesis vs Physical Design Comparison Section
st.subheader("⚖️ Front-End vs Back-End Comparison")
st.write("Understand the key trade-offs and structural focus differences between logical design and physical implementation:")

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
        <div class="custom-card card-blue">
            <h4 style="color:#2563eb;">🟦 Front-End / Logical Design</h4>
            <ul>
                <li>Focuses on <b>system functionality</b>, logic correctness, and protocol compliance.</li>
                <li>Operates at the <b>abstraction level</b> (RTL, gates). Wires have zero or ideal delays.</li>
                <li>Design checks center on logic code coverage, simulation assertions, and state completeness.</li>
                <li>Key job profiles: RTL Design Engineer, Verification Engineer.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
        <div class="custom-card card-amber">
            <h4 style="color:#d97706;">🟧 Back-End / Physical Design</h4>
            <ul>
                <li>Focuses on <b>physical realization</b>: cell placements, routing, signal integrity, and timing.</li>
                <li>Operates at the <b>geometric silicon level</b>. Wire resistance and capacitance dominate delay (RC dominance).</li>
                <li>Design checks center on physical DRC/LVS compliance, setup/hold slack, and IR power drop.</li>
                <li>Key job profiles: Physical Design (PD) Engineer, STA Engineer, DFT Engineer.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

add_footer()
