import pandas as pd
import json
import os
import sys

def build_data():
    file_path = "QR.xlsx"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        sys.exit(1)
        
    try:
        # Read Excel
        df = pd.read_excel(file_path)
        
        # Clean data
        df_clean = df.where(pd.notnull(df), "")
        
        records = df_clean.to_dict(orient='records')
        
        processed_records = []
        for row in records:
            # Process Dates
            # Trigger Date, Close Date
            for k in ['Trigger Date', 'Close Date']:
                 if row.get(k):
                     try:
                         # convert to str if not already
                         row[k] = str(row[k]).split(' ')[0] # just YYYY-MM-DD
                         if row[k] == "NaT" or row[k] == "nan":
                              row[k] = ""
                     except:
                          row[k] = ""
                          
            # Process Duration
            if row.get('Duration'):
                 try:
                      row['Duration'] = float(row['Duration'])
                 except:
                      pass
                      
            # Process Phenomenon Images
            phenom = row.get('Phenomenon', '')
            row['PhenomenonImage'] = ""
            if phenom and phenom.startswith('{'):
                try:
                    p_json = json.loads(phenom)
                    server_url = p_json.get('serverUrl', '')
                    relative_url = p_json.get('serverRelativeUrl', '')
                    if server_url and relative_url:
                        row['PhenomenonImage'] = f"{server_url}{relative_url}"
                except:
                    pass
            
            # Ensure QR Number is integer or nicely formatted string
            if row.get('QR Number'):
                try:
                    row['QR Number'] = int(float(row['QR Number']))
                except:
                    pass
                    
            processed_records.append(row)
            
        # Write to data.js
        with open('data.js', 'w', encoding='utf-8') as f:
            f.write("window.QR_DATA = ")
            json.dump(processed_records, f, ensure_ascii=False, indent=2)
            f.write(";")
            
        print("\nSuccessfully built data.js with image previews!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_data()
