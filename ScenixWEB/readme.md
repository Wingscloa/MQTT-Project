# Scenix Dashboard

## Introduction
Scenix Dashboard is a web-based application designed to monitor and visualize sensor data in real-time. It provides a user-friendly interface to display sensor statuses, historical data, and other critical metrics.

Use with [Scenix api](https://github.com/JP1Q/scenixapi)

## Table of Contents
- [Introduction](#introduction)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/JP1Q/scenixweb
    ```
2. Navigate to the project directory:
    ```sh
    cd scenixweb
    ```
3. Install the dependencies:
    ```sh
    npm install
    ```

## Usage
1. Start the server:
    ```sh
    npm start
    ```
2. Open your browser and navigate to `http://localhost:3000` to view the dashboard.

## Features
- **Real-Time Data Fetching:** Continuously updates sensor data, sensor counts, and records every minute.
- **Dynamic Sensor Cards:** Displays detailed information for each sensor in an interactive card format.
- **Theme Switching:** Toggle between light and dark themes for the dashboard.
- **Historical Data Visualization:** Uses Plotly.js to plot historical data for each sensor.
- **Responsive Design:** Mobile-friendly and adapts to different screen sizes.
- **Search Functionality:** Filter sensors based on their type using the search bar.

## Dependencies
- [Bootstrap 5](https://getbootstrap.com/)
- [Plotly.js](https://plotly.com/javascript/)
- [jQuery](https://jquery.com/)
- [Google Fonts - Roboto](https://fonts.google.com/specimen/Roboto)

## Configuration
- **API Endpoints:**
  - Fetch Sensor Data: `http://127.0.0.1:5000/senzory`
  - Fetch Sensor Count: `http://127.0.0.1:5000/pocetsenzoru`
  - Fetch Records in Last Minute: `http://127.0.0.1:5000/pocetzaminutu`

## Documentation
- **fetchSensorData():** Fetches data for all sensors.
- **fetchSensorCount():** Retrieves the total number of sensors.
- **fetchRecordsInLastMinute():** Gets the number of records in the last minute.
- **generateSensorCards():** Creates sensor cards dynamically based on the fetched data.
- **updatePlotlyTheme(theme):** Updates the Plotly graph theme based on the current theme (light or dark).
- **showModal(sensor):** Displays a modal with historical data for the selected sensor.
- **filterSensorCardsByTyp(query):** Filters sensor cards based on the search query.

## Examples
```javascript
// Fetch sensor data
const sensors = await fetchSensorData();
console.log(sensors);

// Fetch sensor count
const sensorCount = await fetchSensorCount();
console.log(sensorCount);

// Fetch records in last minute
const recordsInLastMinute = await fetchRecordsInLastMinute();
console.log(recordsInLastMinute);
```

## Troubleshooting
- **Issue:** Sensor data is not updating.
  - **Solution:** Check if the API server is running and accessible.
- **Issue:** Theme does not switch.
  - **Solution:** Verify the CSS files for the themes are correctly linked in the HTML.

## Contributors
- [Aroteo](https://github.com/JP1Q)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to update any section or add more details as per your project requirements!