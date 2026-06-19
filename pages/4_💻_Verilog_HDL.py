import json
import os
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from style_utils import apply_custom_style, add_footer, track_page_visit

st.set_page_config(page_title="Verilog HDL", page_icon="💻", layout="wide")
apply_custom_style()

# Track that this page has been visited
track_page_visit("verilog_basics")

import re

def parse_verilog_assign(code, output_name, inputs_dict):
    # Clean comments and whitespace
    clean = re.sub(r'//.*', '', code)
    clean = re.sub(r'/\*.*?\*/', '', clean, flags=re.DOTALL)
    
    # Search for assign statement for the output_name
    pattern = rf"assign\s+{re.escape(output_name)}\s*=\s*([^;]+);"
    match = re.search(pattern, clean)
    if not match:
        # Search for any assign statement
        match = re.search(r"assign\s+[\w\d_\[\]]+\s*=\s*([^;]+);", clean)
        if not match:
            raise ValueError(f"Could not find any continuous assignment ('assign ... = ...;') for output '{output_name}' in your code.")
            
    expr = match.group(1).strip()
    
    # Handle ternary conditional cascades (sel ? i1 : i0)
    ternary_pattern = r"([^?]+)\?\s*([^:]+):\s*(.+)"
    for _ in range(4): # support nested ternaries up to 4 levels
        t_match = re.search(ternary_pattern, expr)
        if t_match:
            cond = t_match.group(1).strip()
            t_val = t_match.group(2).strip()
            f_val = t_match.group(3).strip()
            expr = f"({t_val}) if ({cond}) else ({f_val})"
            
    # Replace logical operators
    expr = expr.replace("&&", " and ").replace("||", " or ").replace("!", " not ")
    # Replace bitwise NOT operator with subtraction for single bit negation
    expr = expr.replace("~", "1 - ")
    
    # Replace bit-slicing: i[0] -> ((i >> 0) & 1)
    expr = re.sub(r'(\w+)\[(\d+)\]', r'((\1 >> \2) & 1)', expr)
    
    # Replace Verilog binary literals like 4'b0001 or 4'b0000 to Python format
    expr = re.sub(r"\d+'b([01_]+)", r"0b\1", expr)
    
    n = len(list(inputs_dict.values())[0])
    res = []
    for idx in range(n):
        ctx = {}
        for k, val in inputs_dict.items():
            ctx[k] = val[idx]
        try:
            eval_val = eval(expr, {}, ctx)
            res.append(int(eval_val))
        except Exception as e:
            raise ValueError(f"Runtime evaluation error: {str(e)}")
    return res

st.title("💻 Verilog HDL Basics & Examples")

st.markdown("""
<div class="custom-card card-blue">
    <h4>Digital Logic Programming</h4>
    This module introduces Hardware Description Languages (HDLs) and includes 
    <b>100+ Verilog Programming Examples</b> with interactive digital waveform simulators.
</div>
""", unsafe_allow_html=True)

tab_theory, tab_examples = st.tabs(["📚 Verilog Basics Guide", "⚡ 100+ Coding Examples & Simulator"])

