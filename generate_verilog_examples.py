import json
import os

def generate_examples():
    db = {}
    item_count = 1

    # Helper to format and add examples
    def add_item(category, name, desc, rtl, tb, traces, is_comb=True, allow_edit=False):
        nonlocal item_count
        key = f"{item_count}. {name}"
        db[key] = {
            "category": category,
            "desc": desc,
            "rtl": rtl.strip(),
            "tb": tb.strip(),
            "is_combinational": is_comb,
            "allow_edit": allow_edit,
            "traces": traces
        }
        item_count += 1

    # -------------------------------------------------------------
    # 1. Basic Logic Gates (Gate level) - 11 Examples
    # -------------------------------------------------------------
    gates = [
        ("AND Gate", "and", "a & b", "Output is High only if both inputs are High."),
        ("OR Gate", "or", "a | b", "Output is High if at least one input is High."),
        ("NOT Gate", "not", "~a & 1", "Output is the logical inversion of the input."),
        ("NAND Gate", "nand", "~(a & b) & 1", "Output is Low only if both inputs are High."),
        ("NOR Gate", "nor", "~(a | b) & 1", "Output is High only if all inputs are Low."),
        ("XOR Gate", "xor", "a ^ b", "Output is High only if inputs are different."),
        ("XNOR Gate", "xnor", "~(a ^ b) & 1", "Output is High only if inputs are identical."),
        ("Buffer", "buf", "a", "Passes input to output, strengthening signal drive."),
        ("3-input AND Gate", "and3", "a & b & c", "Three-input AND gate logic."),
        ("3-input OR Gate", "or3", "a | b | c", "Three-input OR gate logic.")
    ]

    for name, op, expr, desc in gates:
        is_3in = "3-input" in name
        is_not = "NOT" in name or "Buffer" in name
        
        if is_3in:
            rtl = f"""module {op}_gate(
    input a,
    input b,
    input c,
    output y
);
    assign y = {expr.replace('& 1', '')};
endmodule"""
            a_vals = [0, 1, 1, 1, 0, 1, 1, 1, 0, 1]
            b_vals = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
            c_vals = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
            y_vals = [eval(expr, {}, {"a": av, "b": bv, "c": cv}) for av, bv, cv in zip(a_vals, b_vals, c_vals)]
            traces = [
                {"name": "Input A", "vals": a_vals, "color": "#3b82f6", "offset": 3.75},
                {"name": "Input B", "vals": b_vals, "color": "#10b981", "offset": 2.5},
                {"name": "Input C", "vals": c_vals, "color": "#8b5cf6", "offset": 1.25},
                {"name": "Output Y", "vals": y_vals, "color": "#ef4444", "offset": 0.0, "is_output": True}
            ]
            tb = f"""`timescale 1ns/1ps
module tb_{op}_gate;
    reg a, b, c;
    wire y;

    {op}_gate uut (
        .a(a),
        .b(b),
        .c(c),
        .y(y)
    );

    initial begin
        a = 0; b = 0; c = 0; #10;
        a = 1; b = 0; c = 0; #10;
        a = 1; b = 1; c = 0; #10;
        a = 1; b = 1; c = 1; #10;
        a = 0; b = 1; c = 1; #10;
        $finish;
    end
endmodule"""
        elif is_not:
            rtl = f"""module {op}_gate(
    input a,
    output y
);
    assign y = {expr.replace('& 1', '')};
endmodule"""
            a_vals = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
            y_vals = [eval(expr, {}, {"a": av}) for av in a_vals]
            traces = [
                {"name": "Input A", "vals": a_vals, "color": "#3b82f6", "offset": 1.25},
                {"name": "Output Y", "vals": y_vals, "color": "#ef4444", "offset": 0.0, "is_output": True}
            ]
            tb = f"""`timescale 1ns/1ps
module tb_{op}_gate;
    reg a;
    wire y;

    {op}_gate uut (
        .a(a),
        .y(y)
    );

    initial begin
        a = 0; #10;
        a = 1; #10;
        a = 0; #10;
        a = 1; #10;
        $finish;
    end
endmodule"""
        else:
            rtl = f"""module {op}_gate(
    input a,
    input b,
    output y
);
    assign y = {expr.replace('& 1', '')};
endmodule"""
            a_vals = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
            b_vals = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
            y_vals = [eval(expr, {}, {"a": av, "b": bv}) for av, bv in zip(a_vals, b_vals)]
            traces = [
                {"name": "Input A", "vals": a_vals, "color": "#3b82f6", "offset": 2.5},
                {"name": "Input B", "vals": b_vals, "color": "#10b981", "offset": 1.25},
                {"name": "Output Y", "vals": y_vals, "color": "#ef4444", "offset": 0.0, "is_output": True}
            ]
            tb = f"""`timescale 1ns/1ps
module tb_{op}_gate;
    reg a, b;
    wire y;

    {op}_gate uut (
        .a(a),
        .b(b),
        .y(y)
    );

    initial begin
        a = 0; b = 0; #10;
        a = 0; b = 1; #10;
        a = 1; b = 0; #10;
        a = 1; b = 1; #10;
        $finish;
    end
endmodule"""
        add_item("1. Basic Logic Gates (Gate level)", name, desc, rtl, tb, traces, allow_edit=True)

    # Tri-state buffer
    rtl_tri = """module tristate_buf(
    input a,
    input en,
    output y
);
    assign y = en ? a : 1'bz;
endmodule"""
    tb_tri = """`timescale 1ns/1ps
module tb_tristate;
    reg a;
    reg en;
    wire y;

    tristate_buf uut (
        .a(a),
        .en(en),
        .y(y)
    );

    initial begin
        a = 0; en = 0; #10;
        a = 1; en = 0; #10;
        a = 1; en = 1; #10;
        a = 0; en = 1; #10;
        $finish;
    end
endmodule"""
    traces_tri = [
        {"name": "Input A", "vals": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1], "color": "#3b82f6", "offset": 2.5},
        {"name": "Enable EN", "vals": [0, 0, 1, 1, 0, 0, 1, 1, 0, 0], "color": "#10b981", "offset": 1.25},
        {"name": "Output Y (Hi-Z represented as 0)", "vals": [0, 0, 0, 1, 0, 0, 0, 1, 0, 0], "color": "#ef4444", "offset": 0.0, "is_output": True}
    ]
    add_item("1. Basic Logic Gates (Gate level)", "Tri-state Buffer", "Passes input A when active-high enable EN is true, otherwise high impedance.", rtl_tri, tb_tri, traces_tri, allow_edit=False)


    # -------------------------------------------------------------
    # 2. Combinational Circuits (Data flow) - 37 Examples
    # -------------------------------------------------------------
    comb_circuits = [
        ("Half Adder", "Half adder computing sum and carry outputs for two input bits.",
         """module half_adder(input a, input b, output sum, output cout);
    assign sum = a ^ b;
    assign cout = a & b;
endmodule""",
         """`timescale 1ns/1ps
module tb_half_adder;
    reg a, b;
    wire sum, cout;
    half_adder uut (.*);
    initial begin
        a = 0; b = 0; #10;
        a = 0; b = 1; #10;
        a = 1; b = 0; #10;
        a = 1; b = 1; #10;
        $finish;
    end
endmodule""",
         [
             {"name": "Input A", "vals": [0,0,1,1,0,0,1,1,0,0], "offset": 3.75},
             {"name": "Input B", "vals": [0,1,0,1,0,1,0,1,0,1], "offset": 2.5},
             {"name": "Output Sum", "vals": [0,1,1,0,0,1,1,0,0,1], "offset": 1.25, "is_output": True, "expr_var": "sum"},
             {"name": "Output Carry", "vals": [0,0,0,1,0,0,0,1,0,0], "offset": 0.0, "is_output": True, "expr_var": "cout"}
         ], True), # allow edit
         
        ("Full Adder", "Full adder module with carry-in support.",
         """module full_adder(input a, input b, input cin, output sum, output cout);
    assign sum = a ^ b ^ cin;
    assign cout = (a & b) | (b & cin) | (cin & a);
endmodule""",
         """`timescale 1ns/1ps
module tb_full_adder;
    reg a, b, cin;
    wire sum, cout;
    full_adder uut (.*);
    initial begin
        a = 0; b = 0; cin = 0; #10;
        a = 0; b = 1; cin = 0; #10;
        a = 1; b = 0; cin = 0; #10;
        a = 1; b = 1; cin = 0; #10;
        a = 0; b = 0; cin = 1; #10;
        a = 0; b = 1; cin = 1; #10;
        a = 1; b = 0; cin = 1; #10;
        a = 1; b = 1; cin = 1; #10;
        $finish;
    end
endmodule""",
         [
             {"name": "Input A", "vals": [0,0,1,1,0,0,1,1,0,0], "offset": 4.5},
             {"name": "Input B", "vals": [0,1,0,1,0,1,0,1,0,1], "offset": 3.25},
             {"name": "Carry-in Cin", "vals": [0,0,0,0,1,1,1,1,0,0], "offset": 2.0, "expr_var": "cin"},
             {"name": "Output Sum", "vals": [0,1,1,0,1,0,0,1,0,1], "offset": 1.0, "is_output": True, "expr_var": "sum"},
             {"name": "Output Cout", "vals": [0,0,0,1,0,1,1,1,0,0], "offset": 0.0, "is_output": True, "expr_var": "cout"}
         ], True),
         
        ("Half Subtractor", "Subtracts input b from a to yield difference and borrow out.",
         """module half_subtractor(input a, input b, output diff, output borrow);
    assign diff = a ^ b;
    assign borrow = ~a & b;
endmodule""",
         """`timescale 1ns/1ps
module tb_half_subtractor;
    reg a, b;
    wire diff, borrow;
    half_subtractor uut (.*);
    initial begin
        a = 0; b = 0; #10;
        a = 0; b = 1; #10;
        a = 1; b = 0; #10;
        a = 1; b = 1; #10;
        $finish;
    end
endmodule""",
         [
             {"name": "Input A", "vals": [0,0,1,1,0,0,1,1,0,0], "offset": 3.75},
             {"name": "Input B", "vals": [0,1,0,1,0,1,0,1,0,1], "offset": 2.5},
             {"name": "Output Difference", "vals": [0,1,1,0,0,1,1,0,0,1], "offset": 1.25, "is_output": True, "expr_var": "diff"},
             {"name": "Output Borrow", "vals": [0,1,0,0,0,1,0,0,0,1], "offset": 0.0, "is_output": True, "expr_var": "borrow"}
         ], True),
         
        ("Full Subtractor", "Three-input subtractor yielding difference and borrow.",
         """module full_subtractor(input a, input b, input bin, output diff, output borrow);
    assign diff = a ^ b ^ bin;
    assign borrow = (~a & b) | (~(a ^ b) & bin);
endmodule""",
         """`timescale 1ns/1ps
module tb_full_subtractor;
    reg a, b, bin;
    wire diff, borrow;
    full_subtractor uut (.*);
    initial begin
        a = 0; b = 0; bin = 0; #10;
        a = 0; b = 1; bin = 0; #10;
        a = 1; b = 0; bin = 0; #10;
        a = 1; b = 1; bin = 0; #10;
        a = 0; b = 0; bin = 1; #10;
        a = 0; b = 1; bin = 1; #10;
        a = 1; b = 0; bin = 1; #10;
        a = 1; b = 1; bin = 1; #10;
        $finish;
    end
endmodule""",
         [
             {"name": "Input A", "vals": [0,0,1,1,0,0,1,1,0,0], "offset": 4.5},
             {"name": "Input B", "vals": [0,1,0,1,0,1,0,1,0,1], "offset": 3.25},
             {"name": "Borrow-in Bin", "vals": [0,0,0,0,1,1,1,1,0,0], "offset": 2.0, "expr_var": "bin"},
             {"name": "Output Diff", "vals": [0,1,1,0,1,0,0,1,0,1], "offset": 1.0, "is_output": True, "expr_var": "diff"},
             {"name": "Output Borrow", "vals": [0,1,0,0,1,1,0,1,0,1], "offset": 0.0, "is_output": True, "expr_var": "borrow"}
         ], True),
         
        ("2:1 Multiplexer", "Dataflow multiplexer selecting between inputs i0 and i1 based on sel.",
         """module mux2(input i0, input i1, input sel, output y);
    assign y = sel ? i1 : i0;
endmodule""",
         """`timescale 1ns/1ps
module tb_mux2;
    reg i0, i1, sel;
    wire y;
    mux2 uut (.*);
    initial begin
        i0 = 0; i1 = 1; sel = 0; #10;
        sel = 1; #10;
        i0 = 1; i1 = 0; sel = 0; #10;
        sel = 1; #10;
        $finish;
    end
endmodule""",
         [
             {"name": "Input I0", "vals": [0,0,0,0,1,1,1,1,0,0], "offset": 3.5, "expr_var": "i0"},
             {"name": "Input I1", "vals": [1,1,1,1,0,0,0,0,1,1], "offset": 2.25, "expr_var": "i1"},
             {"name": "Selector Sel", "vals": [0,1,0,1,0,1,0,1,0,1], "offset": 1.25, "expr_var": "sel"},
             {"name": "Output Y", "vals": [0,1,0,1,1,0,1,0,0,1], "offset": 0.0, "is_output": True, "expr_var": "y"}
         ], True)
    ]

    for name, desc, rtl, tb, traces, allow_edit in comb_circuits:
        add_item("2. Combinational Circuits (Data flow)", name, desc, rtl, tb, traces, allow_edit=allow_edit)

    # Multiplexers (4:1 to 64:1)
    def add_mux(size):
        sel_bits = (size - 1).bit_length()
        rtl = f"""module mux{size}(
    input [{size-1}:0] i,
    input [{sel_bits-1}:0] sel,
    output y
);
    assign y = i[sel];
endmodule"""
        tb = f"""`timescale 1ns/1ps
module tb_mux{size};
    reg [{size-1}:0] i;
    reg [{sel_bits-1}:0] sel;
    wire y;

    mux{size} uut (
        .i(i),
        .sel(sel),
        .y(y)
    );

    initial begin
        i = {size}'h5555_5555_5555_5555 & (({size}'d1 << {size-1}) - 1);
        sel = 0;
        #10;
        repeat ({size}) begin
            #10 sel = sel + 1;
        end
        #10;
        i = ~i;
        sel = 0;
        repeat ({size}) begin
            #10 sel = sel + 1;
        end
        #10;
        $finish;
    end
endmodule"""
        sel_vals = [idx % size for idx in range(10)]
        y_vals = [(1 if idx % 2 == 0 else 0) for idx in range(10)]
        traces = [
            {"name": f"Selector Sel (0 to {size-1})", "vals": sel_vals, "color": "#8b5cf6", "offset": 1.25},
            {"name": "Output Y", "vals": y_vals, "color": "#ef4444", "offset": 0.0, "is_output": True}
        ]
        add_item("2. Combinational Circuits (Data flow)", f"{size}:1 Multiplexer", f"Dataflow multiplexer routing one of {size} input lines.", rtl, tb, traces, allow_edit=False)

    for s in [4, 8, 16, 32, 64]:
        add_mux(s)

    # Demultiplexers
    def add_demux(size):
        sel_bits = (size - 1).bit_length()
        rtl = f"""module demux{size}(
    input i,
    input [{sel_bits-1}:0] sel,
    output [{size-1}:0] y
);
    assign y = i << sel;
endmodule"""
        tb = f"""`timescale 1ns/1ps
module tb_demux{size};
    reg i;
    reg [{sel_bits-1}:0] sel;
    wire [{size-1}:0] y;

    demux{size} uut (
        .i(i),
        .sel(sel),
        .y(y)
    );

    initial begin
        i = 1;
        sel = 0;
        #10;
        repeat ({size}) begin
            #10 sel = sel + 1;
        end
        i = 0;
        sel = 0;
        repeat ({size}) begin
            #10 sel = sel + 1;
        end
        #10;
        $finish;
    end
endmodule"""
        sel_vals = [idx % size for idx in range(10)]
        traces = [
            {"name": "Data Input I", "vals": [1]*10, "color": "#3b82f6", "offset": 2.5},
            {"name": "Select Sel", "vals": sel_vals, "color": "#8b5cf6", "offset": 1.25},
            {"name": "Output Line 0 (Y[0])", "vals": [(1 if (idx % size == 0) else 0) for idx in range(10)], "color": "#ef4444", "offset": 0.0, "is_output": True}
        ]
        add_item("2. Combinational Circuits (Data flow)", f"1-to-{size} Demultiplexer", f"Splits 1 input line into {size} output lines.", rtl, tb, traces, allow_edit=False)

    for s in [2, 4, 8, 16, 32]:
        add_demux(s)

    # Decoders
    def add_decoder(in_size):
        out_size = 2**in_size
        rtl = f"""module decoder_{in_size}to{out_size}(
    input [{in_size-1}:0] x,
    output [{out_size-1}:0] y
);
    assign y = 1 << x;
endmodule"""
        tb = f"""`timescale 1ns/1ps
module tb_dec{in_size}_{out_size};
    reg [{in_size-1}:0] x;
    wire [{out_size-1}:0] y;

    decoder_{in_size}to{out_size} uut (
        .x(x),
        .y(y)
    );

    initial begin
        x = 0;
        #10;
        repeat ({out_size}) begin
            #10 x = x + 1;
        end
        #10;
        $finish;
    end
endmodule"""
        addr_vals = [idx % out_size for idx in range(10)]
        traces = [
            {"name": f"Address Input X (Dec)", "vals": addr_vals, "color": "#3b82f6", "offset": 1.25},
            {"name": "Decoded Output Bit 0", "vals": [(1 if (idx % out_size == 0) else 0) for idx in range(10)], "color": "#ef4444", "offset": 0.0, "is_output": True}
        ]
        add_item("2. Combinational Circuits (Data flow)", f"{in_size}-to-{out_size} Decoder", f"Translates a {in_size}-bit address into {out_size} mutual-exclusive lines.", rtl, tb, traces, allow_edit=False)

    for s in [2, 3, 4, 5]:
        add_decoder(s)

    # Adders
    def add_adder(bits):
        rtl = f"""module adder{bits}(
    input [{bits-1}:0] a,
    input [{bits-1}:0] b,
    output [{bits-1}:0] sum,
    output cout
);
    assign {{cout, sum}} = a + b;
endmodule"""
        if bits == 1:
            tb_stim = """a = 0; b = 0; #10;
        a = 1; b = 0; #10;
        a = 0; b = 1; #10;
        a = 1; b = 1; #10;"""
        else:
            tb_stim = f"""a = 0; b = 0; #10;
        a = {bits}'d5; b = {bits}'d10; #10;
        a = ({bits}'d1 << {bits-1}) - 1; b = {bits}'d1; #10;
        a = ({bits}'d1 << {bits-1}); b = ({bits}'d1 << {bits-1}); #10;"""
        tb = f"""`timescale 1ns/1ps
module tb_adder{bits};
    reg [{bits-1}:0] a;
    reg [{bits-1}:0] b;
    wire [{bits-1}:0] sum;
    wire cout;

    adder{bits} uut (
        .a(a),
        .b(b),
        .sum(sum),
        .cout(cout)
    );

    initial begin
        {tb_stim}
        $finish;
    end
endmodule"""
        a_vals = [2, 5, 8, 1, 9, 4, 3, 10, 1, 0]
        b_vals = [1, 2, 3, 4, 5, 6, 7, 8, 0, 0]
        y_vals = [(a+b) % (2**bits) for a, b in zip(a_vals, b_vals)]
        traces = [
            {"name": "Input A (Dec representation)", "vals": a_vals, "color": "#3b82f6", "offset": 2.5},
            {"name": "Input B (Dec representation)", "vals": b_vals, "color": "#10b981", "offset": 1.25},
            {"name": f"Sum Output (Dec modulo {2**bits})", "vals": y_vals, "color": "#ef4444", "offset": 0.0, "is_output": True}
        ]
        add_item("2. Combinational Circuits (Data flow)", f"{bits}-bit Binary Adder", f"Ripple carry adder block of width {bits} bits.", rtl, tb, traces, allow_edit=False)

    for b in [1, 2, 4, 8, 16, 32]:
        add_adder(b)

    # Remaining combinational blocks (Subtractors, Comparators, ALUs)
    comb_others = [
        ("Half Subtractor (Alternative)", "Difference & Borrow logic for 2 bits.",
         """module half_sub_alt(input a, input b, output diff, output borrow);
    assign diff = a ^ b;
    assign borrow = ~a & b;
endmodule""",
         """`timescale 1ns/1ps
module tb_half_sub_alt;
    reg a, b;
    wire diff, borrow;
    half_sub_alt uut (.*);
    initial begin
        a = 0; b = 0; #10;
        a = 0; b = 1; #10;
        a = 1; b = 0; #10;
        a = 1; b = 1; #10;
        $finish;
    end
endmodule"""),
         
        ("Full Subtractor (Alternative)", "3-input borrow subtractor.",
         """module full_sub_alt(input a, input b, input bin, output diff, output borrow);
    assign diff = a ^ b ^ bin;
    assign borrow = (~a & b) | (~(a ^ b) & bin);
endmodule""",
         """`timescale 1ns/1ps
module tb_full_sub_alt;
    reg a, b, bin;
    wire diff, borrow;
    full_sub_alt uut (.*);
    initial begin
        a = 0; b = 0; bin = 0; #10;
        a = 0; b = 1; bin = 0; #10;
        a = 1; b = 0; bin = 1; #10;
        a = 1; b = 1; bin = 1; #10;
        $finish;
    end
endmodule"""),
         
        ("2-bit Comparator", "2-bit comparative logic.",
         """module comp2(input [1:0] a, input [1:0] b, output eq, output gt, output lt);
    assign eq = (a == b);
    assign gt = (a > b);
    assign lt = (a < b);
endmodule""",
         """`timescale 1ns/1ps
module tb_comp2;
    reg [1:0] a, b;
    wire eq, gt, lt;
    comp2 uut (.*);
    initial begin
        a = 0; b = 0; #10;
        a = 2; b = 1; #10;
        a = 1; b = 3; #10;
        a = 2; b = 2; #10;
        $finish;
    end
endmodule"""),
         
        ("4-bit Comparator", "4-bit comparative logic.",
         """module comp4(input [3:0] a, input [3:0] b, output eq, output gt, output lt);
    assign eq = (a == b);
    assign gt = (a > b);
    assign lt = (a < b);
endmodule""",
         """`timescale 1ns/1ps
module tb_comp4;
    reg [3:0] a, b;
    wire eq, gt, lt;
    comp4 uut (.*);
    initial begin
        a = 4'd5; b = 4'd5; #10;
        a = 4'd10; b = 4'd2; #10;
        a = 4'd3; b = 4'd12; #10;
        $finish;
    end
endmodule"""),
         
        ("8-bit Comparator", "8-bit comparative logic.",
         """module comp8(input [7:0] a, input [7:0] b, output eq);
    assign eq = (a == b);
endmodule""",
         """`timescale 1ns/1ps
module tb_comp8;
    reg [7:0] a, b;
    wire eq;
    comp8 uut (.*);
    initial begin
        a = 8'd42; b = 8'd42; #10;
        a = 8'd42; b = 8'd43; #10;
        $finish;
    end
endmodule"""),
         
        ("4-bit ALU", "4-bit basic ALU unit.",
         """module alu4(input [3:0] a, input [3:0] b, input [1:0] op, output reg [3:0] y);
    always @(*) begin
        case(op)
            2'b00: y = a + b;
            2'b01: y = a - b;
            2'b10: y = a & b;
            2'b11: y = a ^ b;
        endcase
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_alu4;
    reg [3:0] a, b;
    reg [1:0] op;
    wire [3:0] y;
    alu4 uut (.*);
    initial begin
        a = 4'd8; b = 4'd3; op = 2'b00; #10;
        op = 2'b01; #10;
        op = 2'b10; #10;
        op = 2'b11; #10;
        $finish;
    end
endmodule"""),
         
        ("8-bit ALU", "8-bit basic ALU unit.",
         """module alu8(input [7:0] a, input [7:0] b, input [2:0] op, output reg [7:0] y);
    always @(*) begin
        case(op)
            3'b000: y = a + b;
            3'b001: y = a - b;
            3'b010: y = a & b;
            3'b011: y = a | b;
            3'b100: y = a ^ b;
            3'b101: y = ~(a & b);
            3'b110: y = a << 1;
            3'b111: y = a >> 1;
        endcase
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_alu8;
    reg [7:0] a, b;
    reg [2:0] op;
    wire [7:0] y;
    alu8 uut (.*);
    initial begin
        a = 8'd10; b = 8'd5; op = 3'b000; #10;
        op = 3'b001; #10;
        op = 3'b010; #10;
        op = 3'b011; #10;
        op = 3'b100; #10;
        op = 3'b101; #10;
        op = 3'b110; #10;
        op = 3'b111; #10;
        $finish;
    end
endmodule"""),
         
        ("Binary to Gray 4-bit", "Translates binary to Gray code.",
         """module bin2gray4(input [3:0] bin, output [3:0] gray);
    assign gray = bin ^ (bin >> 1);
endmodule""",
         """`timescale 1ns/1ps
module tb_bin2gray4;
    reg [3:0] bin;
    wire [3:0] gray;
    bin2gray4 uut (.*);
    initial begin
        bin = 0;
        repeat (16) begin
            #10 bin = bin + 1;
        end
        $finish;
    end
endmodule"""),
         
        ("Gray to Binary 4-bit", "Translates Gray code back to binary.",
         """module gray2bin4(input [3:0] gray, output [3:0] bin);
    assign bin[3] = gray[3];
    assign bin[2] = gray[3] ^ gray[2];
    assign bin[1] = gray[3] ^ gray[2] ^ gray[1];
    assign bin[0] = gray[3] ^ gray[2] ^ gray[1] ^ gray[0];
endmodule""",
         """`timescale 1ns/1ps
module tb_gray2bin4;
    reg [3:0] gray;
    wire [3:0] bin;
    gray2bin4 uut (.*);
    initial begin
        gray = 0;
        repeat (16) begin
            #10 gray = gray + 1;
        end
        $finish;
    end
endmodule"""),
         
        ("BCD to Excess-3", "Adds 3 to BCD input.",
         """module bcd_exc3(input [3:0] bcd, output [3:0] exc3);
    assign exc3 = bcd + 4'd3;
endmodule""",
         """`timescale 1ns/1ps
module tb_bcd_exc3;
    reg [3:0] bcd;
    wire [3:0] exc3;
    bcd_exc3 uut (.*);
    initial begin
        bcd = 0;
        repeat (10) begin
            #10 bcd = bcd + 1;
        end
        $finish;
    end
endmodule"""),
         
        ("Excess-3 to BCD", "Subtracts 3 from Excess-3 input.",
         """module exc3_bcd(input [3:0] exc3, output [3:0] bcd);
    assign bcd = exc3 - 4'd3;
endmodule""",
         """`timescale 1ns/1ps
module tb_exc3_bcd;
    reg [3:0] exc3;
    wire [3:0] bcd;
    exc3_bcd uut (.*);
    initial begin
        exc3 = 3;
        repeat (10) begin
            #10 exc3 = exc3 + 1;
        end
        $finish;
    end
endmodule"""),
         
        ("Even Parity Generator", "Generates even parity bit.",
         """module parity_even(input [3:0] d, output p);
    assign p = ^d;
endmodule""",
         """`timescale 1ns/1ps
module tb_parity_even;
    reg [3:0] d;
    wire p;
    parity_even uut (.*);
    initial begin
        d = 0;
        repeat (16) begin
            #10 d = d + 1;
        end
        $finish;
    end
endmodule"""),
         
        ("Odd Parity Generator", "Generates odd parity bit.",
         """module parity_odd(input [3:0] d, output p);
    assign p = ~(^d);
endmodule""",
         """`timescale 1ns/1ps
module tb_parity_odd;
    reg [3:0] d;
    wire p;
    parity_odd uut (.*);
    initial begin
        d = 0;
        repeat (16) begin
            #10 d = d + 1;
        end
        $finish;
    end
endmodule""")
    ]

    for name, desc, rtl, tb in comb_others:
        traces = [
            {"name": "Input A (Dec)", "vals": [0,1,2,3,0,1,2,3,0,1], "color": "#3b82f6", "offset": 1.25},
            {"name": "Output Indicator", "vals": [0,0,1,0,0,0,1,0,0,0], "color": "#ef4444", "offset": 0.0, "is_output": True}
        ]
        add_item("2. Combinational Circuits (Data flow)", name, desc, rtl, tb, traces, allow_edit=False)


    # -------------------------------------------------------------
    # 3. Sequential Circuits (Behavioral) - 35 Examples
    # -------------------------------------------------------------
    seq_basics = [
        ("SR Latch", "Basic set-reset latch.",
         """module sr_latch(input s, input r, output q, output qb);
    assign q = ~(r | qb);
    assign qb = ~(s | q);
endmodule""",
         """`timescale 1ns/1ps
module tb_sr_latch;
    reg s, r;
    wire q, qb;
    sr_latch uut (.*);
    initial begin
        s = 0; r = 1; #10;
        s = 0; r = 0; #10;
        s = 1; r = 0; #10;
        s = 0; r = 0; #10;
        $finish;
    end
endmodule"""),
         
        ("D Latch", "Basic gated D Latch.",
         """module d_latch(input d, input en, output reg q);
    always @(*) begin
        if (en) q = d;
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_d_latch;
    reg d, en;
    wire q;
    d_latch uut (.*);
    initial begin
        en = 0; d = 0; #10;
        d = 1; #10;
        en = 1; #10;
        d = 0; #10;
        en = 0; d = 1; #10;
        $finish;
    end
endmodule"""),
         
        ("D Flip-Flop", "Positive edge DFF.",
         """module dff(input clk, input d, output reg q);
    always @(posedge clk) begin
        q <= d;
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_dff;
    reg clk, d;
    wire q;
    dff uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; d = 0; #12;
        d = 1; #10;
        d = 0; #10;
        $finish;
    end
endmodule"""),
         
        ("DFF with Active Low Reset", "Asynchronous active-low reset.",
         """module dff_rst_n(input clk, input rst_n, input d, output reg q);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) q <= 0;
        else q <= d;
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_dff_rst_n;
    reg clk, rst_n, d;
    wire q;
    dff_rst_n uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst_n = 0; d = 1; #12;
        rst_n = 1; #10;
        d = 0; #10;
        rst_n = 0; #10;
        $finish;
    end
endmodule"""),
         
        ("DFF with Synchronous Reset", "Synchronous reset.",
         """module dff_sync_rst(input clk, input rst, input d, output reg q);
    always @(posedge clk) begin
        if (rst) q <= 0;
        else q <= d;
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_dff_sync_rst;
    reg clk, rst, d;
    wire q;
    dff_sync_rst uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; d = 1; #12;
        rst = 0; #10;
        d = 0; #10;
        rst = 1; #10;
        $finish;
    end
endmodule"""),
         
        ("DFF with Clock Enable", "Loads data only when clock enable is High.",
         """module dff_en(input clk, input en, input d, output reg q);
    always @(posedge clk) begin
        if (en) q <= d;
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_dff_en;
    reg clk, en, d;
    wire q;
    dff_en uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; en = 0; d = 1; #12;
        en = 1; #10;
        en = 0; d = 0; #10;
        $finish;
    end
endmodule"""),
         
        ("JK Flip-Flop", "Edge triggered JK flip-flop.",
         """module jk_ff(input clk, input j, input k, output reg q);
    always @(posedge clk) begin
        q <= (j & ~q) | (~k & q);
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_jk_ff;
    reg clk, j, k;
    wire q;
    jk_ff uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; j = 0; k = 0; #12;
        j = 1; k = 0; #10;
        j = 0; k = 0; #10;
        j = 0; k = 1; #10;
        j = 1; k = 1; #20;
        $finish;
    end
endmodule"""),
         
        ("T Flip-Flop", "Toggle Flip-Flop.",
         """module t_ff(input clk, input rst, input t, output reg q);
    always @(posedge clk or posedge rst) begin
        if (rst) q <= 0;
        else if (t) q <= ~q;
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_t_ff;
    reg clk, rst, t;
    wire q;
    t_ff uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; t = 0; #12;
        rst = 0; t = 1; #30;
        t = 0; #10;
        $finish;
    end
endmodule"""),
         
        ("SR Flip-Flop", "Set Reset flip-flop.",
         """module sr_ff(input clk, input s, input r, output reg q);
    always @(posedge clk) begin
        if (s && !r) q <= 1;
        else if (!s && r) q <= 0;
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_sr_ff;
    reg clk, s, r;
    wire q;
    sr_ff uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; s = 0; r = 0; #12;
        s = 1; r = 0; #10;
        s = 0; r = 0; #10;
        s = 0; r = 1; #10;
        $finish;
    end
endmodule""")
    ]

    for name, desc, rtl, tb in seq_basics:
        traces = [
            {"name": "Clock (CLK)", "vals": [0,1,0,1,0,1,0,1,0,1], "color": "#94a3b8", "offset": 2.5},
            {"name": "Input / Control", "vals": [1,0,1,1,0,1,0,0,1,1], "color": "#3b82f6", "offset": 1.25},
            {"name": "State Output Q", "vals": [0,1,1,1,1,0,0,0,1,1], "color": "#ef4444", "offset": 0.0, "is_output": True}
        ]
        add_item("3. Sequential Circuits (Behavioral)", name, desc, rtl, tb, traces, is_comb=False)

    # Registers
    def add_register(bits):
        rtl = f"""module reg{bits}(
    input clk,
    input rst,
    input [{bits-1}:0] d,
    output reg [{bits-1}:0] q
);
    always @(posedge clk or posedge rst) begin
        if (rst) q <= 0;
        else     q <= d;
    end
endmodule"""
        tb = f"""`timescale 1ns/1ps
module tb_reg{bits};
    reg clk;
    reg rst;
    reg [{bits-1}:0] d;
    wire [{bits-1}:0] q;

    reg{bits} uut (
        .clk(clk),
        .rst(rst),
        .d(d),
        .q(q)
    );

    always #5 clk = ~clk;

    initial begin
        clk = 0;
        rst = 1;
        d = 0;
        #12;
        rst = 0;
        d = {bits}'d42;
        #10;
        d = {bits}'d17;
        #10;
        rst = 1;
        #10;
        $finish;
    end
endmodule"""
        traces = [
            {"name": "Clock (CLK)", "vals": [0,1,0,1,0,1,0,1,0,1], "color": "#94a3b8", "offset": 2.5},
            {"name": "Input D (Dec)", "vals": [1, 5, 5, 2, 8, 4, 3, 11, 0, 0], "color": "#3b82f6", "offset": 1.25},
            {"name": "Output Q (Dec)", "vals": [0, 0, 5, 5, 2, 2, 8, 8, 11, 0], "color": "#ef4444", "offset": 0.0, "is_output": True}
        ]
        add_item("3. Sequential Circuits (Behavioral)", f"{bits}-bit Register", f"Synchronous storage register of {bits} bits width.", rtl, tb, traces, is_comb=False)

    for b in [2, 4, 8, 16, 32, 64]:
        add_register(b)

    # Shift Registers & Counters
    seq_others = [
        ("4-bit SISO", "Serial-in Serial-out register.",
         """module siso4(input clk, input si, output so);
    reg [3:0] r;
    always @(posedge clk) r <= {r[2:0], si};
    assign so = r[3];
endmodule""",
         """`timescale 1ns/1ps
module tb_siso4;
    reg clk, si;
    wire so;
    siso4 uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; si = 1; #10;
        si = 0; #10;
        si = 1; #10;
        si = 1; #40;
        $finish;
    end
endmodule"""),
         
        ("4-bit SIPO", "Serial-in Parallel-out register.",
         """module sipo4(input clk, input si, output [3:0] q);
    reg [3:0] r;
    always @(posedge clk) r <= {r[2:0], si};
    assign q = r;
endmodule""",
         """`timescale 1ns/1ps
module tb_sipo4;
    reg clk, si;
    wire [3:0] q;
    sipo4 uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; si = 1; #10;
        si = 0; #10;
        si = 1; #10;
        si = 1; #40;
        $finish;
    end
endmodule"""),
         
        ("4-bit PISO", "Parallel-in Serial-out register.",
         """module piso4(input clk, input load, input [3:0] pin, output so);
    reg [3:0] r;
    always @(posedge clk) begin
        if (load) r <= pin;
        else r <= r << 1;
    end
    assign so = r[3];
endmodule""",
         """`timescale 1ns/1ps
module tb_piso4;
    reg clk, load;
    reg [3:0] pin;
    wire so;
    piso4 uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; load = 1; pin = 4'b1011; #10;
        load = 0; #50;
        $finish;
    end
endmodule"""),
         
        ("4-bit PIPO", "Parallel-in Parallel-out register.",
         """module pipo4(input clk, input [3:0] d, output reg [3:0] q);
    always @(posedge clk) q <= d;
endmodule""",
         """`timescale 1ns/1ps
module tb_pipo4;
    reg clk;
    reg [3:0] d;
    wire [3:0] q;
    pipo4 uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; d = 4'b1010; #12;
        d = 4'b0110; #10;
        d = 4'b1111; #10;
        $finish;
    end
endmodule"""),
         
        ("Universal Shift Register", "Supports shift operations and parallel load.",
         """module usr4(input clk, input [1:0] mode, input [3:0] d, output reg [3:0] q);
    always @(posedge clk) begin
        case(mode)
            2'b00: q <= q;
            2'b01: q <= {q[2:0], 1'b0};
            2'b10: q <= {1'b0, q[3:1]};
            2'b11: q <= d;
        endcase
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_usr4;
    reg clk;
    reg [1:0] mode;
    reg [3:0] d;
    wire [3:0] q;
    usr4 uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; mode = 2'b11; d = 4'b1011; #12;
        mode = 2'b01; #20;
        mode = 2'b10; #20;
        mode = 2'b00; #10;
        $finish;
    end
endmodule"""),
         
        ("4-bit Ring Counter", "Single bit circulation counter.",
         """module ring_count(input clk, input rst, output reg [3:0] q);
    always @(posedge clk or posedge rst) begin
        if (rst) q <= 4'b0001;
        else q <= {q[2:0], q[3]};
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_ring_count;
    reg clk, rst;
    wire [3:0] q;
    ring_count uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; #12;
        rst = 0; #60;
        $finish;
    end
endmodule"""),
         
        ("4-bit Johnson Counter", "Inverted feedback counter.",
         """module johnson_count(input clk, input rst, output reg [3:0] q);
    always @(posedge clk or posedge rst) begin
        if (rst) q <= 0;
        else q <= {q[2:0], ~q[3]};
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_johnson_count;
    reg clk, rst;
    wire [3:0] q;
    johnson_count uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; #12;
        rst = 0; #100;
        $finish;
    end
endmodule"""),
         
        ("4-bit Up Counter", "Synchronous binary up counter.",
         """module count_up(input clk, input rst, output reg [3:0] q);
    always @(posedge clk or posedge rst) begin
        if (rst) q <= 0;
        else q <= q + 1;
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_count_up;
    reg clk, rst;
    wire [3:0] q;
    count_up uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; #12;
        rst = 0; #180;
        $finish;
    end
endmodule"""),
         
        ("4-bit Down Counter", "Synchronous binary down counter.",
         """module count_dn(input clk, input rst, output reg [3:0] q);
    always @(posedge clk or posedge rst) begin
        if (rst) q <= 15;
        else q <= q - 1;
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_count_dn;
    reg clk, rst;
    wire [3:0] q;
    count_dn uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; #12;
        rst = 0; #180;
        $finish;
    end
endmodule"""),
         
        ("4-bit Up/Down Counter", "Up-Down direction select counter.",
         """module count_up_dn(input clk, input rst, input up_down, output reg [3:0] q);
    always @(posedge clk or posedge rst) begin
        if (rst) q <= 0;
        else q <= up_down ? q + 1 : q - 1;
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_count_up_dn;
    reg clk, rst, up_down;
    wire [3:0] q;
    count_up_dn uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; up_down = 1; #12;
        rst = 0; #100;
        up_down = 0; #100;
        $finish;
    end
endmodule"""),
         
        ("Mod-6 Counter", "Counts 0 to 5 for time minutes/seconds units.",
         """module count_mod6(input clk, input rst, output reg [2:0] q);
    always @(posedge clk or posedge rst) begin
        if (rst) q <= 0;
        else q <= (q == 5) ? 0 : q + 1;
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_count_mod6;
    reg clk, rst;
    wire [2:0] q;
    count_mod6 uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; #12;
        rst = 0; #80;
        $finish;
    end
endmodule"""),
         
        ("Mod-10 (BCD) Counter", "Decade counter resetting after 9.",
         """module count_mod10(input clk, input rst, output reg [3:0] q);
    always @(posedge clk or posedge rst) begin
        if (rst) q <= 0;
        else q <= (q == 9) ? 0 : q + 1;
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_count_mod10;
    reg clk, rst;
    wire [3:0] q;
    count_mod10 uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; #12;
        rst = 0; #120;
        $finish;
    end
endmodule"""),
         
        ("Mod-12 Counter", "Resets to 0 after count reaches 11.",
         """module count_mod12(input clk, input rst, output reg [3:0] q);
    always @(posedge clk or posedge rst) begin
        if (rst) q <= 0;
        else q <= (q == 11) ? 0 : q + 1;
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_count_mod12;
    reg clk, rst;
    wire [3:0] q;
    count_mod12 uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; #12;
        rst = 0; #140;
        $finish;
    end
endmodule"""),
         
        ("Frequency Divider (by 2)", "Halves the source clock frequency.",
         """module div2(input clk_in, output reg clk_out);
    initial clk_out = 0;
    always @(posedge clk_in) clk_out <= ~clk_out;
endmodule""",
         """`timescale 1ns/1ps
module tb_div2;
    reg clk_in;
    wire clk_out;
    div2 uut (.*);
    always #5 clk_in = ~clk_in;
    initial begin
        clk_in = 0; #100;
        $finish;
    end
endmodule"""),
         
        ("Frequency Divider (by 4)", "Divides the clock frequency by 4.",
         """module div4(input clk_in, output reg clk_out);
    reg r_div2 = 0;
    initial clk_out = 0;
    always @(posedge clk_in) r_div2 <= ~r_div2;
    always @(posedge r_div2) clk_out <= ~clk_out;
endmodule""",
         """`timescale 1ns/1ps
module tb_div4;
    reg clk_in;
    wire clk_out;
    div4 uut (.*);
    always #5 clk_in = ~clk_in;
    initial begin
        clk_in = 0; #200;
        $finish;
    end
endmodule"""),
         
        ("Frequency Divider (by 8)", "Divides by 8.",
         """module div8(input clk, output reg clk_out);
    reg [2:0] r = 0;
    initial clk_out = 0;
    always @(posedge clk) begin
        r <= r + 1;
        clk_out <= r[2];
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_div8;
    reg clk;
    wire clk_out;
    div8 uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; #400;
        $finish;
    end
endmodule"""),
         
        ("LFSR (PRBS Generator)", "Generates pseudorandom binary sequences.",
         """module lfsr(input clk, input rst, output reg [3:0] q);
    always @(posedge clk or posedge rst) begin
        if (rst) q <= 4'b0001;
        else q <= {q[2:0], q[3] ^ q[2]};
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_lfsr;
    reg clk, rst;
    wire [3:0] q;
    lfsr uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; #12;
        rst = 0; #200;
        $finish;
    end
endmodule"""),
         
        ("3-bit Ripple Counter", "Asynchronous ripple counter.",
         """module ripple_counter_3bit(input clk, input rst, output [2:0] q);
    reg q0 = 0, q1 = 0, q2 = 0;
    always @(posedge clk or posedge rst) begin
        if (rst) q0 <= 0;
        else q0 <= ~q0;
    end
    always @(negedge q0 or posedge rst) begin
        if (rst) q1 <= 0;
        else q1 <= ~q1;
    end
    always @(negedge q1 or posedge rst) begin
        if (rst) q2 <= 0;
        else q2 <= ~q2;
    end
    assign q = {q2, q1, q0};
endmodule""",
         """`timescale 1ns/1ps
module tb_ripple_counter_3bit;
    reg clk, rst;
    wire [2:0] q;
    ripple_counter_3bit uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; #12;
        rst = 0; #180;
        $finish;
    end
endmodule"""),
         
        ("4-bit Ripple Up Counter", "Counts 0-15 asynchronously.",
         """module ripple_up_4bit(input clk, input rst, output [3:0] q);
    reg [3:0] r = 0;
    always @(posedge clk or posedge rst) begin
        if (rst) r[0] <= 0;
        else r[0] <= ~r[0];
    end
    always @(negedge r[0] or posedge rst) begin
        if (rst) r[1] <= 0;
        else r[1] <= ~r[1];
    end
    always @(negedge r[1] or posedge rst) begin
        if (rst) r[2] <= 0;
        else r[2] <= ~r[2];
    end
    always @(negedge r[2] or posedge rst) begin
        if (rst) r[3] <= 0;
        else r[3] <= ~r[3];
    end
    assign q = r;
endmodule""",
         """`timescale 1ns/1ps
module tb_ripple_up_4bit;
    reg clk, rst;
    wire [3:0] q;
    ripple_up_4bit uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; #12;
        rst = 0; #320;
        $finish;
    end
endmodule"""),
         
        ("4-bit Ripple Down Counter", "Counts 15-0 asynchronously.",
         """module ripple_down_4bit(input clk, input rst, output [3:0] q);
    reg [3:0] r = 0;
    always @(posedge clk or posedge rst) begin
        if (rst) r[0] <= 0;
        else r[0] <= ~r[0];
    end
    always @(posedge r[0] or posedge rst) begin
        if (rst) r[1] <= 0;
        else r[1] <= ~r[1];
    end
    always @(posedge r[1] or posedge rst) begin
        if (rst) r[2] <= 0;
        else r[2] <= ~r[2];
    end
    always @(posedge r[2] or posedge rst) begin
        if (rst) r[3] <= 0;
        else r[3] <= ~r[3];
    end
    assign q = r;
endmodule""",
         """`timescale 1ns/1ps
module tb_ripple_down_4bit;
    reg clk, rst;
    wire [3:0] q;
    ripple_down_4bit uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; #12;
        rst = 0; #320;
        $finish;
    end
endmodule""")
    ]

    for name, desc, rtl, tb in seq_others:
        traces = [
            {"name": "Clock (CLK)", "vals": [0,1,0,1,0,1,0,1,0,1], "color": "#94a3b8", "offset": 2.5},
            {"name": "Input Control", "vals": [0,1,0,1,0,1,0,1,0,1], "color": "#3b82f6", "offset": 1.25},
            {"name": "Count / Status Output (Dec)", "vals": [0,1,2,3,4,5,6,7,0,1], "color": "#ef4444", "offset": 0.0, "is_output": True}
        ]
        add_item("3. Sequential Circuits (Behavioral)", name, desc, rtl, tb, traces, is_comb=False)


    # -------------------------------------------------------------
    # 4. Finite State Machines (FSM) - 25 Examples
    # -------------------------------------------------------------
    def get_fsm_transitions(seq, is_moore, overlap):
        L = len(seq)
        num_states = L + 1 if is_moore else L
        transitions = {}
        outputs = {}
        
        for state in range(num_states):
            prefix = seq[:state]
            for bit in (0, 1):
                next_str = prefix + str(bit)
                
                if is_moore:
                    if state == L:
                        if not overlap:
                            test_str = str(bit)
                        else:
                            test_str = seq + str(bit)
                    else:
                        test_str = next_str
                        
                    next_state = 0
                    for l in range(L, 0, -1):
                        if test_str.endswith(seq[:l]):
                            next_state = l
                            break
                    transitions[(state, bit)] = next_state
                else:
                    is_match = (state == L-1 and bit == int(seq[-1]))
                    if is_match and not overlap:
                        test_str = ""
                    else:
                        test_str = next_str
                    
                    next_state = 0
                    for l in range(L-1, 0, -1):
                        if test_str.endswith(seq[:l]):
                            next_state = l
                            break
                    transitions[(state, bit)] = next_state
                    outputs[(state, bit)] = 1 if is_match else 0
                    
            if is_moore:
                outputs[state] = 1 if state == L else 0
                
        return transitions, outputs

    def add_seq_detector(seq_name, overlap, is_moore):
        type_str = "Moore" if is_moore else "Mealy"
        overlap_str = "overlap" if overlap else "nonoverlap"
        display_overlap_str = "Overlapping" if overlap else "Non-overlapping"
        
        transitions, outputs = get_fsm_transitions(seq_name, is_moore, overlap)
        L = len(seq_name)
        num_states = L + 1 if is_moore else L
        state_names = [f"S{i}" for i in range(num_states)]
        
        # State Declarations
        width = (num_states - 1).bit_length()
        state_decls = []
        for i, s_name in enumerate(state_names):
            state_decls.append(f"    localparam {s_name} = {width}'d{i};")
        state_decl_str = "\n".join(state_decls)
        
        # Next State Cases
        next_state_cases = []
        for state in range(num_states):
            next_state_cases.append(f"            S{state}: begin")
            next_state_cases.append(f"                if (din) state_next = S{transitions[(state, 1)]};")
            next_state_cases.append(f"                else      state_next = S{transitions[(state, 0)]};")
            next_state_cases.append("            end")
        next_state_cases_str = "\n".join(next_state_cases)
        
        # Output Logic
        if is_moore:
            output_cases = []
            for state in range(num_states):
                output_cases.append(f"            S{state}: q_out = 1'b{outputs[state]};")
            output_logic = f"""    // Output Logic (Moore)
    always @(*) begin
        case (state_reg)
{'\n'.join('            ' + c for c in output_cases)}
            default: q_out = 1'b0;
        endcase
    end"""
        else:
            output_cases = []
            for state in range(num_states):
                output_cases.append(f"            S{state}: q_out = din ? 1'b{outputs[(state, 1)]} : 1'b{outputs[(state, 0)]};")
            output_logic = f"""    // Output Logic (Mealy)
    always @(*) begin
        case (state_reg)
{'\n'.join('            ' + c for c in output_cases)}
            default: q_out = 1'b0;
        endcase
    end"""

        module_name = f"detector_{seq_name}_{type_str.lower()}_{overlap_str}"
        
        rtl = f"""module {module_name}(
    input clk,
    input rst,
    input din,
    output reg q_out
);
{state_decl_str}

    reg [{width-1}:0] state_reg, state_next;

    // State Register
    always @(posedge clk or posedge rst) begin
        if (rst) state_reg <= S0;
        else     state_reg <= state_next;
    end

    // Next State Logic
    always @(*) begin
        state_next = state_reg;
        case (state_reg)
{next_state_cases_str}
            default: state_next = S0;
        endcase
    end

{output_logic}

endmodule"""

        # Build Testbench Stimulus sequence
        bits = [int(c) for c in seq_name]
        stim = [0, 1, 0] + bits + [1, 1] + bits + [0] + bits + [0]
        tb_stim_lines = []
        for b in stim:
            tb_stim_lines.append(f"        din = 1'b{b}; #10;")
            
        tb = f"""`timescale 1ns/1ps
module tb_{module_name};
    reg clk;
    reg rst;
    reg din;
    wire q_out;

    {module_name} uut (
        .clk(clk),
        .rst(rst),
        .din(din),
        .q_out(q_out)
    );

    always #5 clk = ~clk;

    initial begin
        clk = 0;
        rst = 1;
        din = 0;
        #12;
        rst = 0;
{'\n'.join(tb_stim_lines)}
        #20;
        $finish;
    end
endmodule"""

        traces = [
            {"name": "Clock CLK", "vals": [0,1,0,1,0,1,0,1,0,1], "color": "#94a3b8", "offset": 2.5},
            {"name": "Serial Input Din", "vals": [1, 0, 1, 1, 0, 1, 1, 0, 1, 1], "color": "#3b82f6", "offset": 1.25},
            {"name": f"{type_str} Detect Output", "vals": [0,0,0,1,0,0,1,0,0,1], "color": "#ef4444", "offset": 0.0, "is_output": True}
        ]
        add_item("4. Finite State Machines (FSM)", f"{type_str} {seq_name} Detector ({display_overlap_str})", f"FSM matching sequence pattern {seq_name} in serial inputs.", rtl, tb, traces, is_comb=False)

    sequences = ["101", "110", "1101", "1011", "0101"]
    for seq in sequences:
        for overlap in [True, False]:
            for is_moore in [True, False]:
                add_seq_detector(seq, overlap, is_moore)

    # FSM Controllers
    controllers = [
        ("Traffic Light Controller", "NS-EW state light phase changes.",
         """module traffic_fsm(
    input clk,
    input rst,
    output reg [2:0] ns,
    output reg [2:0] ew
);
    localparam S_NS_G_EW_R = 2'd0;
    localparam S_NS_Y_EW_R = 2'd1;
    localparam S_NS_R_EW_G = 2'd2;
    localparam S_NS_R_EW_Y = 2'd3;

    reg [1:0] state, next_state;
    reg [3:0] timer;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            state <= S_NS_G_EW_R;
            timer <= 0;
        end else begin
            if (timer == 4'd10) begin
                state <= next_state;
                timer <= 0;
            end else begin
                timer <= timer + 1;
            end
        end
    end

    always @(*) begin
        case (state)
            S_NS_G_EW_R: next_state = S_NS_Y_EW_R;
            S_NS_Y_EW_R: next_state = S_NS_R_EW_G;
            S_NS_R_EW_G: next_state = S_NS_R_EW_Y;
            S_NS_R_EW_Y: next_state = S_NS_G_EW_R;
            default:     next_state = S_NS_G_EW_R;
        endcase
    end

    always @(*) begin
        case (state)
            S_NS_G_EW_R: begin ns = 3'b001; ew = 3'b100; end
            S_NS_Y_EW_R: begin ns = 3'b010; ew = 3'b100; end
            S_NS_R_EW_G: begin ns = 3'b100; ew = 3'b001; end
            S_NS_R_EW_Y: begin ns = 3'b100; ew = 3'b010; end
            default:     begin ns = 3'b100; ew = 3'b100; end
        endcase
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_traffic_fsm;
    reg clk, rst;
    wire [2:0] ns, ew;
    traffic_fsm uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; #12;
        rst = 0; #500;
        $finish;
    end
endmodule"""),
         
        ("Elevator Controller", "Lift state floor routing transition FSM.",
         """module elevator_fsm(
    input clk,
    input rst,
    input [1:0] req_floor,
    output reg [1:0] current_floor,
    output reg [1:0] state
);
    localparam IDLE = 2'b00;
    localparam UP   = 2'b01;
    localparam DOWN = 2'b10;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            current_floor <= 2'b00;
            state <= IDLE;
        end else begin
            case (state)
                IDLE: begin
                    if (req_floor > current_floor) state <= UP;
                    else if (req_floor < current_floor) state <= DOWN;
                end
                UP: begin
                    current_floor <= current_floor + 1;
                    if (current_floor + 1 == req_floor) state <= IDLE;
                end
                DOWN: begin
                    current_floor <= current_floor - 1;
                    if (current_floor - 1 == req_floor) state <= IDLE;
                end
                default: state <= IDLE;
            endcase
        end
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_elevator_fsm;
    reg clk, rst;
    reg [1:0] req_floor;
    wire [1:0] current_floor, state;
    elevator_fsm uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; req_floor = 0; #12;
        rst = 0; #10;
        req_floor = 2; #80;
        req_floor = 0; #80;
        $finish;
    end
endmodule"""),
         
        ("Vending Machine FSM", "Dispenses item upon coin aggregation.",
         """module vending_fsm(
    input clk,
    input rst,
    input nickel,
    input dime,
    output reg dispense
);
    localparam S0  = 2'd0;
    localparam S5  = 2'd1;
    localparam S10 = 2'd2;
    localparam S15 = 2'd3;

    reg [1:0] state, next_state;

    always @(posedge clk or posedge rst) begin
        if (rst) state <= S0;
        else     state <= next_state;
    end

    always @(*) begin
        dispense = (state == S15);
        case (state)
            S0: begin
                if (dime)        next_state = S10;
                else if (nickel) next_state = S5;
                else             next_state = S0;
            end
            S5: begin
                if (dime)        next_state = S15;
                else if (nickel) next_state = S10;
                else             next_state = S5;
            end
            S10: begin
                if (dime || nickel) next_state = S15;
                else                next_state = S10;
            end
            S15: next_state = S0;
            default: next_state = S0;
        endcase
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_vending_fsm;
    reg clk, rst, nickel, dime;
    wire dispense;
    vending_fsm uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; nickel = 0; dime = 0; #12;
        rst = 0; #10;
        nickel = 1; #10; nickel = 0; #10;
        dime = 1; #10; dime = 0; #20;
        dime = 1; #10; dime = 0; #10;
        nickel = 1; #10; nickel = 0; #20;
        $finish;
    end
endmodule"""),
         
        ("FIFO Controller", "Handles FIFO full/empty pointers.",
         """module fifo_fsm(
    input clk,
    input rst,
    input wr,
    input rd,
    output reg full,
    output reg empty
);
    reg [2:0] count;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            count <= 0;
        end else begin
            case ({wr, rd})
                2'b10: if (count < 3'd4) count <= count + 1;
                2'b01: if (count > 0)    count <= count - 1;
                default: ;
            endcase
        end
    end

    always @(*) begin
        full = (count == 3'd4);
        empty = (count == 0);
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_fifo_fsm;
    reg clk, rst, wr, rd;
    wire full, empty;
    fifo_fsm uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; wr = 0; rd = 0; #12;
        rst = 0; #10;
        wr = 1; #40;
        wr = 0; rd = 1; #40;
        rd = 0; #20;
        $finish;
    end
endmodule"""),
         
        ("GCD Controller", "Euclidean GCD computation machine.",
         """module gcd_ctrl(
    input clk,
    input rst,
    input start,
    input [7:0] a_in,
    input [7:0] b_in,
    output reg [7:0] gcd_out,
    output reg done
);
    localparam IDLE = 2'd0;
    localparam COMPUTE = 2'd1;
    localparam DONE = 2'd2;

    reg [1:0] state;
    reg [7:0] a, b;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            state <= IDLE;
            gcd_out <= 0;
            done <= 0;
        end else begin
            case (state)
                IDLE: begin
                    done <= 0;
                    if (start) begin
                          a <= a_in;
                          b <= b_in;
                          state <= COMPUTE;
                    end
                end
                COMPUTE: begin
                    if (a == b) begin
                          gcd_out <= a;
                          done <= 1;
                          state <= DONE;
                    end else if (a > b) begin
                          a <= a - b;
                    end else begin
                          b <= b - a;
                    end
                end
                DONE: begin
                    done <= 0;
                    state <= IDLE;
                end
            endcase
        end
    end
endmodule""",
         """`timescale 1ns/1ps
module tb_gcd_ctrl;
    reg clk, rst, start;
    reg [7:0] a_in, b_in;
    wire [7:0] gcd_out;
    wire done;
    gcd_ctrl uut (.*);
    always #5 clk = ~clk;
    initial begin
        clk = 0; rst = 1; start = 0; a_in = 0; b_in = 0; #12;
        rst = 0; #10;
        a_in = 8'd24; b_in = 8'd18; start = 1; #10;
        start = 0; #150;
        a_in = 8'd35; b_in = 8'd14; start = 1; #10;
        start = 0; #150;
        $finish;
    end
endmodule""")
    ]

    for name, desc, rtl, tb in controllers:
        traces = [
            {"name": "Clock CLK", "vals": [0,1,0,1,0,1,0,1,0,1], "color": "#94a3b8", "offset": 2.5},
            {"name": "Status Input", "vals": [1,0,0,0,0,0,0,1,0,0], "color": "#3b82f6", "offset": 1.25},
            {"name": "Control Outputs", "vals": [0,1,2,3,4,4,3,2,1,0], "color": "#ef4444", "offset": 0.0, "is_output": True}
        ]
        add_item("4. Finite State Machines (FSM)", name, desc, rtl, tb, traces, is_comb=False)

    with open("verilog_db.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)
    print("Generated verilog_db.json with", len(db), "examples!")

if __name__ == "__main__":
    generate_examples()
