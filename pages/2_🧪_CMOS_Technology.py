import streamlit as st
import numpy as np
import plotly.graph_objects as go
from style_utils import apply_custom_style, add_footer, track_page_visit

st.set_page_config(page_title="CMOS Technology", page_icon="🧪", layout="wide")
apply_custom_style()

# Track that this page has been visited
track_page_visit("cmos_tech")

st.title("🧪 CMOS Technology Fundamentals")

st.markdown("""
<div class="custom-card card-green">
    <h4>Core Module</h4>
    This module covers the physics and operation of NMOS and PMOS transistors, the CMOS inverter logic, 
    interactive device characteristics, power dissipation models, and the advantages of CMOS.
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🏛️ Transistor Physics (NMOS vs PMOS)", 
    "📈 I-V Characteristics Lab", 
    "🔌 CMOS Inverter VTC Lab", 
    "🔋 Power & Advantages"
])

with tab1:
    st.header("CMOS Basics & Device Physics")
    st.write("""
    **Complementary Metal-Oxide-Semiconductor (CMOS)** is the core technology used to manufacture integrated circuits. 
    It is "complementary" because it uses both N-type (NMOS) and P-type (PMOS) MOSFETs to build logic gates.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. NMOS Transistor")
        st.write("""
        - **Structure**: Built on a P-type substrate with N-type Source and Drain diffusions.
        - **Operation**: A positive gate-to-source voltage ($V_{gs} > V_{th}$) attracts electrons under the gate oxide, forming an N-channel. This allows current to flow from Drain to Source (electrons move from Source to Drain).
        - **Logic Function**: Acts as a **pull-down network (PDN)** to pull outputs to ground (Logic 0).
        """)
        col_img1, col_img2 = st.columns([1, 2])
        with col_img1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/N-MOSFET_symbol.svg/150px-N-MOSFET_symbol.svg.png", caption="NMOS Symbol", width=100)
        with col_img2:
            st.image("nmos_cross_section.jpg", caption="NMOS Physical Structure", width="stretch")
        
    with col2:
        st.subheader("2. PMOS Transistor")
        st.write("""
        - **Structure**: Built on an N-well inside a P-type substrate, with P-type Source and Drain diffusions.
        - **Operation**: A negative gate-to-source voltage ($V_{gs} < -|V_{thp}|$, i.e., gate is grounded relative to source) attracts holes under the gate oxide, forming a P-channel.
        - **Logic Function**: Acts as a **pull-up network (PUN)** to connect outputs to $V_{DD}$ (Logic 1).
        """)
        col_img3, col_img4 = st.columns([1, 2])
        with col_img3:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/P-MOSFET_symbol.svg/150px-P-MOSFET_symbol.svg.png", caption="PMOS Symbol", width=100)
        with col_img4:
            st.image("pmos_cross_section.jpg", caption="PMOS Physical Structure", width="stretch")

    st.subheader("Transistor Operational Regions")
    st.write("A MOSFET operates in one of three regions depending on voltages ($V_{gs}$, $V_{ds}$, and threshold voltage $V_{th}$):")
    st.markdown(r"""
    1. **Cut-off ($V_{gs} < V_{th}$)**: Channel is not formed. $I_d \approx 0$.
    2. **Linear/Triode ($V_{gs} \ge V_{th}$ and $V_{ds} < V_{gs} - V_{th}$)**: Channel is continuous. Current increases linearly with drain voltage:
       $$I_d = \beta \left( (V_{gs} - V_{th})V_{ds} - \frac{V_{ds}^2}{2} \right)$$
    3. **Saturation ($V_{gs} \ge V_{th}$ and $V_{ds} \ge V_{gs} - V_{th}$)**: Channel pinches off at the drain side. Current saturates and is independent of $V_{ds}$:
       $$I_d = \frac{\beta}{2} (V_{gs} - V_{th})^2$$
    """)

with tab2:
    st.header("Interactive MOSFET I-V Characterization")
    st.write("Adjust the parameters to see the drain current characteristics of an NMOS transistor.")
    
    col_ctrl, col_plot = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown("**Slider Controls**")
        vgs_val = st.slider("Gate-Source Voltage (Vgs) [V]", 0.0, 5.0, 3.0, 0.1)
        vth_val = st.slider("Threshold Voltage (Vth) [V]", 0.3, 1.5, 0.7, 0.1)
        beta_val = st.slider("Transistor Gain Beta (k')", 0.5, 4.0, 2.0, 0.1)
        vds_range = 5.0
        
    with col_plot:
        vds_arr = np.linspace(0, vds_range, 100)
        id_arr = []
        reg_arr = []
        
        for v in vds_arr:
            if vgs_val < vth_val:
                id_arr.append(0)
                reg_arr.append("Cut-off")
            elif v < (vgs_val - vth_val):
                # Linear
                id_arr.append(beta_val * ((vgs_val - vth_val) * v - (v**2)/2.0))
                reg_arr.append("Linear")
            else:
                # Saturation
                id_arr.append((beta_val / 2.0) * (vgs_val - vth_val)**2)
                reg_arr.append("Saturation")
                
        fig_iv = go.Figure()
        fig_iv.add_trace(go.Scatter(x=vds_arr, y=id_arr, mode='lines', 
                                    line=dict(color='#10b981', width=4),
                                    name=f'Vgs = {vgs_val}V',
                                    hovertemplate="Vds: %{x:.2f}V<br>Id: %{y:.2f}mA"))
        
        # Mark saturation transition point
        if vgs_val > vth_val:
            v_sat = vgs_val - vth_val
            i_sat = (beta_val / 2.0) * (vgs_val - vth_val)**2
            fig_iv.add_trace(go.Scatter(x=[v_sat], y=[i_sat], mode='markers',
                                        marker=dict(size=12, color='#ef4444', symbol='circle'),
                                        name='Pinch-off Point'))
            fig_iv.add_annotation(x=v_sat, y=i_sat, text="Saturation Start", showarrow=True, arrowhead=1, yshift=10)
            
        fig_iv.update_layout(
            xaxis_title="Drain-Source Voltage Vds [V]",
            yaxis_title="Drain Current Id [mA]",
            margin=dict(l=0, r=0, t=30, b=0),
            height=400,
            template="plotly_white"
        )
        st.plotly_chart(fig_iv, use_container_width=True)

with tab3:
    st.header("CMOS Inverter Lab")
    st.write("""
    A **CMOS Inverter** consists of a PMOS transistor (PUN) at the top, connected to $V_{DD}$, 
    and an NMOS transistor (PDN) at the bottom, connected to Ground. The gates of both devices are connected to the input $V_{in}$.
    """)
    
    col_inv1, col_inv2 = st.columns([1, 2])
    
    with col_inv1:
        st.image("images/CMOS_Inverter.png",width=200,caption="CMOS Inverter Schematic")
        st.image("cmos_cross_section.jpg", caption="CMOS Integrated Inverter Cross-Section", width="stretch")
        st.write("""
        **Operational States:**
        - **Vin = 0 (Logic L)**: NMOS OFF, PMOS ON → Output pulled to $V_{DD}$ (Logic H).
        - **Vin = VDD (Logic H)**: NMOS ON, PMOS OFF → Output pulled to Ground (Logic L).
        """)
        
        st.markdown("**Adjust Transistor Sizing Ratio:**")
        # Ratio of beta (kp/kn)
        beta_ratio = st.slider("Beta Ratio (W/L)_p / (W/L)_n", 0.5, 4.0, 1.0, 0.1, help="Typically PMOS is wider (2-3x) to compensate for lower hole mobility.")
        
    with col_inv2:
        # Generate VTC curve
        vdd = 3.3
        vin_arr = np.linspace(0, vdd, 100)
        vout_arr = []
        
        # Switching threshold calculation
        # Vm = (Vthn + (r**0.5) * (Vdd - |Vthp|)) / (1 + r**0.5) where r = beta_p / beta_n
        vthn = 0.5
        vthp = 0.5
        r = beta_ratio
        v_m = (vthn + (r**0.5) * (vdd - vthp)) / (1.0 + r**0.5)
        
        # Calculate transition slope S
        slope = 10.0 * (1.0 + (r-1.0)*0.15)
        
        # Calculate mathematically exact Vil, Vih, Vol, Voh where dVout/dVin = -1
        sq_term = (vdd * slope / np.pi) - 1.0
        if sq_term < 0:
            sq_term = 0.0
            
        v_il = v_m - (1.0 / slope) * np.sqrt(sq_term)
        v_ih = v_m + (1.0 / slope) * np.sqrt(sq_term)
        
        # Define smooth function for Vout:
        # Vout = Vdd/2 - Vdd/pi * arctan(slope * (Vin - Vm))
        def get_vout(v):
            if v < vthn:
                return vdd
            elif v > (vdd - vthp):
                return 0.0
            else:
                vout_val = (vdd / 2.0) - (vdd / np.pi) * np.arctan(slope * (v - v_m))
                return np.clip(vout_val, 0.0, vdd)
                
        for v in vin_arr:
            vout_arr.append(get_vout(v))
            
        v_oh = get_vout(v_il)
        v_ol = get_vout(v_ih)
        
        nm_l = v_il - v_ol
        nm_h = v_oh - v_ih
                
        fig_vtc = go.Figure()
        # VTC line
        fig_vtc.add_trace(go.Scatter(x=vin_arr, y=vout_arr, mode='lines', 
                                     line=dict(color='#3b82f6', width=4),
                                     name='Inverter VTC',
                                     hovertemplate="Vin: %{x:.2f}V<br>Vout: %{y:.2f}V"))
        
        # Draw switching threshold Vm
        fig_vtc.add_trace(go.Scatter(x=[v_m], y=[vdd/2.0], mode='markers',
                                     marker=dict(size=12, color='#f59e0b', symbol='x'),
                                     name=f'Switching Threshold Vm = {v_m:.2f}V'))
        
        # Add Vil and Voh guideline
        fig_vtc.add_trace(go.Scatter(x=[v_il, v_il, 0], y=[0, v_oh, v_oh], mode='lines+markers',
                                     line=dict(color='#8b5cf6', dash='dash'),
                                     marker=dict(size=6),
                                     name=f'Vil ({v_il:.2f}V), Voh ({v_oh:.2f}V)'))
                                     
        # Add Vih and Vol guideline
        fig_vtc.add_trace(go.Scatter(x=[v_ih, v_ih, 0], y=[0, v_ol, v_ol], mode='lines+markers',
                                     line=dict(color='#10b981', dash='dash'),
                                     marker=dict(size=6),
                                     name=f'Vih ({v_ih:.2f}V), Vol ({v_ol:.2f}V)'))
        
        fig_vtc.update_layout(
            title="Voltage Transfer Characteristic (VTC) with Noise Margin Points",
            xaxis_title="Input Voltage Vin [V]",
            yaxis_title="Output Voltage Vout [V]",
            margin=dict(l=0, r=0, t=40, b=0),
            height=350,
            template="plotly_white"
        )
        st.plotly_chart(fig_vtc, use_container_width=True)
        
        # Output calculated noise margins
        st.markdown(f"""
        <div style="background-color:#eff6ff; padding:1rem; border-radius:12px; border-left:4px solid #3b82f6;">
            <b>📐 Exact VTC Parameters</b><br>
            • Switching Threshold (Vm): <b>{v_m:.2f} V</b><br>
            • Critical Input Voltages: Vil = <b>{v_il:.2f} V</b>, Vih = <b>{v_ih:.2f} V</b><br>
            • Critical Output Voltages: Voh = <b>{v_oh:.2f} V</b>, Vol = <b>{v_ol:.2f} V</b><br>
            • Calculated Noise Margin Low (NM_L = Vil - Vol): <b>{nm_l:.2f} V</b><br>
            • Calculated Noise Margin High (NM_H = Voh - Vih): <b>{nm_h:.2f} V</b>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.header("Power Dissipation & CMOS Advantages")
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.subheader("⚡ Power Dissipation in CMOS")
        st.write("Total power dissipation in CMOS circuits is the sum of two components:")
        
        st.markdown(r"""
        ##### 1. Dynamic Power Dissipation
        This is the power consumed during the switching of output nodes. It has two sub-types:
        - **Capacitive Switching Power**: Power needed to charge/discharge parasitic node capacitors:
          $$P_{switching} = \alpha \cdot C_L \cdot V_{DD}^2 \cdot f$$
          Where $\alpha$ is switching activity factor, $C_L$ load capacitance, $V_{DD}$ supply, and $f$ clock frequency.
        - **Short-Circuit Power**: Occurs during input transitions when both NMOS and PMOS are briefly ON simultaneously, creating a direct path from VDD to GND.
        
        ##### 2. Static Power Dissipation
        Ideally, CMOS logic draws zero static current. However, leakage currents exist:
        - **Sub-threshold leakage**: Current that flows from drain to source when the transistor is nominally OFF ($V_{gs} < V_{th}$).
        - **Gate oxide leakage**: Tunneling of electrons through the extremely thin gate oxide layer.
        - **Junction leakage**: Leakage through the reverse-biased source/drain diffusions.
        """)
        
    with col_p2:
        st.subheader("🌟 Key Advantages of CMOS Technology")
        st.markdown("""
        <div class="custom-card card-green" style="margin-top:0.5rem;">
            <ul>
                <li><b>Near-Zero Static Power</b>: Only one network (PUN or PDN) is active at a time, preventing static DC paths from VDD to Ground.</li>
                <li><b>Full-Rail Output Swing</b>: Output transitions fully to VDD (Logic High) and Ground (Logic Low), yielding higher noise margins.</li>
                <li><b>High Noise Immunity</b>: Large noise margins make CMOS circuits highly resistant to electrical noise and crosstalk.</li>
                <li><b>Symmetric Delay Characteristics</b>: Sizing PMOS to compensate for hole mobility yields balanced rise and fall transition times.</li>
                <li><b>Extreme Scalability</b>: Easy to shrink in size, enabling billions of transistors on a single chip.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

add_footer()
