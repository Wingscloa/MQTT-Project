# Project Title: MQTT Sensor Data Management

## Introduction
This project involves a system to manage sensor data using MQTT (Message Queuing Telemetry Transport) protocol. The project includes database setup scripts, an MQTT client for receiving sensor data, and Python code for handling the data and interacting with a MySQL database. It is designed to process sensor data, categorize it, and store it in a structured format for easy retrieval and analysis.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
4. [Dependencies](#dependencies)
5. [Configuration](#configuration)
6. [Documentation](#documentation)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)
9. [Contributors](#contributors)
10. [License](#license)

## Installation
### Prerequisites
- Python 3.x
- MySQL server
- `paho-mqtt` library
- `geopy` library
- `pymysql` library

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/Wingscloa/MQTT-Project
   cd MQTT-Project
   ```
2. Install the required Python packages:
   ```sh
   pip install paho-mqtt geopy pymysql
   ```
3. Set up the MySQL database:
   ```sql
   CREATE DATABASE DCUK_MQTT;

   USE DCUK_MQTT;

   CREATE TABLE senzory
   (
     id_sen    BIGINT         NOT NULL AUTO_INCREMENT UNIQUE COMMENT 'ano',
     nazev     VARCHAR(20)    NOT NULL COMMENT 'ano',
     typ       TEXT           NOT NULL COMMENT 'ano',
     frekvence DECIMAL(10, 2) NULL     COMMENT 'ano',
     misto     VARCHAR(60)    NULL     COMMENT 'ano',
     id_stav   BIGINT         NOT NULL DEFAULT 1,
     PRIMARY KEY (id_sen)
   );

   CREATE TABLE stav
   (
     id_stav BIGINT      NOT NULL AUTO_INCREMENT UNIQUE,
     nazev   VARCHAR(20) NULL    ,
     popis   TEXT        NULL     COMMENT 'pricina',
     barva   VARCHAR(20) NULL     COMMENT 'color v hex',
     PRIMARY KEY (id_stav)
   );

   CREATE TABLE zaznamy
   (
     id_zaz BIGINT      NOT NULL AUTO_INCREMENT UNIQUE COMMENT 'NE',
     id_sen BIGINT      NOT NULL COMMENT 'ano',
     cas    TIMESTAMP   NOT NULL DEFAULT now() COMMENT 'NE',
     počasí VARCHAR(20) NULL     COMMENT 'NE',
     PRIMARY KEY (id_zaz)
   );

   ALTER TABLE zaznamy
     ADD CONSTRAINT FK_senzory_TO_zaznamy
       FOREIGN KEY (id_sen)
       REFERENCES senzory (id_sen);

   ALTER TABLE senzory
     ADD CONSTRAINT FK_stav_TO_senzory
       FOREIGN KEY (id_stav)
       REFERENCES stav (id_stav);
   ```

4. Insert initial data into the `stav` table:
   ```sql
   INSERT INTO stav (nazev, popis, barva) VALUES 
   ('vypocet_zac', 'Tento stav indikuje, že výpočet právě začal. Všechny systémy by měly být připravené na spuštění úloh.', "#DE9A26"), 
   ('vypocet_pru', 'Tento stav znamená, že výpočet právě probíhá. Systémy aktivně zpracovávají data a vykonávají úlohy.', '#DEB126'),
   ('vypocet_skoro', 'Tento stav naznačuje, že výpočet je téměř dokončen. Systémy by měly připravovat finální kroky a závěrečné operace.', "#DEC726"),
   ('funguje', 'Tento stav signalizuje, že vše funguje bez problémů. Systémy jsou v normálním provozu a nejsou detekovány žádné chyby.', "#5FDE26"),
   ('bacha', 'Tento stav upozorňuje na potenciální problém nebo varování. Systémy by měly být monitorovány, ale zatím není nutný zásah.', '#7B8945'),
   ('neco se deje', 'Tento stav indikuje, že se v systému děje něco neočekávaného. Může být potřeba bližší analýza nebo zásah.', "#DE266C"),
   ('pohni', 'Tento stav znamená, že je potřeba rychlý zásah. Systémy mohou být v kritickém stavu a vyžadují okamžitou pozornost.', '#FF0E00');
   ```

## Usage
1. Update the MQTT and database configuration in the Python script (`mqtt_client.py`):
   ```python
   
   db = _mysql.Database()
   ```

2. Run the MQTT client script:
   ```sh
   python mqtt_client.py
   ```

3. The script will connect to the MQTT broker, subscribe to all topics, and process incoming messages. Sensor data will be inserted into the `senzory` and `zaznamy` tables in the MySQL database.

## Features
- **MQTT Client**: Connects to an MQTT broker and subscribes to topics to receive sensor data.
- **Data Processing**: Parses incoming messages and extracts relevant information.
- **Database Interaction**: Inserts sensor data into MySQL tables and ensures data integrity through transaction management.

## Dependencies
- Python 3.x
- MySQL server
- `paho-mqtt` library
- `geopy` library
- `pymysql` library

## Configuration
- **MQTT Broker**: Update the `MQTT_HOST`, `MQTT_PORT`, `MQTT_USER`, and `MQTT_PASSWORD` variables in the script with the appropriate credentials.
- **Database**: Ensure the MySQL database is set up with the correct schema and initial data. Update the database connection settings in the `Database` class.

## Documentation
### Database Schema
- **`senzory` Table**:
  - `id_sen`: Sensor ID (Primary Key)
  - `nazev`: Sensor name
  - `typ`: Sensor type
  - `frekvence`: Frequency
  - `misto`: Location
  - `id_stav`: State ID

- **`stav` Table**:
  - `id_stav`: State ID (Primary Key)
  - `nazev`: State name
  - `popis`: Description
  - `barva`: Color in hex

- **`zaznamy` Table**:
  - `id_zaz`: Record ID (Primary Key)
  - `id_sen`: Sensor ID (Foreign Key)
  - `cas`: Timestamp
  - `počasí`: Weather

### Python Script
- **`on_connect`**: Callback function for successful MQTT connection.
- **`on_message`**: Callback function for receiving messages.
- **`publish_message`**: Function to send messages to the MQTT broker.
- **`Database` Class**: Handles database operations including inserting sensors and records, and checking if a sensor exists.

## Examples
### Publishing a Test Message
```python
publish_message("/hackithon/test", "Hello, MQTT!")
```

### Inserting Sensor Data
```python
data = {
    "nazev": "sensor1",
    "typ": "temperature",
    "misto": "office"
}
db.insert_senzorV3(data)
```

## Troubleshooting
- **Connection Issues**: Ensure the MQTT broker credentials are correct and the broker is running.
- **Database Errors**: Check the MySQL database setup and ensure the correct schema is used. Verify the database connection settings in the Python script.

## Contributors
- [Wingscloa](https://github.com/Wingscloa)

## License
This project is licensed under the MIT License.
