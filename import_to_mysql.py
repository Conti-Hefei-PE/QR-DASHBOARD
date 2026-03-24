import pandas as pd
import mysql.connector
import json
import os
import sys

# DB Config
DB_CONFIG = {
    "host": "10.246.97.159",
    "user": "root",
    "password": "root",
    "database": "QREP",
    "port": 3306
}

def migrate():
    excel_path = "QR.xlsx"
    if not os.path.exists(excel_path):
        print(f"Error: {excel_path} not found.")
        sys.exit(1)
        
    try:
        # 1. Read Excel
        print("Reading Excel...")
        df = pd.read_excel(excel_path)
        df_clean = df.where(pd.notnull(df), None) # Use None for NULL in SQL
        
        # 2. Connect to MySQL
        print("Connecting to MySQL...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 3. Create Table
        print("Creating Table...")
        # Drop if exists for clean state during dev
        cursor.execute("DROP TABLE IF EXISTS qr_cases;")
        
        create_table_sql = """
        CREATE TABLE qr_cases (
            id INT AUTO_INCREMENT PRIMARY KEY,
            qr_number INT,
            title VARCHAR(255),
            qr_status VARCHAR(50),
            failure_code VARCHAR(100),
            scope VARCHAR(100),
            trigger_area VARCHAR(100),
            trigger_date DATE,
            qr_owner VARCHAR(100),
            present_cannel VARCHAR(100),
            problem_severity TEXT,
            phenomenon TEXT,
            target TEXT,
            action TEXT,
            result TEXT,
            good_lead TEXT,
            evidence TEXT,
            conclusion TEXT,
            close_date DATE,
            duration FLOAT,
            next_step TEXT,
            ep_direction_1 TEXT,
            ep1_reliability VARCHAR(100),
            ep1_applicability VARCHAR(100),
            ep1_cost VARCHAR(100),
            ep1_races VARCHAR(100),
            ep_direction_2 TEXT,
            ep2_reliability VARCHAR(100),
            ep2_applicability VARCHAR(100),
            ep2_cost VARCHAR(100),
            ep2_races VARCHAR(100),
            ep_direction_3 TEXT,
            ep3_reliability VARCHAR(100),
            ep3_applicability VARCHAR(100),
            ep3_cost VARCHAR(100),
            ep3_races VARCHAR(100),
            next_step_executor VARCHAR(100),
            ep_category VARCHAR(100),
            item_type VARCHAR(100),
            path VARCHAR(255),
            phenomenon_image TEXT
        );
        """
        cursor.execute(create_table_sql)
        
        # 4. Insert Data
        print("Inserting Data...")
        insert_sql = """
        INSERT INTO qr_cases (
            qr_number, title, qr_status, failure_code, scope, trigger_area,
            trigger_date, qr_owner, present_cannel, problem_severity, phenomenon,
            target, action, result, good_lead, evidence, conclusion,
            close_date, duration, next_step,
            ep_direction_1, ep1_reliability, ep1_applicability, ep1_cost, ep1_races,
            ep_direction_2, ep2_reliability, ep2_applicability, ep2_cost, ep2_races,
            ep_direction_3, ep3_reliability, ep3_applicability, ep3_cost, ep3_races,
            next_step_executor, ep_category, item_type, path, phenomenon_image
        ) VALUES (
            %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, 
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        """
        
        batch = []
        for index, row in df_clean.iterrows():
            # Clean values
            qr_num = None
            try: qr_num = int(float(row['QR Number'])) if row['QR Number'] is not None else None
            except: pass
            
            # format trigger_date
            t_date = row.get('Trigger Date')
            try:
                t_date = str(t_date).split(' ')[0]
                if t_date in ["NaT", "nan", "None"]: t_date = None
            except: t_date = None
                
            c_date = row.get('Close Date')
            try:
                c_date = str(c_date).split(' ')[0]
                if c_date in ["NaT", "nan", "None"]: c_date = None
            except: c_date = None

            duration = None
            try: duration = float(row['Duration'])
            except: pass

            # Image extraction
            phenom = row.get('Phenomenon', '')
            image_url = ""
            if phenom and str(phenom).startswith('{'):
                try:
                    p_json = json.loads(phenom)
                    server_url = p_json.get('serverUrl', '')
                    relative_url = p_json.get('serverRelativeUrl', '')
                    if server_url and relative_url:
                        image_url = f"{server_url}{relative_url}"
                except: pass

            record = (
                qr_num, row.get('Title'), row.get('QR Status'), row.get('Failure Code'), row.get('Scope'), row.get('Trigger Area'),
                t_date, row.get('QR Owner'), row.get('Present Cannel'), row.get('Problem Severity'), row.get('Phenomenon'),
                row.get('Target'), row.get('Action'), row.get('Result'), row.get('Good Lead'), row.get('Evidence'), row.get('conclusion'),
                c_date, duration, row.get('Next Step'),
                row.get('Next Step Direction 1'), row.get('EP Direction 1: Reliability'), row.get('EP Direction 1: Applicability'), row.get('EP Direction 1: Cost'), row.get('EP Direction 1 RACES'),
                row.get('Next Step Direction 2'), row.get('EP Direction 2: Reliability'), row.get('EP Direction 2: Applicability'), row.get('EP Direction 2: Cost'), row.get('EP Direction 2 RACES'),
                row.get('Next Step Direction 3'), row.get('EP Direction 3: Reliability'), row.get('EP Direction 3: Applicability'), row.get('EP Direction 3: Cost'), row.get('EP Direction 3 RACES'),
                row.get('Next Step Executor'), row.get('EP Category'), row.get('Item Type'), row.get('Path'), image_url
            )
            batch.append(record)
            
        cursor.executemany(insert_sql, batch)
        conn.commit()
        print(f"Successfully inserted {cursor.rowcount} rows!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
