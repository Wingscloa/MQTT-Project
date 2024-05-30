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

# Přidání middleware pro povolení CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Povolit všechny zdroje
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Funkce pro získání připojení k databázi
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST','db'),  # Adresa hostitele databáze
        user=os.getenv('DB_USER', 'root'),  # Uživatelské jméno pro připojení k databázi
        database=os.getenv('DB_NAME', 'dcuk_mqtt')  # Název databáze
    )
# Model senzoru pro validaci a serializaci dat
# class Sensor(BaseModel):
#     id: int
#     nazev: str
#     typ: str
#     misto: str
#     frekvence: str
#     stav: str
#     count_records: int

# Endpoint pro získání seznamu senzorů
@app.get("/senzory")
def get_senzory():
    conn = get_db_connection()  # Získání připojení k databázi
    cursor = conn.cursor(dictionary=True)
    
    # Dotaz na získání seznamu senzorů s počtem záznamů
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

# Endpoint pro získání počtu záznamů za poslední minutu
@app.get("/pocetzaminutu")
def get_zaminutu():
    conn = get_db_connection()  # Získání připojení k databázi
    cursor = conn.cursor(dictionary=True)
    
    timezone = datetime.timezone(datetime.timedelta(hours=2)) # Časové pásmo pro cesko
    current_time = datetime.datetime.now(timezone)  # Aktuální čas
    print(f"current time  {current_time}")
    one_minute_ago = current_time - datetime.timedelta(minutes=1)  # Čas před jednou minutou
    print(current_time.strftime('%Y-%m-%d %H:%M:%S'))
    print(one_minute_ago.strftime('%Y-%m-%d %H:%M:%S'))
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

# Endpoint pro získání počtu senzorů
@app.get("/pocetsenzoru")
def get_sensors():
    conn = get_db_connection()  # Získání připojení k databázi
    cursor = conn.cursor(dictionary=True)
    
    # Dotaz na počet senzorů
    query = "SELECT COUNT(*) as count FROM senzory"
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result

# Endpoint pro graf ze zaznamu RAW DATA (CAS -> Pocet poslanych zaznamu)

@app.get("/grafzaznamu/raw")
def graf_zaznamu():
    conn = get_db_connection()  # Získání připojení k databázi
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT z.cas FROM zaznamy as z"
        cursor.execute(query)
        result = cursor.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        result = None

    finally:
        cursor.close()
        conn.close()

    return result



@app.get("/grafzaznamu/graf", response_class=HTMLResponse)
def graf_zaznamu_graf():
    conn = get_db_connection()  # Get database connection
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT z.cas FROM zaznamy as z"
        cursor.execute(query)
        results = cursor.fetchall()

        # Convert the results to a DataFrame
        df = pd.DataFrame(results)
        df['cas'] = pd.to_datetime(df['cas'])

        # Group by hour and count records
        df['hour'] = df['cas'].dt.floor('H')
        hourly_counts = df.groupby('hour').size().reset_index(name='counts')

        # Create a Plotly graph
        fig = px.line(hourly_counts, x='hour', y='counts', title='Number of Records per Hour')

        # Generate HTML for the graph
        graph_html = fig.to_html(full_html=False)

    except Exception as e:
        print(f"Error: {e}")
        return f"<h1>Error: {e}</h1>"

    finally:
        cursor.close()
        conn.close()

    return HTMLResponse(content=graph_html)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=5000)  # Spuštění aplikace na portu 5000
