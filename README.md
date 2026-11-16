# 🚌 Cádiz Bus IoT — Real-Time Fleet Monitoring

An end-to-end telemetry and smart management system for the urban public transit network of **Cádiz, Spain**. The project simulates a connected bus fleet using the **MQTT** protocol, offering both an **operations control dashboard** with AI-powered predictive alerts and a **real-time web application** for passengers.

> 🏆 **Award-Winning Challenge Project:** Developed as part of the **[Líderes Digitales Universitarios](https://www.telefonica.es/es/compromiso/red-de-catedras-telefonica/lideres-digitales-universitarios/)** program organized by the **Red de Cátedras Telefónica** ([Cátedra Telefónica - Universidad de Cádiz](https://catedratelefonica.uca.es/)), where this solution **won the local phase**.

## ✨ Key Features

### 1. IoT Telemetry Simulator (`script.py`)

* **Realistic Geolocation:** Simulates the routes of 15 buses across Cádiz's main lines (**L1, L2, L3, L5, and L7**) following real city coordinates.

* **Vehicle Status:** Dynamically calculates driving direction, onboard sensor battery levels, and GPS position fluctuations.

* **Incident Simulation:** Generates random traffic, weather, or road incident events that feed into the alert system.

### 2. Operations Dashboard (`dashboard.html`)

* **Live Interactive Map:** Global fleet visualization over Esri/Leaflet cartography with smooth updates every 2 seconds.

* **Inventory & Filtering:** Side panel displaying battery status, GPS coordinates, and direction for each unit, filterable by bus line.

* **AI Predictive Alerts:** Dedicated module that automatically detects and notifies operators of potential connection losses due to critical battery levels ($< 20\%$) and service delays.

### 3. Passenger Web App (`app_usuarios.html`)

* **Mobile-First Interface:** Clean, responsive design tailored for mobile devices at bus stops.

* **Quick Line Filters:** Top selector with official color codes to instantly locate buses on a specific route.

* **Passenger Notifications:** Displays real-time delay warnings directly on each bus card.

## 🛠️ Architecture & Tech Stack

```
[ script.py (IoT Simulator) ]
             │
             ▼  (Publishes JSON via MQTT / TCP)
   [ MQTT Broker (EMQX) ]
             │
             ├──► (WebSockets Subscription) ──► [ dashboard.html (Operators) ]
             └──► (WebSockets Subscription) ──► [ app_usuarios.html (Passengers) ]

```

* **Backend / Simulation:** Python 3, `paho-mqtt`

* **IoT Protocol:** MQTT over TCP (port `1883`) and MQTT over Secure WebSockets (`wss://`, port `8084`)

* **Frontend:** HTML5, CSS3, Vanilla JavaScript

* **Maps & Visualization:** Leaflet.js + ArcGIS World Street Map

## 🚀 Installation & Usage

### 1. Clone the repository

```
git clone https://github.com/your-username/cadiz-bus-iot.git
cd cadiz-bus-iot

```

### 2. Install Python dependencies

Make sure you have Python 3 installed, then install the MQTT client library:

```
pip install paho-mqtt

```

### 3. Start the fleet simulator

Run the main script to start broadcasting bus telemetry:

```
python script.py

```

*You will see `Telemetría enviada...` printed in your console every 2 seconds.*

### 4. Open the web interfaces

No additional web server is required. Simply open either of the HTML files in your favorite browser:

* **`dashboard.html`**: To access the fleet control center and technical alerts.

* **`app_usuarios.html`**: To test the passenger/commuter view.

## 📁 Project Structure

```
├── script.py           # Bus simulator and MQTT telemetry publisher
├── dashboard.html      # Fleet control panel and predictive alerts
├── app_usuarios.html   # Commuter tracking web application
├── icon.png            # Application favicon (optional)
└── README.md           # Project documentation

```

## 📝 Technical Notes

* This project uses the public testing broker `broker.emqx.io` under the topic `reto_telefonica/cadiz/flota_global`.

* Location data, battery drain, and traffic incidents are synthetically generated for demonstration purposes.