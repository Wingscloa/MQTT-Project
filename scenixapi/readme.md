# Scenix API

Scenix api je flask-based api

## Endpointy


### Získání všech senzorů v DB

- **Endpoint:** `/senzory`
- **Method:** `GET`
- **Description:** Vrátí list všech senzorů v DB s detaily.

### Příklad vrácených dat:

```sql
[
    {
        "id": 1,
        "nazev": "Sensor 1",
        "typ": "Temperature",
        "misto": "Room 1",
        "frekvence": 60.0,
        "stav": "#FFFFFF"
    },
    {
        "id": 2,
        "nazev": "Sensor 2",
        "typ": "Humidity",
        "misto": "Room 2",
        "frekvence": 30.0,
        "stav": "#FFFFFF"
    }
]
```

### 2. Počet zápisů v poslední minutě

- **Endpoint**: ``/pocetzaminutu``
- **Method**: ``GET``
- **Description**: ``Vrátí počet zápisů v poslední minutě``

### Příklad

```sql
{
    "count": 5
}
```

### Počet senzorů

- **Endpoint**: ``/pocetsenzoru``
- **Method**: ``GET``
- **Description**: ``Vrátí počet všech senzorů v DB``

### Příklad

```sql
{
    "count": 10
}
```


### Počet zápisů pro určitý senzor

- **Endpoint**: ```/pocet_records```
- Method: `GET`
- Description: `Returns the count of records for a specific sensor.`
- Query Parameter: `id_sensoru`

#### Příklad req.
```sh
curl "http://127.0.0.1:5000/pocet_records?id_sensoru=2"
```

### Příklad outputu

```sql
{
    "count": 50
}
```