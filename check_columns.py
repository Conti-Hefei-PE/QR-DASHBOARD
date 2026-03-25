import mysql.connector

def check_columns():
    try:
        conn = mysql.connector.connect(
            host='10.246.97.159',
            user='root',
            password='root',
            database='QREP'
        )
        cursor = conn.cursor()
        cursor.execute("DESCRIBE qr_cases")
        columns = cursor.fetchall()
        print("Columns in qr_cases:")
        for col in columns:
            print(col[0])
        conn.close()
    except Exception as e:
        print("Error connecting to DB:", e)

if __name__ == "__main__":
    check_columns()
