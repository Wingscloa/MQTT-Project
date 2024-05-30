from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import mysql.connector
import os
import datetime
import plotly.express as px
import pandas as pd
import logging

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to get database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'mariadb'), 
            user=os.getenv('DB_USER', 'dcuk_user'),
            password=os.getenv('DB_PASSWORD', 'dcuk'),
            database=os.getenv('DB_NAME', 'dcuk_mqtt_docker')
        )
        return conn
    except mysql.connector.Error as err:
        logger.error(f"Error connecting to database: {err}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Endpoint to get sensor list
@app.get("/senzory")
def get_senzory():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
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
    except Exception as e:
        logger.error(f"Error fetching sensors: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to get record count in the last minute
@app.get("/pocetzaminutu")
def get_zaminutu():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        timezone = datetime.timezone(datetime.timedelta(hours=2))
        current_time = datetime.datetime.now(timezone)
        one_minute_ago = current_time - datetime.timedelta(minutes=1)
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
    except Exception as e:
        logger.error(f"Error fetching record count: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint to get sensor count
@app.get("/pocetsenzoru")
def get_sensors():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT COUNT(*) as count FROM senzory"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        logger.error(f"Error fetching sensor count: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/modal/")

@app.get("/grafzaznamu/raw")
def graf_zaznamu():
    conn = get_db_connection()  # Získání připojení k databázi
    cursor = conn.cursor(dictionary=True)

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
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
    # except Exception as e:
    #     logger.error(f"Error fetching raw graph data: {e}")
    #     raise HTTPException(status_code=500, detail="Internal Server Error")

    # return result



@app.get("/grafzaznamu/graf", response_class=HTMLResponse)
def graf_zaznamu_graf():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT z.cas FROM zaznamy as z"
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.DataFrame(results)
        df['cas'] = pd.to_datetime(df['cas'])
        df['hour'] = df['cas'].dt.floor('H')
        hourly_counts = df.groupby('hour').size().reset_index(name='counts')
        fig = px.line(hourly_counts, x='hour', y='counts', title='Number of Records per Hour')
        graph_html = fig.to_html(full_html=False)
        cursor.close()
        conn.close()
        return HTMLResponse(content=graph_html)
    except Exception as e:
        logger.error(f"Error generating graph: {e}")
        return HTMLResponse(content=f"<h1>Error: {e}</h1>", status_code=500)

@app.get("/grafzaznamu/{sensor_id}")
def graf_zaznamu_sensor(sensor_id: int):
    conn = get_db_connection()  # Získání připojení k databázi
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT z.cas FROM zaznamy z WHERE z.id_sen = %s"
        cursor.execute(query, (sensor_id,))
        results = cursor.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        return f"<h1>Error: {e}</h1>"

    finally:
        cursor.close()
        conn.close()

    return results

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)  # Spuštění aplikace na portu 5000
