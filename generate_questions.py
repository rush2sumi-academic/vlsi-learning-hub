import json
import os

def generate_questions_db():
    # 1. Generate 130 unique flashcards
    flashcards = []
    
    unique_flashcards = [
        # Basic Level (1-45)
        ("Basic", "VLSI", "What is VLSI?", 
         "Very Large Scale Integration (VLSI) is the process of integrating millions or billions of metal-oxide-semiconductor transistors onto a single silicon integrated circuit chip."),
        ("Basic", "CMOS", "What is CMOS?", 
         "CMOS stands for Complementary Metal-Oxide-Semiconductor. It is a technology that uses complementary pairs of P-type and N-type MOSFETs to build low-power digital logic gates."),
        ("Basic", "CMOS", "What is the difference between NMOS and PMOS?", 
         "NMOS uses electrons as carriers (fast, pulls down to GND, turns ON with High gate voltage). PMOS uses holes as carriers (slower, pulls up to VDD, turns ON with Low gate voltage)."),
        ("Basic", "VLSI", "What is Moore's Law?", 
         "Moore's Law is an empirical observation that the number of transistors on a microchip doubles roughly every two years, while the cost is halved."),
        ("Basic", "VLSI", "What is an ASIC?", 
         "ASIC stands for Application-Specific Integrated Circuit. It is an integrated circuit customized for a particular use, rather than general-purpose processors."),
        ("Basic", "VLSI", "What is an FPGA?", 
         "FPGA stands for Field-Programmable Gate Array. It is a semiconductor device that can be configured by the customer or designer after manufacturing."),
        ("Basic", "CMOS", "What is the threshold voltage (Vth) of a MOSFET?", 
         "Vth is the minimum gate-to-source voltage (Vgs) required to create a conducting channel between the source and drain terminals."),
        ("Basic", "Verilog", "What is the difference between wire and reg in Verilog?", 
         "A wire represents a physical connection and does not store state; it must be continuously driven. A reg represents a variable that holds its value between procedural assignments."),
        ("Basic", "Verilog", "What is structural modeling in Verilog?", 
         "Structural modeling describes a circuit by instantiating lower-level modules and logic gates and connecting them using wires."),
        ("Basic", "Verilog", "What is dataflow modeling in Verilog?", 
         "Dataflow modeling describes logic using continuous assignments ('assign' statements) that define expressions on wires."),
        ("Basic", "Verilog", "What is behavioral modeling in Verilog?", 
         "Behavioral modeling describes the algorithmic behavior of a circuit inside procedural blocks like 'always' and 'initial'."),
        ("Basic", "Logic Gates", "What is a universal gate?", 
         "A universal gate is a logic gate that can implement any Boolean function without the need for other gates. NAND and NOR are universal gates."),
        ("Basic", "FSM", "What is a Moore FSM?", 
         "A finite state machine whose outputs depend only on the current state and are independent of current inputs."),
        ("Basic", "FSM", "What is a Mealy FSM?", 
         "A finite state machine whose outputs depend on both the current state and the current inputs."),
        ("Basic", "Combinational", "What is a multiplexer?", 
         "A combinational circuit that selects one of many inputs and routes it to a single output line based on selector lines."),
        ("Basic", "Sequential", "What is a latch?", 
         "A level-sensitive sequential circuit that stores state and is transparent (passes input to output) when enabled."),
        ("Basic", "Sequential", "What is a flip-flop?", 
         "An edge-triggered sequential circuit that stores state and updates its value on active transitions (rising or falling) of a clock."),
        ("Basic", "Digital", "What is the difference between synchronous and asynchronous circuits?", 
         "Synchronous circuits use a global clock to synchronize state changes, while asynchronous circuits use handshaking protocols or local signal changes."),
        ("Basic", "IC Classifications", "What is SSI, MSI, LSI, and VLSI?", 
         "Small, Medium, Large, and Very Large Scale Integration, classified by gate/transistor counts on a single silicon die."),
        ("Basic", "Logic Optimization", "What is a Karnaugh Map (K-Map)?", 
         "A graphical method to simplify Boolean algebra expressions without algebraic calculations, mapping combinations into adjacent squares."),
        ("Basic", "Number Systems", "What is 2's complement?", 
         "A mathematical operation used to represent signed binary numbers, where the MSB has a negative weight (e.g. -2^(N-1))."),
        ("Basic", "Setup/Hold", "What is propagation delay?", 
         "The time taken for an input signal transition to propagate and cause a stable logic transition at the output of a gate."),
        ("Basic", "Setup/Hold", "What is contamination delay?", 
         "The minimum delay from an input change to the first change on the output of a gate, also called min-delay."),
        ("Basic", "Verilog", "What is a module in Verilog?", 
         "The fundamental block of hierarchy in Verilog representing a logical circuit block with defined ports and internal logic."),
        ("Basic", "Verilog", "What does timescale 1ns/1ps mean?", 
         "Sets the reference time unit to 1ns (delays specified as #1 are 1ns) and time precision (rounding resolution) to 1ps."),
        ("Basic", "Verilog", "What is a blocking assignment?", 
         "An assignment using the '=' operator that executes sequentially, blocking subsequent assignments until completed."),
        ("Basic", "Verilog", "What is a non-blocking assignment?", 
         "An assignment using the '<=' operator that executes concurrently, scheduling updates for the end of the time step without blocking."),
        ("Basic", "Verilog", "What is a localparam?", 
         "A constant parameter whose scope is restricted to the local module and cannot be overridden by parent modules during instantiation."),
        ("Basic", "CMOS", "What is the body effect?", 
         "A short-channel effect where the threshold voltage changes due to a source-to-substrate (bulk) bias potential."),
        ("Basic", "CMOS", "Why does PMOS conduct poorly compared to NMOS?", 
         "Because hole mobility in silicon is 2-3 times lower than electron mobility, resulting in less current drive for equal channel dimensions."),
        ("Basic", "Digital", "What is a Gray Code?", 
         "An unweighted binary code where only one bit transitions at a time between successive numeric values, preventing hazards."),
        ("Basic", "Verilog", "What is a testbench?", 
         "A non-synthesizable block used to apply control stimuli and verify Device Under Test (DUT) outputs in simulation."),
        ("Basic", "Verification", "What is verification?", 
         "The process of checking that a design matches its functional specification through simulation, emulation, or formal methods."),
        ("Basic", "Design", "What is synthesis?", 
         "The process of translating high-level RTL code into a gate-level netlist of library standard cells under timing constraints."),
        ("Basic", "Verification", "What is code coverage?", 
         "A verification metric indicating how much of the RTL code structure (lines, branches, expressions) has been executed during simulation."),
        ("Basic", "STA", "What is static timing analysis?", 
         "A method of computing timing delays along paths in a digital circuit without running functional simulations."),
        ("Basic", "Physical Design", "What is floorplanning?", 
         "Determining chip size, core boundary, power routing, and macro/I/O placement to optimize design constraints."),
        ("Basic", "Physical Design", "What is routing?", 
         "Laying out physical metal wires to connect standard cells together per the netlist while satisfying design rules."),
        ("Basic", "DFT", "What is a scan chain?", 
         "A shift register path formed by chaining flip-flops together to improve test observability and controllability after fabrication."),
        ("Basic", "CMOS", "What is dynamic power?", 
         "Power consumed during signal transitions, primarily charging/discharging capacitances and short-circuit currents."),
        ("Basic", "CMOS", "What is static power?", 
         "Leakage power consumed when gates are idle, caused by subthreshold, gate tunneling, and reverse-bias leakage currents."),
        ("Basic", "Logic Design", "What is active-low logic?", 
         "A logic scheme where a logic 0 indicates the active or asserted state, commonly used for resets and select signals."),
        ("Basic", "Logic Design", "What is a tri-state buffer?", 
         "A buffer with three output states: High (1), Low (0), and High-Impedance (Z) where the output is electrically disconnected."),
        ("Basic", "STA", "What is a clock period?", 
         "The time elapsed between two consecutive identical edges of the clock signal, representing clock cycle time."),
        ("Basic", "Logic Design", "What is even parity?", 
         "A check bit added to a binary code to ensure the total count of 1-bits is even, facilitating simple error detection."),

        # Intermediate Level (46-90)
        ("Intermediate", "FinFET", "What is a FinFET?", 
         "A 3D transistor where the channel is a thin vertical fin wrapped by the gate on three sides, reducing leakage."),
        ("Intermediate", "FinFET", "Why is FinFET better than planar MOSFET?", 
         "Better gate control over the channel, lower subthreshold leakage, and higher drive currents at lower operating voltages."),
        ("Intermediate", "DIBL", "What is Drain-Induced Barrier Lowering (DIBL)?", 
         "A short-channel effect where high drain voltage lowers the source-channel potential barrier, reducing threshold voltage."),
        ("Intermediate", "CMOS", "What is channel length modulation?", 
         "The saturation-region shortening of the channel length as Vds increases, which slightly increases drain current."),
        ("Intermediate", "Latch-up", "What is latch-up?", 
         "An accidental low-impedance path between VDD and GND caused by parasitic SCR structures in CMOS, causing short circuits."),
        ("Intermediate", "Latch-up", "How do you prevent latch-up?", 
         "Placing substrate/well guard rings, using well taps, and increasing spacing between N-well and P-substrate regions."),
        ("Intermediate", "Metastability", "What is metastability?", 
         "An unstable state where a flip-flop output fails to settle to a stable 0 or 1 within the required time due to setup/hold violations."),
        ("Intermediate", "CDC", "What is Clock Domain Crossing?", 
         "A signal transition from one clock domain to another asynchronous clock domain, requiring synchronization."),
        ("Intermediate", "Synchronizer", "What is a 2-FF synchronizer?", 
         "Two cascading flip-flops used to resolve metastability before passing asynchronous data into a new clock domain."),
        ("Intermediate", "Synchronizer", "What is a FIFO synchronizer?", 
         "A queue using gray-coded read/write pointers to safely cross multi-bit data between asynchronous clock domains."),
        ("Intermediate", "Handshaking", "What is handshaking CDC?", 
         "A CDC method where control signals (request/acknowledge) are passed back and forth to guarantee data transfer."),
        ("Intermediate", "FSM", "What is one-hot encoding?", 
         "A state representation where only one flip-flop is active (logic 1) at a time, simplifying next-state logic."),
        ("Intermediate", "FSM", "What is binary encoding?", 
         "A state representation using standard binary counting, minimizing the number of state flip-flops."),
        ("Intermediate", "FSM", "What is gray state encoding?", 
         "State encoding where successive states differ by only 1 bit, preventing hazard glitches during transitions."),
        ("Intermediate", "Verilog", "What is a generate block?", 
         "A construct used to instantiate modules or generate code structures conditionally or in a loop based on parameters."),
        ("Intermediate", "Verilog", "What is a task in Verilog?", 
         "A procedural block that can consume simulation time (delays) and have multiple outputs, but does not return a direct value."),
        ("Intermediate", "Verilog", "What is a function in Verilog?", 
         "A zero-delay procedural block that must return exactly one value and cannot contain time-consuming statements."),
        ("Intermediate", "Verilog", "What is the difference between logic and reg in SystemVerilog?", 
         "logic is a single-drive variable that can replace both reg and wire, eliminating declaration confusion."),
        ("Intermediate", "Verilog", "What is procedural assignment?", 
         "Assignment inside always or initial blocks (using '=' or '<='), storing values in variables."),
        ("Intermediate", "Verilog", "What is continuous assignment?", 
         "Assignment on wires using the assign keyword, executing continuously in parallel."),
        ("Intermediate", "STA", "What is setup time?", 
         "The minimum time before the clock edge during which the data input to a flip-flop must remain stable."),
        ("Intermediate", "STA", "What is hold time?", 
         "The minimum time after the clock edge during which the data input to a flip-flop must remain stable."),
        ("Intermediate", "STA", "What is clock skew?", 
         "The spatial difference in the arrival time of a clock signal edge at two different registers."),
        ("Intermediate", "STA", "What is clock jitter?", 
         "The temporal variation of clock edges from their ideal periodic positions over time."),
        ("Intermediate", "STA", "What is setup slack?", 
         "The timing margin for setup: Required Arrival Time minus Actual Arrival Time. Positive is good; negative is a violation."),
        ("Intermediate", "STA", "What is hold slack?", 
         "The timing margin for hold: Actual Arrival Time minus Required Arrival Time."),
        ("Intermediate", "STA", "What is a false path?", 
         "A path that physically exists but is electrically impossible to traverse, or is intentionally ignored for timing."),
        ("Intermediate", "STA", "What is a multi-cycle path?", 
         "A path designed to take more than one clock cycle to propagate data from source to destination."),
        ("Intermediate", "Physical Design", "What is Floorplanning?", 
         "The step of placing macros, pad pins, and partitioning the core layout."),
        ("Intermediate", "Physical Design", "What is Placement?", 
         "Placing standard cell instances on rows within the core area, optimizing wire length and timing."),
        ("Intermediate", "Physical Design", "What is Clock Tree Synthesis (CTS)?", 
         "Constructing a clock buffer network to distribute the clock to all registers with minimal skew."),
        ("Intermediate", "Physical Design", "What is RC extraction?", 
         "Computing parasitic resistances and capacitances of layout metal lines to perform accurate delay calculation."),
        ("Intermediate", "DFT", "What is ATPG?", 
         "Automatic Test Pattern Generation: using software to generate vectors to test manufactured chips for structural defects."),
        ("Intermediate", "DFT", "What is BIST?", 
         "Built-In Self-Test: adding internal test circuits (like LFSR and MISR) to test memory or logic blocks autonomously."),
        ("Intermediate", "DFT", "What is JTAG?", 
         "Joint Test Action Group: a standard interface (IEEE 1149.1) used for boundary scans to test PCB interconnections."),
        ("Intermediate", "Fault Models", "What is a stuck-at fault?", 
         "A defect model where a wire signal is permanently tied to VDD (stuck-at-1) or GND (stuck-at-0)."),
        ("Intermediate", "Fault Models", "What is a transition fault?", 
         "A defect model representing slow-to-rise or slow-to-fall signal propagation."),
        ("Intermediate", "Fault Models", "What is a path delay fault?", 
         "A defect model testing whether the cumulative delay of a path exceeds the clock cycle."),
        ("Intermediate", "Power", "What is leakage power?", 
         "Power consumed by subthreshold conduction, gate tunneling, and reverse bias leakage when transistors are inactive."),
        ("Intermediate", "Power", "What is short-circuit power?", 
         "Direct current flow from VDD to GND during switching when both pull-up and pull-down networks are transiently ON."),
        ("Intermediate", "Power", "What is clock gating?", 
         "Disabling the clock signal to idle registers to save dynamic switching power."),
        ("Intermediate", "Power", "What is power gating?", 
         "Shutting off the power supply (VDD) to inactive blocks to eliminate static leakage power."),
        ("Intermediate", "Physical Design", "What is Antenna Effect?", 
         "Charge accumulation on long metal wires during fabrication, which can rupture thin gate oxides."),
        ("Intermediate", "Physical Design", "How is the Antenna Effect solved?", 
         "Inserting antenna diodes or routing wires to higher metal layers (layer hopping)."),
        ("Intermediate", "STA", "Define Setup Constraint Equation.",
         "T_cq + T_comb + T_setup <= T_clk + T_skew. Slack is the difference."),

        # Advanced Level (91-130)
        ("Advanced", "STA", "What is setup time borrowing in latches?", 
         "Transparent latches allow data to arrive late, 'borrowing' time from the subsequent clock phase."),
        ("Advanced", "STA", "What is recovery time?", 
         "The minimum setup time for an asynchronous control signal (like reset) to go inactive before the active clock edge."),
        ("Advanced", "STA", "What is removal time?", 
         "The minimum hold time for an asynchronous control signal to remain active after the active clock edge."),
        ("Advanced", "STA", "What is On-Chip Variation (OCV)?", 
         "Variations in process, voltage, and temperature across different locations on the same die."),
        ("Advanced", "STA", "What is the difference between AOCV and POCV?", 
         "AOCV applies location-distance variation derates; POCV models variation statistically per cell (using standard deviations)."),
        ("Advanced", "Physical Design", "What is Layout vs Schematic (LVS)?", 
         "A physical verification step checking that layout netlist connectivity matches the schematic netlist."),
        ("Advanced", "Physical Design", "What is Design Rule Checking (DRC)?", 
         "Verification that layout patterns obey geometric spacing and width rules set by the foundry."),
        ("Advanced", "Physical Design", "What is Electromigration?", 
         "Gradual displacement of metal atoms in conductors due to high current density, causing opens or shorts."),
        ("Advanced", "Physical Design", "How is Electromigration solved?", 
         "Widening metal tracks or using electromigration-resistant metals like copper or ruthenium."),
        ("Advanced", "Physical Design", "What is IR Drop?", 
         "Voltage drops across power distribution networks due to wire resistances, slowing cell speeds."),
        ("Advanced", "Physical Design", "What is dynamic IR drop?", 
         "High voltage drops occurring during active clock edges when many cells switch simultaneously."),
        ("Advanced", "Physical Design", "What is Crosstalk?", 
         "Unwanted signal coupling between adjacent routing wires due to mutual capacitance and inductance."),
        ("Advanced", "Physical Design", "What is Crosstalk delay?", 
         "Crosstalk slowing down or speeding up transition times due to opposite or same-direction switching on neighboring lines."),
        ("Advanced", "Physical Design", "What is Crosstalk noise (glitch)?", 
         "A voltage spike induced on an idle victim line by a transition on an adjacent aggressor line."),
        ("Advanced", "STA", "How do you fix setup violations?", 
         "Gate sizing (increase driver strength), logic restructuring, lowering threshold voltage (LVT), or lowering clock frequency."),
        ("Advanced", "STA", "How do you fix hold violations?", 
         "Inserting delay buffers on the data path to slow it down (cannot be fixed by changing clock frequency)."),
        ("Advanced", "Verification", "What is functional coverage?", 
         "A verification metric defining user-specified logic scenarios to track which features have been verified."),
        ("Advanced", "Verification", "What is assertion-based verification (ABV)?", 
         "Using assertions (SystemVerilog Assertions - SVA) to monitor and verify design properties in real-time."),
        ("Advanced", "Verification", "What is constrained-random stimulus?", 
         "Generating random test vectors restricted by constraints to hit corner cases automatically."),
        ("Advanced", "Metastability", "What is Mean Time Between Failures (MTBF) for synchronizers?", 
         "A metric estimating the average time between system failures due to metastability."),
        ("Advanced", "GAAFET", "What is GAAFET (Gate-All-Around)?", 
         "A transistor architecture where the gate material wraps around the nanosheet channel completely on all sides."),
        ("Advanced", "FinFET", "What is FinFET self-heating?", 
         "Heat confinement in FinFET fins due to poor thermal conductivity of surrounding oxide layers, increasing local temperature."),
        ("Advanced", "CMOS", "What is Fowler-Nordheim tunneling?", 
         "Quantum mechanical tunneling of electrons through thin barrier oxides under high electric fields (used in EEPROMs/Flash)."),
        ("Advanced", "CMOS", "What is gate-induced drain leakage (GIDL)?", 
         "Substrate leakage current under the gate-drain overlap region caused by high electric fields in sub-micron devices."),
        ("Advanced", "Clock Tree", "What is clock latency (insertion delay)?", 
         "The time delay required for a clock signal to propagate from the clock source pin to register clock pins."),
        ("Advanced", "Power", "What is a Level Shifter?", 
         "A cell used to interface signals traveling between two different voltage domains in multi-VDD designs."),
        ("Advanced", "Power", "What is an Isolation Cell?", 
         "A cell used to clamp signals to a safe constant value when crossing from a powered-down domain to an active domain."),
        ("Advanced", "Power", "What is a Retention Flop?", 
         "A special flip-flop that preserves its state using an auxiliary low-leakage supply when the primary block is power-gated."),
        ("Advanced", "DFT", "What is a fault coverage metric?", 
         "The ratio of faults detected by ATPG patterns to the total testable faults in the design."),
        ("Advanced", "DFT", "What is IDDQ testing?", 
         "Testing method detecting defects by measuring supply leakage current in the quiescent (idle) state."),
        ("Advanced", "Verification", "What is UVM?", 
         "Universal Verification Methodology: a standardized SystemVerilog library to build modular, coverage-driven verification testbenches."),
        ("Advanced", "DFT", "What is boundary scan?", 
         "Test methodology inserting scan cells on chip pads to verify pin connections on a PCB (JTAG)."),
        ("Advanced", "STA", "What is dynamic timing analysis?", 
         "Functional gate-level simulation verifying timing paths by applying input waveforms over time."),
        ("Advanced", "CMOS", "What is velocity saturation?", 
         "Saturation of carrier velocity in short-channel devices due to high lateral electric fields, limiting drain current."),
        ("Advanced", "FSM", "What is a glitch-free clock multiplexer?", 
         "A circuit using synchronized enables to switch clock sources safely without introducing transient clock spikes."),
        ("Advanced", "STA", "What is clock latency uncertainty?", 
         "A margin added during timing analysis to model jitter and tree variations."),
        ("Advanced", "Clock Tree", "What is clock gating setup/hold time?", 
         "The setup and hold requirements for the gating control signal relative to the clock."),
        ("Advanced", "SOI", "What is Silicon-on-Insulator (SOI) technology?", 
         "Fabricating transistors on a thin silicon layer isolated from the bulk substrate by a buried oxide (BOX) layer."),
        ("Advanced", "STA", "What is a multi-cycle path constraint?", 
         "An instruction tells the STA tool to allow N clock cycles (e.g. set_multicycle_path 2) for a path."),
        ("Advanced", "DFT", "What is a transitional fault check?", 
         "Testing a gate's ability to switch from 0 to 1 and 1 to 0 within a clock cycle.")
    ]

    for idx, item in enumerate(unique_flashcards):
        flashcards.append({
            "id": f"card_{idx+1}",
            "category": item[0],
            "topic": item[1],
            "question": item[2],
            "answer": item[3]
        })

    # 2. Generate 92 unique multiple choice questions (23 per domain)
    quiz = {}
    
    # -------------------------------------------------------------
    # Topic 1: VLSI Fundamentals (23 Unique Questions)
    # -------------------------------------------------------------
    quiz["VLSI Fundamentals"] = [
        {
            "q": "What is the typical active transistor count range for a Very Large Scale Integration (VLSI) chip?",
            "opts": ["1 to 10", "100 to 10,000", "10,000 to 1,000,000", "Over 1,000,000"],
            "ans": "10,000 to 1,000,000",
            "exp": "VLSI classification covers circuits with 10k to 1 million active devices."
        },
        {
            "q": "Moore's Law predicts that the transistor density on an IC doubles approximately every:",
            "opts": ["6 months", "1 year", "2 years", "5 years"],
            "ans": "2 years",
            "exp": "Gordon Moore observed that transistor counts double roughly every 24 months."
        },
        {
            "q": "Which of the following is a primary physical bottleneck of scaling down below 2nm?",
            "opts": ["Lack of designers", "Quantum tunneling and static leakage", "Low silicon abundance", "Incorrect Boolean math"],
            "ans": "Quantum tunneling and static leakage",
            "exp": "As gate oxide layers approach atomic thickness, electrons tunnel through the barrier, causing high static leakage."
        },
        {
            "q": "SSI (Small Scale Integration) was primarily used to build:",
            "opts": ["Basic single logic gates and flip-flops", "8-bit microprocessors", "Modern smart device SoCs", "16-core GPU modules"],
            "ans": "Basic single logic gates and flip-flops",
            "exp": "SSI chips contained very few transistors (usually 1 to 10), covering basic logic gates."
        },
        {
            "q": "What does ULSI stand for in microelectronics classification?",
            "opts": ["Ultra Large Scale Integration", "Universal Logic Silicon Interface", "Unified Layout Simulation Instrument", "Unipolar Latch Static Impedance"],
            "ans": "Ultra Large Scale Integration",
            "exp": "ULSI stands for Ultra Large Scale Integration, representing chips with over 1,000,000 transistors."
        },
        {
            "q": "Who co-founded Intel and formulated the empirical scaling law for microchips in 1965?",
            "opts": ["Gordon Moore", "Robert Noyce", "Jack Kilby", "Dennis Ritchie"],
            "ans": "Gordon Moore",
            "exp": "Gordon Moore co-founded Intel and described the doubling of components on a chip."
        },
        {
            "q": "What is the main characteristic of a System-on-Chip (SoC)?",
            "opts": ["Integration of processor, memory, and peripherals on a single die", "Placing separate packages on a board", "Using vacuum tubes for processing", "Restricting the clock frequency to 1 MHz"],
            "ans": "Integration of processor, memory, and peripherals on a single die",
            "exp": "An SoC integrates all components of a computer or other electronic system into a single integrated circuit."
        },
        {
            "q": "What type of material is primarily used as the substrate in semiconductor manufacturing?",
            "opts": ["Copper", "Silicon", "Germanium", "Gallium Arsenide"],
            "ans": "Silicon",
            "exp": "Silicon is the most widely used semiconductor substrate due to its abundance and stable oxide."
        },
        {
            "q": "Which scale of integration contains 100 to 10,000 transistors?",
            "opts": ["SSI", "MSI", "LSI", "VLSI"],
            "ans": "MSI",
            "exp": "MSI (Medium Scale Integration) contains 100 to 10,000 transistors."
        },
        {
            "q": "In digital logic, what is the 'fan-out' of a gate?",
            "opts": ["The number of gate inputs the output can reliably drive", "The size of the output pin", "The current drawn from power grid", "The temperature of the silicon die"],
            "ans": "The number of gate inputs the output can reliably drive",
            "exp": "Fan-out specifies the maximum number of logical inputs that the output of a single gate can feed."
        },
        {
            "q": "Which rule/law describes the relationship between logic gate count and pin count of an IC?",
            "opts": ["Rent's Rule", "Moore's Law", "Ohm's Law", "Dennard Scaling"],
            "ans": "Rent's Rule",
            "exp": "Rent's Rule is an empirical relationship between the number of external pins and the number of logic blocks."
        },
        {
            "q": "What does 'foundry' refer to in the semiconductor industry?",
            "opts": ["A design center", "A fabrication plant that manufactures silicon wafers", "A software testing company", "A packaging facility"],
            "ans": "A fabrication plant that manufactures silicon wafers",
            "exp": "A semiconductor fabrication plant (foundry or fab) manufactures the physical integrated circuits."
        },
        {
            "q": "Which technology node type represents a 3D channel wrap gate design?",
            "opts": ["Planar MOSFET", "BJT", "FinFET", "JFET"],
            "ans": "FinFET",
            "exp": "FinFET wraps the gate around a thin vertical fin, forming a 3D channel structure."
        },
        {
            "q": "What is a 'wafer' in silicon processing?",
            "opts": ["A thin slice of semiconductor material used to fabricate ICs", "A type of logic analyzer", "A packaging layer", "A testing signal pin"],
            "ans": "A thin slice of semiconductor material used to fabricate ICs",
            "exp": "Wafers are round, thin slices of crystalline silicon used as substrates for microchips."
        },
        {
            "q": "Which scale of integration corresponds to early 8-bit microprocessors like the Intel 8080?",
            "opts": ["MSI", "LSI", "VLSI", "ULSI"],
            "ans": "LSI",
            "exp": "LSI (Large Scale Integration) covers 10,000 to 100,000 transistors, suitable for early CPUs."
        },
        {
            "q": "What is the primary purpose of packaging an IC?",
            "opts": ["To protect the silicon die and provide electrical connection pins", "To reduce the gate count", "To increase clock speed", "To eliminate parasitics completely"],
            "ans": "To protect the silicon die and provide electrical connection pins",
            "exp": "Packaging protects the fragile silicon die and provides contact leads to mount on PCBs."
        },
        {
            "q": "What does 'yield' represent in semiconductor manufacturing?",
            "opts": ["The speed of the chip", "The percentage of functional dies on a fabricated wafer", "The voltage limit of the substrate", "The width of the channel"],
            "ans": "The percentage of functional dies on a fabricated wafer",
            "exp": "Yield is the ratio of working chips to the total number of chips fabricated on a wafer."
        },
        {
            "q": "Which metric measures the processing performance per unit of silicon area?",
            "opts": ["Computational Density", "Dynamic Power", "Static Current", "Transistor Count"],
            "ans": "Computational Density",
            "exp": "Computational Density measures performance throughput relative to silicon area."
        },
        {
            "q": "What does a 'fabless' semiconductor company mean?",
            "opts": ["Designs chips but outsources physical fabrication", "Fabricates chips but does not design them", "Has no design team", "Sells raw silicon wafers"],
            "ans": "Designs chips but outsources physical fabrication",
            "exp": "Fabless companies focus on design and sales, outsourcing wafer fabrication to foundries."
        },
        {
            "q": "What is the typical thickness of a silicon wafer?",
            "opts": ["1 to 2 meters", "0.5 to 1.0 millimeters", "1 to 2 nanometers", "10 to 20 micrometers"],
            "ans": "0.5 to 1.0 millimeters",
            "exp": "Wafers are thin discs, typically between 500 to 1000 micrometers thick."
        },
        {
            "q": "Which company developed the first commercial microprocessor (the 4004)?",
            "opts": ["AMD", "IBM", "Intel", "TSMC"],
            "ans": "Intel",
            "exp": "Intel introduced the 4-bit 4004 microprocessor in 1971."
        },
        {
            "q": "Which term describes the degradation of IC performance due to continuous temperature and voltage stress over time?",
            "opts": ["Silicon Aging", "Electromigration", "Body effect", "Channel modulation"],
            "ans": "Silicon Aging",
            "exp": "Silicon aging refers to degradation mechanisms (like NBTI and HCI) that shift parameters over time."
        },
        {
            "q": "What does GDSII stand for in the IC design flow?",
            "opts": ["Graphic Database System II", "General Design Standard II", "Gate Delay Simulator II", "Global Die Structure II"],
            "ans": "Graphic Database System II",
            "exp": "GDSII is the standard database format for exchange of integrated circuit physical layout data."
        }
    ]

    # -------------------------------------------------------------
    # Topic 2: CMOS Technology (23 Unique Questions)
    # -------------------------------------------------------------
    quiz["CMOS Technology"] = [
        {
            "q": "Why is the PMOS transistor made wider than the NMOS in a symmetric CMOS inverter layout?",
            "opts": ["PMOS handles higher voltages", "Hole mobility is 2-3x lower than electron mobility", "PMOS needs to be closer to VDD", "It reduces fabrication costs"],
            "ans": "Hole mobility is 2-3x lower than electron mobility",
            "exp": "Because holes have lower mobility than electrons, PMOS must be wider to match the current-drive capacity and ensure symmetric rise/fall times."
        },
        {
            "q": "When the input voltage to a CMOS inverter is Vin = VDD (Logic H), what are the states of the NMOS and PMOS?",
            "opts": ["NMOS is ON, PMOS is OFF", "NMOS is OFF, PMOS is ON", "Both are ON", "Both are OFF"],
            "ans": "NMOS is ON, PMOS is OFF",
            "exp": "High input gate voltage attracts electrons in NMOS (ON) and shuts down PMOS channel (OFF), pulling output to Ground."
        },
        {
            "q": "In which region does a MOSFET operate if Vgs > Vth and Vds >= Vgs - Vth?",
            "opts": ["Cut-off", "Linear", "Saturation", "Breakdown"],
            "ans": "Saturation",
            "exp": "When drain-to-source voltage Vds exceeds the gate overdrive (Vgs - Vth), the channel pinch-off occurs near the drain, putting the device in Saturation."
        },
        {
            "q": "What is the formula for dynamic capacitive switching power in CMOS circuits?",
            "opts": ["P = V * I", "P = C * V_DD^2 * f", "P = I_leak * V_DD", "P = V^2 / R"],
            "ans": "P = C * V_DD^2 * f",
            "exp": "Dynamic capacitive power is directly proportional to load capacitance, frequency, and the square of supply voltage."
        },
        {
            "q": "How is threshold voltage (Vth) of a MOSFET defined?",
            "opts": ["Vgs at which strong inversion occurs in the channel", "Vds at which current saturates", "Minimum supply voltage", "Leakage voltage limit"],
            "ans": "Vgs at which strong inversion occurs in the channel",
            "exp": "Vth is the minimum gate-to-source voltage required to create an inversion layer for conduction."
        },
        {
            "q": "How does the body effect influence the threshold voltage (Vth) of a MOSFET?",
            "opts": ["Decreases Vth", "Increases Vth", "Has no effect", "Reverses polarity"],
            "ans": "Increases Vth",
            "exp": "A reverse bias between the source and substrate (bulk) increases Vth due to depletion layer expansion."
        },
        {
            "q": "In which region of operation does 'channel length modulation' occur?",
            "opts": ["Linear", "Cut-off", "Saturation", "Subthreshold"],
            "ans": "Saturation",
            "exp": "Increasing Vds beyond pinch-off shifts the channel termination point away from the drain, decreasing effective length."
        },
        {
            "q": "Which mechanism dominates leakage power in deep sub-micron (sub-10nm) planar transistors?",
            "opts": ["Subthreshold leakage and gate oxide tunneling", "Short-circuit dissipation", "Dynamic charging", "Junction heating"],
            "ans": "Subthreshold leakage and gate oxide tunneling",
            "exp": "As gate oxide and channel dimensions shrink, static leakage currents dominate due to tunneling and poor gate control."
        },
        {
            "q": "What prevents latch-up in CMOS layout implementations?",
            "opts": ["Using guard rings and well taps", "Adding serial resistors", "Increasing clock skew", "Reducing channel width"],
            "ans": "Using guard rings and well taps",
            "exp": "Guard rings collect stray carriers, and well taps clamp well potentials, preventing parasitic SCR triggering."
        },
        {
            "q": "What is the 'noise margin' of a CMOS logic gate?",
            "opts": ["The input voltage range a gate can tolerate without changing output logic", "The noise generated by standard cells", "The thermal limit of substrate", "The dynamic current drawn from grid"],
            "ans": "The input voltage range a gate can tolerate without changing output logic",
            "exp": "Noise margin is the measure of noise immunity of a gate, defined as differences between logic voltage parameters."
        },
        {
            "q": "In a CMOS NAND gate, how are the NMOS and PMOS transistors connected?",
            "opts": ["NMOS in series, PMOS in parallel", "NMOS in parallel, PMOS in series", "Both in series", "Both in parallel"],
            "ans": "NMOS in series, PMOS in parallel",
            "exp": "NAND pull-down requires both NMOS to conduct (series), while pull-up requires either PMOS to conduct (parallel)."
        },
        {
            "q": "In a CMOS NOR gate, how are the NMOS and PMOS transistors connected?",
            "opts": ["NMOS in series, PMOS in parallel", "NMOS in parallel, PMOS in series", "Both in series", "Both in parallel"],
            "ans": "NMOS in parallel, PMOS in series",
            "exp": "NOR pull-down requires either NMOS to conduct (parallel), while pull-up requires both PMOS to conduct (series)."
        },
        {
            "q": "When does short-circuit current flow in a CMOS logic gate?",
            "opts": ["During input transitions when both pull-up and pull-down networks are partially ON", "When Vin is stable at VDD", "When Vin is stable at GND", "Only in cut-off state"],
            "ans": "During input transitions when both pull-up and pull-down networks are partially ON",
            "exp": "As the input switches, both PMOS and NMOS conduct momentarily, creating a direct path from VDD to GND."
        },
        {
            "q": "What happens to the subthreshold leakage current of a transistor as temperature increases?",
            "opts": ["Increases exponentially", "Decreases lineally", "Remains constant", "Becomes zero"],
            "ans": "Increases exponentially",
            "exp": "Subthreshold current is exponentially dependent on thermal voltage, rising rapidly with temperature."
        },
        {
            "q": "What is the formula for gate overdrive voltage?",
            "opts": ["Vgs - Vth", "Vds - Vgs", "Vgs + Vth", "Vdd - Vth"],
            "ans": "Vgs - Vth",
            "exp": "Gate overdrive is the voltage excess over the threshold voltage: Vgs - Vth."
        },
        {
            "q": "Which region of operation has Vgs > Vth and Vds < Vgs - Vth?",
            "opts": ["Linear / Triode", "Saturation", "Cut-off", "Sub-threshold"],
            "ans": "Linear / Triode",
            "exp": "When drain voltage is below gate overdrive, the channel is continuous and acts as a voltage-controlled resistor."
        },
        {
            "q": "What is Drain-Induced Barrier Lowering (DIBL)?",
            "opts": ["Lowering of source barrier by high drain voltage", "Increasing Vth at low drain voltage", "Channel pinch-off", "Oxide gate rupture"],
            "ans": "Lowering of source barrier by high drain voltage",
            "exp": "In short channels, drain field lines reach the source, lowering the potential barrier and reducing Vth."
        },
        {
            "q": "What is the velocity saturation effect in short-channel devices?",
            "opts": ["Carrier velocity limiting at high lateral electric fields", "Clock frequency limits", "Diffusion current constraints", "Body effect increases"],
            "ans": "Carrier velocity limiting at high lateral electric fields",
            "exp": "High lateral fields cause carriers to scatter, saturating their speed and limiting maximum current."
        },
        {
            "q": "What is the physical subthreshold slope (SS) limit for planar silicon MOSFETs at room temperature (300K)?",
            "opts": ["60 mV/decade", "10 mV/decade", "100 mV/decade", "120 mV/decade"],
            "ans": "60 mV/decade",
            "exp": "Thermodynamics restricts the subthreshold slope of planar transistors to a minimum of ~60 mV/dec."
        },
        {
            "q": "What is the primary advantage of Silicon-on-Insulator (SOI) technology?",
            "opts": ["Reduced junction capacitances and latch-up immunity", "Higher threshold voltage", "Lower silicon cost", "Simple packaging design"],
            "ans": "Reduced junction capacitances and latch-up immunity",
            "exp": "The insulating layer isolates transistors, reducing parasitic source/drain capacitances and preventing latch-up."
        },
        {
            "q": "What is the dielectric material used in high-k metal gate (HKMG) technology?",
            "opts": ["Hafnium oxide", "Silicon dioxide", "Silicon nitride", "Aluminum"],
            "ans": "Hafnium oxide",
            "exp": "Hafnium-based oxides replace silicon dioxide to increase capacitance and reduce gate tunneling leakage."
        },
        {
            "q": "How does scaling the threshold voltage Vth affect static power consumption?",
            "opts": ["Increases subthreshold leakage exponentially", "Decreases leakage power", "Has no effect on static power", "Implements clock gating"],
            "ans": "Increases subthreshold leakage exponentially",
            "exp": "Lowering Vth increases subthreshold current exponentially, leading to high static leakage."
        },
        {
            "q": "What is the primary carrier in PMOS transistors?",
            "opts": ["Holes", "Electrons", "Ions", "Protons"],
            "ans": "Holes",
            "exp": "PMOS uses p-type channels where positive holes are the majority charge carriers."
        }
    ]

    # -------------------------------------------------------------
    # Topic 3: VLSI Design Flow (23 Unique Questions)
    # -------------------------------------------------------------
    quiz["VLSI Design Flow"] = [
        {
            "q": "Which design step translates RTL source code into physical gate cells?",
            "opts": ["Functional Verification", "Logic Synthesis", "Floorplanning", "Testing"],
            "ans": "Logic Synthesis",
            "exp": "Logic synthesis translates behavioral description (RTL) into a structural cell netlist."
        },
        {
            "q": "What check ensures that the physical geometric layout matches the electrical circuit schematic?",
            "opts": ["DRC (Design Rule Check)", "LVS (Layout vs Schematic)", "STA (Static Timing Analysis)", "ATPG"],
            "ans": "LVS (Layout vs Schematic)",
            "exp": "Layout vs Schematic (LVS) compares the layout connectivity against the logical schematic to ensure layout accuracy."
        },
        {
            "q": "In back-end physical design, 'CTS' stands for:",
            "opts": ["Chip Test Standard", "Clock Tree Synthesis", "Capacitor Timing System", "Cell Translation Stage"],
            "ans": "Clock Tree Synthesis",
            "exp": "Clock Tree Synthesis (CTS) builds the clock distribution network using buffers to minimize clock skew and jitter."
        },
        {
            "q": "Setup and hold time violations are verified during which procedure?",
            "opts": ["Functional simulation", "Design for Testability (DFT)", "Static Timing Analysis (STA)", "Logic synthesis"],
            "ans": "Static Timing Analysis (STA)",
            "exp": "STA is dedicated to verifying that the design meets all setup and hold timing constraints across all paths."
        },
        {
            "q": "What does Floorplanning define in Physical Design?",
            "opts": ["Core boundaries, power pad locations, and macro placements", "Logical equations", "RTL code syntax", "Test vectors"],
            "ans": "Core boundaries, power pad locations, and macro placements",
            "exp": "Floorplanning establishes chip dimensions, places I/O cells, and allocates space for macro blocks."
        },
        {
            "q": "What is 'routing' in the ASIC design flow?",
            "opts": ["Creating physical metal line connections between standard cells", "Simulating code test benches", "Partitioning logic gates", "Generating clock trees"],
            "ans": "Creating physical metal line connections between standard cells",
            "exp": "Routing connects standard cell pins using metal tracks while avoiding layout design rule violations."
        },
        {
            "q": "What does RTL stand for in the front-end design stage?",
            "opts": ["Register Transfer Level", "Routing Tree Layout", "Real Time Logic", "Receiver Timing Loop"],
            "ans": "Register Transfer Level",
            "exp": "RTL is a modeling style that describes digital circuits in terms of data flows between registers."
        },
        {
            "q": "What is the primary goal of Functional Verification?",
            "opts": ["Checking RTL behavior against functional specifications", "Optimizing gate cell layouts", "Inserting scan chains", "Testing silicon wafers"],
            "ans": "Checking RTL behavior against functional specifications",
            "exp": "Verification ensures the design logic operates correctly as defined in the specification."
        },
        {
            "q": "What is 'linting' in RTL design?",
            "opts": ["Static syntax and semantic checks on source code", "Dynamic simulation of logic gates", "Synthesis parameter overriding", "RC extraction"],
            "ans": "Static syntax and semantic checks on source code",
            "exp": "Linting statically reviews RTL code to flag coding style violations and potential hardware structural issues."
        },
        {
            "q": "What check ensures that layout geometries obey foundry spacing and width rules?",
            "opts": ["DRC (Design Rule Check)", "LVS", "STA", "ATPG"],
            "ans": "DRC (Design Rule Check)",
            "exp": "Design Rule Checking (DRC) verifies layouts satisfy sub-micron lithographic limits."
        },
        {
            "q": "What does ATPG do in DFT design?",
            "opts": ["Generates test patterns for manufacturing defect testing", "Runs timing constraints", "Optimizes power grids", "Compiles Verilog models"],
            "ans": "Generates test patterns for manufacturing defect testing",
            "exp": "ATPG (Automatic Test Pattern Generator) produces vectors to detect structural faults in fabricated ICs."
        },
        {
            "q": "What does BIST stand for in chip architecture?",
            "opts": ["Built-In Self-Test", "Bus Interface Setup Task", "Buffer Insertion Slack Tuning", "Binary Interface Simulation Tool"],
            "ans": "Built-In Self-Test",
            "exp": "BIST allows a circuit to test its own sub-blocks (like memory arrays) using embedded test hardware."
        },
        {
            "q": "How is timing slack defined?",
            "opts": ["Difference between required and actual arrival times", "The skew of clock trees", "Total delay of cell paths", "Clock period limit"],
            "ans": "Difference between required and actual arrival times",
            "exp": "Slack measures timing margin: positive slack means timing is met; negative slack is a violation."
        },
        {
            "q": "How do you resolve a setup timing violation?",
            "opts": ["Gate sizing, logic restructuring, or lower threshold cells", "Inserting delay buffers on the data path", "Increasing the clock frequency", "Bypassing STA verification"],
            "ans": "Gate sizing, logic restructuring, or lower threshold cells",
            "exp": "Setup is fixed by speeding up the critical path (sizing up cells, reducing logic depths, or using fast LVT cells)."
        },
        {
            "q": "How do you resolve a hold timing violation?",
            "opts": ["Inserting delay buffers on the data path", "Decreasing the clock frequency", "Reducing gate driver sizes", "Changing standard cells to HVT"],
            "ans": "Inserting delay buffers on the data path",
            "exp": "Hold is fixed by delaying fast data signals using buffers, ensuring data stays stable until the hold constraint is met."
        },
        {
            "q": "What is a multi-cycle path in STA?",
            "opts": ["A path designed to take more than one clock cycle to propagate data", "A clock domain crossover path", "An incorrect feedback loop", "A path with hold violations"],
            "ans": "A path designed to take more than one clock cycle to propagate data",
            "exp": "Multi-cycle paths are explicitly constrained to allow two or more clock cycles for signal propagation."
        },
        {
            "q": "What is a false path in timing analysis?",
            "opts": ["A path that cannot physically propagate signals or is timing-exempt", "A logic gate error", "A clock path with high skew", "A layout routing mistake"],
            "ans": "A path that cannot physically propagate signals or is timing-exempt",
            "exp": "False paths are declared to instruct the STA tool not to optimize or analyze non-functional timing paths."
        },
        {
            "q": "What is 'electromigration' in physical layouts?",
            "opts": ["Metal atom transport under high current density causing failure", "Signal coupling between parallel wires", "Gate oxide breakdown", "Charge accumulation on routing tracks"],
            "ans": "Metal atom transport under high current density causing failure",
            "exp": "High current density causes metal atoms to drift, leading to voids (opens) or hillocks (shorts) in wires."
        },
        {
            "q": "What format is the final layout database file released to the foundry for fabrication?",
            "opts": ["GDSII / OASIS", "Verilog Netlist", "SDC Timing file", "DEF Placement file"],
            "ans": "GDSII / OASIS",
            "exp": "GDSII and OASIS are standard stream formats representing physical layout geometries for photolithography."
        },
        {
            "q": "What does the term 'Tape-out' refer to?",
            "opts": ["Releasing final layout database (GDSII) to the foundry", "Wrapping finished chips in reels", "Running wafer logic tests", "Writing verilog testbenches"],
            "ans": "Releasing final layout database (GDSII) to the foundry",
            "exp": "Tape-out is the final milestone in the design cycle where the layout is shipped for mask fabrication."
        },
        {
            "q": "What is OCV (On-Chip Variation) in STA?",
            "opts": ["Process, voltage, and temperature variations across a single die", "Variations between wafer batches", "Clock phase differences", "Leakage variations on standard cells"],
            "ans": "Process, voltage, and temperature variations across a single die",
            "exp": "OCV models localized variation on the same silicon chip using derating factors."
        },
        {
            "q": "What is dynamic IR drop?",
            "opts": ["Transient power grid voltage drop during active clock transitions", "Static current leakage drop", "Electromigration in power grids", "Threshold voltage degradation"],
            "ans": "Transient power grid voltage drop during active clock transitions",
            "exp": "Dynamic IR drop is the voltage sag caused by high current draws during active clock transitions."
        },
        {
            "q": "What does DFT stand for in the design flow?",
            "opts": ["Design for Testability", "Dynamic Functional Timing", "Digital Filter Template", "Delay Fault Testing"],
            "ans": "Design for Testability",
            "exp": "DFT incorporates test features (like scan chains) into the design to facilitate structural silicon testing."
        }
    ]

    # -------------------------------------------------------------
    # Topic 4: Verilog Basics (23 Unique Questions)
    # -------------------------------------------------------------
    quiz["Verilog Basics"] = [
        {
            "q": "Which operator is used for non-blocking assignments in sequential Verilog blocks?",
            "opts": ["=", "<=", "==", "=>"],
            "ans": "<=",
            "exp": "The '<=' operator is non-blocking. It schedules parallel assignments at the end of the time step, preventing race conditions in sequential logic."
        },
        {
            "q": "A variable that stores its value procedures-wise and is assigned within 'always' blocks is declared as:",
            "opts": ["wire", "reg", "param", "assign"],
            "ans": "reg",
            "exp": "Variables assigned inside 'initial' or 'always' blocks must be declared as 'reg'."
        },
        {
            "q": "What represents the continuous assignment statement in Verilog dataflow modeling?",
            "opts": ["always", "assign", "initial", "always_comb"],
            "ans": "assign",
            "exp": "The 'assign' statement defines a continuous driver on a wire variable, re-evaluating instantly whenever inputs change."
        },
        {
            "q": "In Verilog, what does the operator '^' represent when applied to a single vector (e.g., ^bus)?",
            "opts": ["Bitwise XOR", "Exponential power", "Reduction XOR (parity check)", "Logical XOR"],
            "ans": "Reduction XOR (parity check)",
            "exp": "When placed before a single vector, '^' is a reduction operator that XORs all bits of that vector together, yielding a 1-bit result."
        },
        {
            "q": "What is the key difference between blocking (=) and non-blocking (<=) assignments?",
            "opts": ["Blocking executes sequentially; non-blocking executes concurrently in parallel", "Non-blocking blocks execution", "Blocking is only for registers", "Non-blocking requires wires"],
            "ans": "Blocking executes sequentially; non-blocking executes concurrently in parallel",
            "exp": "Blocking assignments update instantly before moving on. Non-blocking update at the end of the step."
        },
        {
            "q": "What is the scope of a 'localparam' constant in Verilog?",
            "opts": ["Restricted to the local module and cannot be overridden", "Global to the project", "Can be changed in testbenches", "Can be accessed by nested modules only"],
            "ans": "Restricted to the local module and cannot be overridden",
            "exp": "localparam declares constants that are locally protected from external parameter overrides."
        },
        {
            "q": "In `timescale 1ns/1ps, what do the terms represent?",
            "opts": ["1ns reference time unit, 1ps precision resolution", "1ns rise delay, 1ps fall delay", "1ns execution speed, 1ps sampling rate", "1ns clock period, 1ps jitter limit"],
            "ans": "1ns reference time unit, 1ps precision resolution",
            "exp": "The first number is the unit for time specifications; the second is the rounding precision."
        },
        {
            "q": "How do you override module parameters during module instantiation in Verilog?",
            "opts": ["Using #(.param_name(value)) syntax", "Using localparam statements", "Assigning value inside the testbench directly", "Recompining source files"],
            "ans": "Using #(.param_name(value)) syntax",
            "exp": "Named parameter override passes parameters during module instantiation using the '#' syntax."
        },
        {
            "q": "When does a procedural block always @(posedge clk) trigger?",
            "opts": ["On the rising edge of the clock signal", "On any clock edge", "When clk is stable at logic 1", "Continuously in parallel"],
            "ans": "On the rising edge of the clock signal",
            "exp": "posedge triggers the block execution when the clock transition goes from low to high."
        },
        {
            "q": "What is the default initial logic state of a 'wire' variable in Verilog simulation?",
            "opts": ["z (High Impedance)", "x (Unknown)", "0 (Logic Low)", "1 (Logic High)"],
            "ans": "z (High Impedance)",
            "exp": "Wires are high-impedance (z) by default until driven by an active gate or assign statement."
        },
        {
            "q": "What is the default initial logic state of a 'reg' variable in Verilog simulation?",
            "opts": ["z (High Impedance)", "x (Unknown)", "0 (Logic Low)", "1 (Logic High)"],
            "ans": "x (Unknown)",
            "exp": "Register variables store state and initialize to the unknown value (x) in simulation until assigned."
        },
        {
            "q": "How do you model a 2-to-1 Multiplexer using a ternary conditional operator?",
            "opts": ["assign y = sel ? i1 : i0;", "assign y = sel ? i0 : i1;", "always @(*) y = i1;", "assign y = sel & i1;"],
            "ans": "assign y = sel ? i1 : i0;",
            "exp": "If sel is 1, y gets i1, else y gets i0. This is the standard dataflow representation of a 2:1 MUX."
        },
        {
            "q": "What is the purpose of a 'generate' block in Verilog?",
            "opts": ["Looping or conditional instantiation of gates, modules, or variables", "Generating clock signals", "Compiling testbench values", "Defining timing constraints"],
            "ans": "Looping or conditional instantiation of gates, modules, or variables",
            "exp": "Generate blocks permit parameterized design structures to be duplicated or conditionally instantiated."
        },
        {
            "q": "What is a main difference between a 'task' and a 'function' in Verilog?",
            "opts": ["Tasks can consume time (delays); functions execute in zero simulation time", "Tasks cannot have outputs", "Functions can contain delays", "Tasks must return a direct value"],
            "ans": "Tasks can consume time (delays); functions execute in zero simulation time",
            "exp": "Functions cannot contain delays (#), wait, or event triggers (@) and must run in zero simulation time."
        },
        {
            "q": "Which system task prints variable transitions to the console only when their values change?",
            "opts": ["$monitor", "$display", "$write", "$strobe"],
            "ans": "$monitor",
            "exp": "$monitor registers variables and automatically prints messages when their values change."
        },
        {
            "q": "What is a Verilog testbench?",
            "opts": ["A non-synthesizable module used to apply stimuli and verify DUT behavior", "A physical prototype board", "A standard gate library", "A compiler command file"],
            "ans": "A non-synthesizable module used to apply stimuli and verify DUT behavior",
            "exp": "Testbenches apply simulation stimuli to design inputs and monitor outputs to verify functional behavior."
        },
        {
            "q": "In Verilog, what value does the literal representation 4'b10x0 represent?",
            "opts": ["4-bit binary vector with the second bit unknown", "Hexadecimal representation", "Undefined port connection", "High impedance vector"],
            "ans": "4-bit binary vector with the second bit unknown",
            "exp": "The literal represents a 4-bit binary value where bit 1 is '0', bit 2 is 'x' (unknown), bit 3 is '0', and bit 4 (MSB) is '1'."
        },
        {
            "q": "What does the sensitivity list syntax always @(*) do in Verilog-2001?",
            "opts": ["Creates an automatic sensitivity list for combinational logic procedural blocks", "Triggers only on clock positive edges", "Registers all system parameters", "Disables gate timing delays"],
            "ans": "Creates an automatic sensitivity list for combinational logic procedural blocks",
            "exp": "always @(*) automatically senses all variables read in the block, preventing latch creation due to missing signals."
        },
        {
            "q": "How do you model high impedance (Z) in Verilog code?",
            "opts": ["1'bz", "1'bx", "1'b0", "1'b1"],
            "ans": "1'bz",
            "exp": "High impedance is represented by the character 'z' or 'Z'."
        },
        {
            "q": "What is the structural model of a half adder using Verilog gate primitives?",
            "opts": ["xor(sum, a, b); and(cout, a, b);", "assign sum = a ^ b;", "always @(*) sum = a ^ b;", "or(sum, a, b);"],
            "ans": "xor(sum, a, b); and(cout, a, b);",
            "exp": "Structural modeling instantiates the gate primitives directly, connecting outputs first then inputs."
        },
        {
            "q": "How do you declare a parameter named 'WIDTH' with a default value of 8?",
            "opts": ["parameter WIDTH = 8;", "localparam WIDTH = 8;", "define WIDTH 8", "const int WIDTH = 8;"],
            "ans": "parameter WIDTH = 8;",
            "exp": "The parameter keyword defines module constants that can be overridden at instantiation."
        },
        {
            "q": "What is the behavior of the case equality operator (===) in Verilog?",
            "opts": ["Performs strict bitwise comparison including x and z states", "Ignores x and z states", "Forces value matching", "Converts values to decimal"],
            "ans": "Performs strict bitwise comparison including x and z states",
            "exp": "=== compares bits exactly, including matching unknown (x) and high-impedance (z) levels."
        },
        {
            "q": "Which system task terminates the active simulator execution?",
            "opts": ["$finish", "$stop", "$exit", "$terminate"],
            "ans": "$finish",
            "exp": "$finish exits the simulator and returns control to the operating system."
        }
    ]

    with open("/home/swami/vlsi_srm/questions_db.json", "w", encoding="utf-8") as f:
        json.dump({
            "flashcards": flashcards,
            "quiz": quiz
        }, f, indent=2)
        
    print(f"SUCCESS: questions_db.json generated with {len(flashcards)} unique flashcards and {sum(len(q_list) for q_list in quiz.values())} unique quiz questions!")

if __name__ == "__main__":
    generate_questions_db()
