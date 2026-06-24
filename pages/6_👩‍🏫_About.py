import streamlit as st
from style_utils import apply_custom_style, add_footer

import base64

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception:
        return ""

st.set_page_config(page_title="About the Developer", page_icon="👩‍🏫", layout="wide")
apply_custom_style()

st.title("👩‍🏫 Faculty Profile")

col1, col2 = st.columns([1, 2])

with col1:
    img_b64 = get_base64_image("dr_sumitra_avatar.jpg")
    st.markdown(f"""
        <div style="text-align: center;">
            <img src="data:image/jpeg;base64,{img_b64}" style="width:200px; height:200px; border-radius: 50%; object-fit: cover; border: 5px solid #1e3a8a; margin-bottom: 20px;">
            <h2 style="white-space: nowrap;">
    Dr. Sumitra V
</h2>
            <p style="color: #6b7280; font-size: 1.1rem;">Assistant Professor</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="custom-card" style="border-left-color: #1e3a8a;">
            <h4>📍 Contact Information</h4>
            <p>📧 sumitrav@srmist.edu.in</p>
            <p>🏢 ECE Department, SRMIST</p>
            <p>🔗 <a href="#">LinkedIn Profile</a> | <a href="#">Google Scholar</a></p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="custom-card">
            <h3>Academic Background</h3>
            <p>Dr. Sumitra V is a dedicated educator and researcher at <b>SRM Institute of Science and Technology</b>. With years of expertise in VLSI and Embedded Systems, she has mentored numerous undergraduate and postgraduate students in cutting-edge hardware design projects.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🔬 Research & Specializations")
    
    # Using columns for research interests
    r1, r2 = st.columns(2)
    with r1:
        st.success("**VLSI & FPGA Design**")
        st.write("Specializing in high-speed, low-power architectural optimizations and hardware accelerators.")
        
        st.success("**Embedded Systems**")
        st.write("Designing robust systems for IoT and real-time applications.")

    with r2:
        st.success("**Network-on-Chip (NoC)**")
        st.write("Exploring scalable communication subsystems for modern many-core System-on-Chips.")
        
        st.success("**Digital System Design**")
        st.write("Expertise in Verilog HDL and ASIC design methodologies.")

    st.divider()
    
    st.subheader("🎓 Professional Highlights")
    st.markdown("""
    - **Faculty Advisor**: Leading student teams in national-level design competitions.
    - **Publication Record**: Multiple papers in IEEE and Scopus-indexed journals.
    - **Industrial Collaboration**: Working on hardware acceleration projects.
    """)

add_footer()