# ==========================================
# TAB 1: THEORY GUIDE
# ==========================================
with tab_theory:
    st.header("Verilog HDL Basics")
    
    col_th1, col_th2 = st.columns(2)
    
    with col_th1:
        with st.expander("1. Introduction to Verilog", expanded=True):
            st.write("""
            **Verilog** is a Hardware Description Language (HDL) used to model and simulate electronic systems. 
            Unlike software programming languages (like C or Python), Verilog code is concurrent, meaning many actions occur in parallel.
            It describes actual hardware connections, logic gates, and registers that are synthesized into silicon.
            """)
            
        with st.expander("2. Module Structure"):
            st.write("""
            The primary building block in Verilog is the **module**. It defines the input/output ports and containing logic.
            """)
            st.code("""
module my_design(
    input clk,       // Input port
    input reset,     // Input port
    input [3:0] data_in, // 4-bit bus input
    output reg [3:0] q // 4-bit bus output
);
    // Logic statements go here
    always @(posedge clk or posedge reset) begin
        if (reset) q <= 4'b0000;
        else q <= data_in;
    end
endmodule
            """, language="verilog")

        with st.expander("3. Data Types"):
            st.write("""
            Verilog has two primary data groups:
            - **Nets (e.g., `wire`)**: Represent physical connections between hardware elements. They do not store values; they must be driven continuously by gates or `assign` statements.
            - **Registers (e.g., `reg`)**: Represent variables that store data. They retain values until another assignment overrides them. Note: a `reg` in Verilog code does *not* always translate to a physical D flip-flop register; it depends on the synthesis context.
            - **Parameters**: constants (e.g., `parameter WIDTH = 8;`).
            """)

        with st.expander("4. Operators"):
            st.markdown("""
            - **Arithmetic**: `+`, `-`, `*`, `/`, `%`
            - **Bitwise**: `~` (NOT), `&` (AND), `|` (OR), `^` (XOR), `~^` (XNOR)
            - **Reduction**: Performs bitwise operation on a single vector, yielding a 1-bit output: `&data` (AND all bits of data bus together)
            - **Logical**: `!`, `&&`, `||`
            - **Relational**: `<`, `>`, `<=`, `>=`, `==`, `!=`
            - **Shift**: `<<` (left shift), `>>` (right shift)
            - **Conditional**: `sel ? input_a : input_b` (ternary operator)
            """)
            st.write("""
            ##### Detailed Highlight: Concatenation `{}` & Replication `{{}}`
            These operators are unique to HDLs and are heavily used to manipulate bus structures:
            - **Concatenation `{a, b}`**: Combines multiple smaller vectors into a single larger vector.
            - **Replication `{n{a}}`**: Repeats a vector `a` exactly `n` times. Very commonly used for **sign extension** of signed numbers.
            """)
            st.code("""
wire [3:0] a = 4'b1010;
wire [3:0] b = 4'b0110;
wire [7:0] combined;
assign combined = {a, b}; // combined becomes 8'b1010_0110

// Sign Extension of 4-bit 'a' to 8-bit output:
wire [7:0] sign_extended;
assign sign_extended = {{4{a[3]}}, a}; // repeats MSB 4 times -> 8'b1111_1010
            """, language="verilog")

    with col_th2:
        with st.expander("5. Assign Statement (Dataflow Modeling)", expanded=True):
            st.write("""
            Used for continuous assignments on **wires**. The RHS value is continuously calculated and transferred to the LHS.
            """)
            st.code("""
wire sum, a, b, cin;
assign sum = a ^ b ^ cin; // Re-evaluates instantly when a, b, or cin changes
            """, language="verilog")

        with st.expander("6. Always Block (Behavioral Modeling)"):
            st.write("""
            Executes when triggered by a change in signals defined in the **sensitivity list**.
            
            ##### Sensitivity List triggers:
            - `always @(a or b)` : combinational logic (re-evaluates on any input change)
            - `always @(*)` : automatic sensitivity list for combinational logic
            - `always @(posedge clk)` : sequential logic (re-evaluates on positive edge of the clock)
            
            ##### Assignment Rules:
            1. **Blocking Assignments (`=`)**: Evaluated sequentially (similar to software). Used in combinational `always` blocks.
            2. **Non-Blocking Assignments (`<=`)**: Evaluated in parallel at the end of the time step. Used in sequential `always @(posedge clk)` blocks to avoid race conditions.
            """)
            
        with st.expander("7. Testbench Basics"):
            st.write("""
            A **testbench** is a non-synthesizable Verilog module used to apply stimuli to the Device Under Test (DUT) and verify its outputs.
            """)
            st.code("""
`timescale 1ns/1ps
module my_tb;
    reg clk;
    reg reset;
    wire [3:0] q;
    
    // Instantiate DUT (Device Under Test)
    my_design dut (.clk(clk), .reset(reset), .data_in(4'b1010), .q(q));
    
    // Generate Clock
    initial begin
        clk = 0;
        forever #5 clk = ~clk; // 10ns period clock
    end
    
    // Generate Stimulus
    initial begin
        reset = 1;
        #15 reset = 0; // release reset
        #100 $finish;  // terminate simulator
    end
endmodule
            """, language="verilog")

        with st.expander("8. Synthesizable Verilog Rules"):
            st.write("""
            Writing synthesizable code requires adhering to strict coding guidelines so the EDA synthesis tool can map it to actual logic gates:
            
            ##### 1. Avoid Unintentional Latch Generation
            In combinational blocks (e.g., `always @(*)`), if an output is not assigned a value under *all* possible branches, the synthesis tool generates a latch to remember its previous state. Latch timing is hard to analyze.
            - **Fix**: Always include a `default` case in case statements, and an `else` branch for every `if` statement.
            
            ##### 2. Synthesis vs. Simulation constructs
            - **Synthesizable**: `always`, `assign`, `module`, `parameter`, `if`, `case`, `for` (with static limits).
            - **Non-Synthesizable (Sim-only)**: `#delay` (e.g., `#5`), `initial` blocks, `$display`, `$monitor`, `$finish`, `real` data types.
            
            ##### 3. FSM State Encoding Styles
            - **Binary**: States represented as standard binary counts (e.g., 00, 01, 10, 11). Uses fewer registers but requires complex combinational decoding logic.
            - **Gray Code**: Only 1 bit changes state at a time. Reduces switching power and prevents transient glitch hazards.
            - **One-Hot**: Uses one flip-flop per state (e.g. 4'b0001, 4'b0010, 4'b0100, 4'b1000). Decoding is extremely fast and simple, ideal for high-speed systems, though it consumes more registers.
            """)
            
        with st.expander("9. Tasks, Functions & Parameter Overrides"):
            st.write("""
            To create modular, reusable HDL blocks, Verilog provides advanced functions and parameterization structures:
            
            ##### 1. Tasks vs. Functions
            - **Functions**: Run in zero simulation time. Cannot contain delay statements (`#`, `@`, `wait`). Can only return a single value and cannot have `output` or `inout` ports.
            - **Tasks**: Can consume simulation time (can contain delays). Can have multiple `input`, `output`, and `inout` ports, but do not return a direct value.
            
            ##### 2. Parameterized Modules
            Define a module with generic parameters that can be overridden at instantiation:
            """)
            st.code("""
module register #(parameter WIDTH = 8)(
    input clk, rst,
    input [WIDTH-1:0] d,
    output reg [WIDTH-1:0] q
);
    always @(posedge clk) begin
        if (rst) q <= 0;
        else q <= d;
    end
endmodule

// Overriding parameter on instantiation:
register #(.WIDTH(16)) reg16 (.clk(clk), .rst(rst), .d(data_16), .q(out_16));
            """, language="verilog")

        with st.expander("10. Concept: Synchronous vs. Asynchronous Resets"):
            st.write("""
            A reset signal brings the sequential digital circuit into a known initial state. There are two primary reset styles in ASIC designs:
            
            ##### 1. Asynchronous Reset
            The reset takes effect immediately, independent of the clock. The reset signal must be in the sensitivity list of the `always` block.
            - **Advantage**: Circuit resets even if the clock is not running. Saves power during reset.
            - **Disadvantage**: Susceptible to glitches on the reset line. Latch-up/metastability issues can occur if reset is released too close to the active clock edge (recovery/removal violations).
            """)
            st.code("""
// Asynchronous Active-Low Reset D-FF
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) 
        q <= 0;
    else 
        q <= d;
end
            """, language="verilog")
            st.write("""
            ##### 2. Synchronous Reset
            The reset is sampled on the active edge of the clock. Reset signal is **not** in the sensitivity list.
            - **Advantage**: Immune to glitches on the reset line. Simpler static timing analysis.
            - **Disadvantage**: The circuit will not reset unless a valid clock pulse is running.
            """)
            st.code("""
// Synchronous Active-Low Reset D-FF
always @(posedge clk) begin
    if (!rst_n) 
        q <= 0;
    else 
        q <= d;
end
            """, language="verilog")

