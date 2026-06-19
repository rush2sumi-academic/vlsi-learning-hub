import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from style_utils import apply_custom_style, add_footer, track_page_visit

st.set_page_config(page_title="Introduction to VLSI", page_icon="📘", layout="wide")
apply_custom_style()

# Track that this page has been visited
track_page_visit("intro_vlsi")

st.title("📘 Introduction to VLSI")

st.markdown("""
<div class="custom-card card-blue">
    <h4>Core Module</h4>
    Welcome to the introductory module. Here we cover the basic concepts of VLSI technology, 
    the evolution of integrated circuits, Moore's Law, applications, and current industry challenges.
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🏛️ Evolution & Scale", "📈 Moore's Law", "🌐 Applications", "⚡ Advantages & Challenges"])

with tab1:
    st.header("What is VLSI?")
    st.write("""
    **Very Large Scale Integration (VLSI)** is the process of creating an integrated circuit (IC) by combining thousands or millions of transistors onto a single silicon chip. 
    Before VLSI, electronic circuits typically consisted of discrete transistors, resistors, diodes, and capacitors connected on a printed circuit board (PCB). 
    VLSI allows complex systems—such as CPUs, GPUs, and complete System-on-Chips (SoCs)—to fit in the palm of your hand.
    """)
    
    st.subheader("Evolution of Integrated Circuits")
    st.write("""
    The integration of semiconductor components has evolved dramatically over the last few decades. 
    Below is the classification of ICs based on the number of active devices (gates/transistors) integrated per chip:
    """)
    
    # Comparative Table
    evolution_data = {
        "Era / Standard": ["SSI (Small Scale Integration)", "MSI (Medium Scale Integration)", "LSI (Large Scale Integration)", "VLSI (Very Large Scale Integration)", "ULSI (Ultra Large Scale Integration)"],
        "Active Devices per Chip": ["1 to 10", "10 to 100", "100 to 10,000", "10,000 to 1,000,000", "Over 1,000,000"],
        "Typical Components": ["Basic Logic Gates, Flip-Flops", "Counters, Adders, Decoders", "8-bit Microprocessors, Small ROM/RAM", "16/32-bit CPUs, Complex Digital Controllers", "Modern Multi-core CPUs, GPUs, AI Accelerators"]
    }
    df = pd.DataFrame(evolution_data)
    st.table(df)
    
    st.info("💡 **Historical Context**: The transition from LSI to VLSI occurred in the late 1970s when the number of gates approached 10,000. Today, we regularly fabricate chips containing tens of billions of transistors, representing a transition into deep sub-micron ULSI and beyond.")

with tab2:
    st.header("Moore's Law")
    st.markdown("""
    In 1965, **Gordon Moore**, the co-founder of Intel, made an observation that the number of transistors on a microchip doubles approximately every two years, 
    while the cost of computers is halved. 
    
    Although often referred to as a "law," it is actually an empirical observation and an industrial roadmap that has driven the semiconductor industry for over 50 years.
    """)
    
    # Interactive Plotly chart showing historical chip transistor count vs Moore's Law projection
    years = [1971, 1974, 1978, 1982, 1985, 1989, 1993, 1997, 1999, 2000, 2006, 2010, 2015, 2020, 2022]
    chips = ["Intel 4004", "Intel 8080", "Intel 8086", "Intel 286", "Intel 386", "Intel 486", "Pentium", "Pentium II", "Pentium III", "Pentium 4", "Core 2 Duo", "Core i7", "Core i7 (Broadwell)", "Apple M1", "Apple M2 Ultra"]
    counts = [2300, 6000, 29000, 134000, 275000, 1200000, 3100000, 7500000, 9500000, 42000000, 291000000, 730000000, 1900000000, 16000000000, 134000000000]
    
    # Theoretical Moore's Law (starting at 2300 in 1971, doubling every 2 years)
    theoretical_counts = [2300 * (2 ** ((yr - 1971)/2.0)) for yr in years]
    
    fig = go.Figure()
    # Actual
    fig.add_trace(go.Scatter(x=years, y=counts, mode='markers+lines', 
                             name='Actual Transistor Count',
                             text=chips,
                             hovertemplate="<b>%{text}</b><br>Year: %{x}<br>Transistors: %{y:,.0f}",
                             line=dict(color='#3b82f6', width=3),
                             marker=dict(size=8, color='#0f172a')))
    # Projected
    fig.add_trace(go.Scatter(x=years, y=theoretical_counts, mode='lines', 
                             name="Moore's Law (Doubles every 2 years)",
                             line=dict(color='#ef4444', dash='dash'),
                             hoverinfo='none'))
    
    fig.update_layout(
        title="Evolution of Chip Transistor Counts (Log Scale)",
        xaxis_title="Year of Introduction",
        yaxis_title="Transistor Count (Logarithmic)",
        yaxis_type="log",
        margin=dict(l=0, r=0, t=40, b=0),
        height=500,
        legend=dict(x=0.01, y=0.99),
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.warning("⚠️ **Is Moore's Law Dead?**: As physical limits are reached (transistor gate dimensions approaching atomic scales below 2nm), classical scaling has slowed down. The industry is adapting through 'More than Moore' technologies, such as **3D IC stacking, Chiplets, and Advanced Packaging** (e.g., TSMC's CoWoS).")

with tab3:
    st.header("Applications of VLSI")
    st.write("VLSI technology is the backbone of almost all modern electronic systems. Main industries include:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="custom-card card-green">
            <h5>💻 Consumer Electronics & Computing</h5>
            <ul>
                <li><b>Personal Computing</b>: Microprocessors, DRAM memories, and SSD controllers.</li>
                <li><b>Mobile Technologies</b>: Smartphones, tablets, and smartwatches driven by integrated Systems-on-Chips (SoCs).</li>
                <li><b>Smart Appliances</b>: Microcontrollers inside IoT devices, smart TVs, and home security.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card card-amber">
            <h5>🚗 Automotive Systems</h5>
            <ul>
                <li><b>ADAS (Advanced Driver Assistance Systems)</b>: Real-time image and radar processing chips.</li>
                <li><b>ECUs</b>: Engine control, braking, and battery management systems.</li>
                <li><b>Infotainment & Cockpits</b>: Touchscreen drivers and high-definition audio/video processors.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="custom-card card-purple">
            <h5>🛰️ Telecommunication & Aerospace</h5>
            <ul>
                <li><b>5G Infrastructure</b>: High-speed RF transceivers and digital baseband processors.</li>
                <li><b>Networking</b>: Router switches, network cards, and fiber-optic transmitters.</li>
                <li><b>Aerospace Rad-Hard Chips</b>: Radiation-hardened VLSI circuits for satellite electronics and deep-space missions.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card card-indigo">
            <h5>🧠 AI & High-Performance Computing</h5>
            <ul>
                <li><b>Tensor Processing Units (TPUs)</b>: Custom ASIC accelerators optimized for neural network training and inference.</li>
                <li><b>Data Centers</b>: Massive parallel GPUs, high-speed interfaces, and memory-hub controllers.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.header("Advantages and Challenges of VLSI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="custom-card card-green">
            <h5 style="color:#10b981;">✅ Key Advantages</h5>
            <ol>
                <li><b>Reduced Physical Size</b>: Combining millions of circuits into a tiny silicon footprint.</li>
                <li><b>High Performance & Speed</b>: Short interconnect paths lead to extremely low propagation delay.</li>
                <li><b>Lower Power Consumption</b>: Shrinking transistors consume significantly less dynamic energy.</li>
                <li><b>Cost Efficiency</b>: High-volume manufacturing (batch fabrication) dramatically drops the per-transistor cost.</li>
                <li><b>High Reliability</b>: Eliminating external wiring connections reduces mechanical and electrical failures.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="custom-card card-amber">
            <h5 style="color:#f59e0b;">⚠️ Industrial Challenges</h5>
            <ol>
                <li><b>Static Leakage Current</b>: Thin gate oxides lead to quantum tunneling and leakage power issues.</li>
                <li><b>Thermal / Heat Dissipation</b>: Packaging millions of switching elements produces significant heat density.</li>
                <li><b>High Design Complexity</b>: Designing chips with billions of nodes requires complex EDA tools and lengthy verification processes.</li>
                <li><b>Short Channel Effects (SCE)</b>: At sub-micron levels, drain voltages start controlling the channel instead of the gate.</li>
                <li><b>Huge Capital Cost</b>: Constructing modern semiconductor fabrication plants (Fabs) costs upwards of $15-20 billion.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

add_footer()
