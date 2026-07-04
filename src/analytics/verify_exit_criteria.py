import os
import sqlite3

def check_sprint2_exit_criteria():
    db_path = "database/nifty100.db"
    log_path = "output/ratio_edge_cases.log"
    
    print("\n" + "="*60)
    print(" 🛠️  AUTOMATED SPRINT 2 EXIT CRITERIA CHECKER ")
    print("="*60)
    
    # 1. Database and Table Existence
    if not os.path.exists(db_path):
        print("❌ CRITERIA FAILED: database/nifty100.db file missing!")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='financial_ratios';")
    if not cursor.fetchone():
        print("❌ CRITERIA FAILED: 'financial_ratios' table does not exist!")
        conn.close()
        return

    # --- CRITERIA 1: Row Count >= 1100 ---
    cursor.execute("SELECT COUNT(*) FROM financial_ratios;")
    total_rows = cursor.fetchone()[0]
    
    if total_rows >= 1100:
        print(f"✅ PASS: Total Row Count is {total_rows} (Requirement: >= 1100)")
    else:
        print(f"❌ FAIL: Total Row Count is only {total_rows} (Requirement: >= 1100)")

    # --- CRITERIA 2: 14 KPI Columns and Zero Null-Only Columns ---
    cursor.execute("PRAGMA table_info(financial_ratios);")
    columns = [col[1] for col in cursor.fetchall()]
    total_columns = len(columns)
    
    # Check for null-only columns
    null_only_cols = []
    for col in columns:
        cursor.execute(f"SELECT COUNT(*) FROM financial_ratios WHERE {col} IS NOT NULL;")
        if cursor.fetchone()[0] == 0:
            null_only_cols.append(col)
            
    if total_columns >= 14 and len(null_only_cols) == 0:
        print(f"✅ PASS: Found {total_columns} KPI columns and 0 null-only columns.")
    else:
        print(f"❌ FAIL: Columns count is {total_columns} or Null-only columns found: {null_only_cols}")

    conn.close()

    # --- CRITERIA 3: Log File and Explanations ---
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check if logs contain categories/explanations
        has_explanations = "Category:" in content or "mismatch" in content
        total_anomalies = content.count("👉")
        
        if total_anomalies > 0 and has_explanations:
            print(f"✅ PASS: ratio_edge_cases.log exists with {total_anomalies} categorized entries.")
        else:
            print("❌ FAIL: Log file exists but lacks proper anomaly formats.")
    else:
        print("❌ FAIL: output/ratio_edge_cases.log file does not exist!")

    print("="*60 + "\n")

if __name__ == "__main__":
    check_sprint2_exit_criteria()