# ==========================================
# TAB 2: 100+ CODING EXAMPLES & SIMULATOR
# ==========================================
with tab_examples:
    st.header("Verilog Code Library & Waveform Viewer")
    st.write("Choose a code module to review the theory, structural RTL code, testbench code, and view simulated waveforms.")
    
    # Load database
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    v_db_path = os.path.join(parent_dir, "verilog_db.json")
    try:
        with open(v_db_path, "r", encoding="utf-8") as f:
            v_db = json.load(f)
    except Exception as e:
        v_db = {}

    category = st.radio(
        "Choose Category:",
        ["1. Basic Logic Gates (Gate level)", "2. Combinational Circuits (Data flow)", "3. Sequential Circuits (Behavioral)", "4. Finite State Machines (FSM)"],
        horizontal=True
    )
    
    # Filter selection lists based on category
    prog_keys = [k for k, v in v_db.items() if v.get("category") == category]
    try:
        prog_keys = sorted(prog_keys, key=lambda x: int(x.split(".")[0]))
    except Exception:
        pass
        
    selected_program = st.selectbox("Select Program:", prog_keys if prog_keys else ["No programs found"])
    
    program_key = selected_program
    prog_data = v_db.get(program_key, {})
    
    st.write(prog_data.get("desc", ""))
    
    # Track completion in session state
    st.session_state.progress["verilog_completed"][program_key] = True
    
    col_code, col_sim = st.columns([1, 1], gap="large")
    
    with col_code:
        st.markdown("**💻 Verilog Codes**")
        code_tabs = st.tabs(["Edit RTL Design Code", "Testbench Code"])
        with code_tabs[0]:
            user_rtl = st.text_area(
                "Modify the RTL code (specifically the continuous assignments!):",
                value=prog_data.get("rtl", ""),
                height=220,
                key=f"editor_{program_key}"
            )
            # Add notice for sequential/FSM logic or non-editable combinational logic
            allow_edit = prog_data.get("allow_edit", False)
            if not allow_edit:
                st.caption("ℹ️ *Complex/Sequential/FSM simulations use precompiled logic models. Edits to RTL code won't alter the waveform results.*")
        with code_tabs[1]:
            st.code(prog_data.get("tb", ""), language="verilog")
            
    with col_sim:
        st.markdown("**📊 Interactive Waveform Simulator**")
        st.write("Click below to run a mock simulator testbench and generate real-time logic graphs:")
        
        sim_btn = st.button("Run Simulation", key=f"sim_{program_key}")
        
        if sim_btn:
            steps = 10
            x_time = list(range(steps))
            fig = go.Figure()
            
            # Gather inputs for parsing
            inputs_map = {}
            for t in prog_data.get("traces", []):
                if not t.get("is_output"):
                    in_var = t.get("expr_var", t["name"].split()[-1].lower())
                    inputs_map[in_var] = t["vals"]
                    
            custom_sim_success = False
            custom_sim_error = None
            
            # Plot traces
            for t in prog_data.get("traces", []):
                name = t["name"]
                offset = t.get("offset", 0.0)
                color = t.get("color", None)
                
                if t.get("is_output") and allow_edit:
                    try:
                        out_var = t.get("expr_var", t["name"].split()[-1].lower())
                        y_vals = parse_verilog_assign(user_rtl, out_var, inputs_map)
                        custom_sim_success = True
                    except Exception as e:
                        custom_sim_error = str(e)
                        y_vals = t["vals"]
                else:
                    y_vals = t["vals"]
                    
                line_shape = "hv"
                width = 3
                if t.get("is_output"):
                    width = 4
                    if not color:
                        color = "#ef4444"
                
                plot_y = [v + offset for v in y_vals]
                
                line_dict = dict(width=width)
                if color:
                    line_dict["color"] = color
                    
                fig.add_trace(go.Scatter(
                    x=x_time,
                    y=plot_y,
                    name=name,
                    line_shape=line_shape,
                    line=line_dict
                ))
                
            if allow_edit:
                if custom_sim_success:
                    st.success("🎉 Custom Verilog RTL parsed and simulated successfully!")
                elif custom_sim_error:
                    st.error(f"❌ Verilog Lint/Compiler Error: {custom_sim_error}")
                    st.warning("⚠️ Simulation falling back to original code behavior.")
            
            # Dynamically build y-axis ticks based on trace offsets to prevent weird floating offsets
            y_ticks = {}
            for t in prog_data.get("traces", []):
                offset = t.get("offset", 0.0)
                vals = t.get("vals", [])
                if not vals:
                    continue
                unique_vals = sorted(list(set(vals)))
                is_binary = all(v in (0, 1) for v in unique_vals)
                
                if is_binary:
                    y_ticks[offset] = "L"
                    y_ticks[offset + 1.0] = "H"
                else:
                    for v in unique_vals:
                        y_ticks[offset + v] = str(v)
            
            # Sort ticks by value
            sorted_ticks = sorted(y_ticks.items())
            tickvals = [item[0] for item in sorted_ticks]
            ticktext = [item[1] for item in sorted_ticks]
                    
            fig.update_layout(
                title=f"Timing Diagram Analysis: {selected_program}",
                xaxis_title="Simulation Timeline / Time steps",
                xaxis=dict(tickvals=x_time),
                yaxis=dict(tickvals=tickvals, ticktext=ticktext),
                margin=dict(l=0, r=0, t=40, b=0),
                height=350,
                legend=dict(x=0.01, y=0.99, orientation="h"),
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.success("✅ Waveform generation complete. Analyzed logic transition values are plotted above.")
        else:
            st.info("💡 Click the 'Run Simulation' button to load the logic testbench and view the timing diagram waveform.")

add_footer()
