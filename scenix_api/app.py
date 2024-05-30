from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import mysql.connector
import os
import datetime
import plotly.express as px
import pandas as pd

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to establish database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'db'),  # Adresa hostitele databáze
        user=os.getenv('DB_USER', 'root'),  # Uživatelské jméno pro připojení k databázi
        password=os.getenv('DB_PASSWORD', ''),  # Heslo pro připojení k databázi
        database=os.getenv('DB_NAME', 'sensory_debug')  # Název databáze
    )

# Model senzoru pro validaci a serializaci dat
class Sensor(BaseModel):
    id: int
    nazev: str
    typ: str
    misto: str
    frekvence: str
    stav: str
    count_records: int

# Endpoint to retrieve list of sensors
@app.get("/senzory")
def get_senzory():
    conn = get_db_connection()  # Get database connection
    cursor = conn.cursor(dictionary=True)
    
    # Query to get list of sensors with record count
    query = """
    SELECT s.id_sen, s.nazev, s.typ, s.misto, s.frekvence, st.barva as stav, 
           (SELECT COUNT(*) FROM zaznamy z WHERE z.id_sen = s.id_sen) as count_records
    FROM senzory s
    JOIN stav st ON s.id_stav = st.id_stav
    GROUP BY s.nazev
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    sensors = [
        {
            "id": row["id_sen"],
            "nazev": row["nazev"],
            "typ": row["typ"],
            "misto": row["misto"],
            "frekvence": row.get("frekvence"),
            "stav": row["stav"],
            "count_records": row["count_records"]
        }
        for row in rows
    ]
    
    cursor.close()
    conn.close()
    
    return sensors

# Endpoint to retrieve record count for the last minute
@app.get("/pocetzaminutu")
def get_zaminutu():
    conn = get_db_connection()  # Get database connection
    cursor = conn.cursor(dictionary=True)
    
    current_time = datetime.datetime.now()  # Aktuální čas
    one_minute_ago = current_time - datetime.timedelta(minutes=1)  # Čas před jednou minutou
    
    # Dotaz na počet záznamů mezi current_time a one_minute_ago
    query = """
    SELECT COUNT(*) as count
    FROM zaznamy
    WHERE cas BETWEEN %s AND %s
    """
    
    cursor.execute(query, (one_minute_ago.strftime('%Y-%m-%d %H:%M:%S'), current_time.strftime('%Y-%m-%d %H:%M:%S')))
    
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result

# Endpoint to retrieve sensor count
@app.get("/pocetsenzoru")
def get_sensors():
    conn = get_db_connection()  # Get database connection
    cursor = conn.cursor(dictionary=True)
    
    # Query to count sensors
    query = "SELECT COUNT(*) as count FROM senzory"
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)  # Spuštění aplikace na portu 5000
