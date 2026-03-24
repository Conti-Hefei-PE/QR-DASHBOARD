import pandas as pd
import json
import os
import sys

def inspect_and_convert():
    file_path = "QR.xlsx"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        sys.exit(1)
        
    try:
        # Read Excel file
        # openpyxl is needed for xlsx
        df = pd.read_excel(file_path)
        
        # Print column info
        print("--- Column Information ---")
        for col in df.columns:
            print(f"- {col} (Type: {df[col].dtype})")
            
        print("\n--- Shape ---")
        print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        
        print("\n--- Sample Data (First Row) ---")
        print(df.head(1).to_dict(orient='records'))
        
        # Convert to JSON for frontend
        # Handle nan values to avoid invalid JSON or just clean them
        df_clean = df.where(pd.notnull(df), "")
        
        # Convert date columns to string to avoid serialization issues
        for col in df_clean.columns:
            if 'date' in col.lower() or 'time' in col.lower() or 'duration' in col.lower():
                 # Try to convert to str
                 try:
                    df_clean[col] = df_clean[col].astype(str)
                 except:
                     pass
        
        json_data = df_clean.to_dict(orient='records')
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
            
        print("\nSuccessfully converted to data.json")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    inspect_and_convert()
