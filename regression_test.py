import os
import sys
import json
import py_compile

def run_regression():
    print("==================================================")
    print("         VLSI SRM PORTAL REGRESSION TEST          ")
    print("==================================================")
    
    # Use relative workspace directory to ensure portability
    workspace_dir = os.path.dirname(os.path.abspath(__file__))
    pages_dir = os.path.join(workspace_dir, "pages")
    
    # List of python files to compile
    python_files = [
        os.path.join(workspace_dir, "app.py"),
        os.path.join(workspace_dir, "style_utils.py"),
        os.path.join(workspace_dir, "generate_verilog_examples.py"),
        os.path.join(workspace_dir, "generate_questions.py")
    ]
    
    # Add files in pages dir
    if os.path.exists(pages_dir):
        for f in os.listdir(pages_dir):
            if f.endswith(".py"):
                python_files.append(os.path.join(pages_dir, f))
            
    print(f"Found {len(python_files)} Python files to verify.")
    
    # 1. Compile Checks
    compile_failures = 0
    for fpath in python_files:
        try:
            py_compile.compile(fpath, doraise=True)
            print(f"[PASS] Compile: {os.path.basename(fpath)}")
        except Exception as e:
            print(f"[FAIL] Compile: {os.path.basename(fpath)} - {str(e)}")
            compile_failures += 1
            
    # 2. Database Validation: verilog_db.json
    verilog_failures = 0
    v_db_path = os.path.join(workspace_dir, "verilog_db.json")
    print("\nValidating verilog_db.json...")
    try:
        with open(v_db_path, "r", encoding="utf-8") as f:
            v_db = json.load(f)
        print(f"[PASS] Load verilog_db.json (Count: {len(v_db)})")
        
        # Verify structure of elements
        invalid_keys = []
        for k, v in v_db.items():
            required_keys = ["category", "desc", "rtl", "tb", "traces", "is_combinational", "allow_edit"]
            missing = [rk for rk in required_keys if rk not in v]
            if missing:
                invalid_keys.append((k, missing))
        if not invalid_keys:
            print("[PASS] verilog_db.json structural schema verification.")
        else:
            print(f"[FAIL] verilog_db.json contains invalid schema for keys: {invalid_keys}")
            verilog_failures += 1
    except Exception as e:
        print(f"[FAIL] Load verilog_db.json - {str(e)}")
        verilog_failures += 1
        
    # 3. Database Validation: questions_db.json
    question_failures = 0
    q_db_path = os.path.join(workspace_dir, "questions_db.json")
    print("\nValidating questions_db.json...")
    try:
        with open(q_db_path, "r", encoding="utf-8") as f:
            q_db = json.load(f)
        
        # Validate flashcards schema
        flashcards = q_db.get("flashcards", [])
        print(f"[PASS] Load questions_db.json -> flashcards (Count: {len(flashcards)})")
        invalid_fc_keys = []
        for idx, fc in enumerate(flashcards):
            required_fc_keys = ["id", "category", "topic", "question", "answer"]
            missing = [rk for rk in required_fc_keys if rk not in fc]
            if missing:
                invalid_fc_keys.append((f"flashcards[{idx}]", missing))
        if not invalid_fc_keys:
            print("[PASS] flashcards structural schema verification.")
        else:
            print(f"[FAIL] flashcards contains invalid schema for keys: {invalid_fc_keys}")
            question_failures += 1
            
        # Validate quiz schema
        quiz = q_db.get("quiz", {})
        print(f"[PASS] Load questions_db.json -> quiz (Count of sections: {len(quiz)})")
        invalid_quiz_keys = []
        for cat, q_list in quiz.items():
            for idx, q in enumerate(q_list):
                required_q_keys = ["q", "opts", "ans", "exp"]
                missing = [rk for rk in required_q_keys if rk not in q]
                if missing:
                    invalid_quiz_keys.append((f"quiz[{cat}][{idx}]", missing))
        if not invalid_quiz_keys:
            print("[PASS] quiz structural schema verification.")
        else:
            print(f"[FAIL] quiz contains invalid schema for keys: {invalid_quiz_keys}")
            question_failures += 1
            
    except Exception as e:
        print(f"[FAIL] Load questions_db.json - {str(e)}")
        question_failures += 1
        
    print("\n==================================================")
    total_failures = compile_failures + verilog_failures + question_failures
    if total_failures == 0:
        print("          ALL REGRESSION TESTS PASSED!            ")
        print("==================================================")
        sys.exit(0)
    else:
        print(f"          REGRESSION FAILED WITH {total_failures} ERRORS           ")
        print("==================================================")
        sys.exit(1)

if __name__ == "__main__":
    run_regression()
