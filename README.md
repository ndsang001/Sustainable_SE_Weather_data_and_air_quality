# Sustainable Software Engineering - Weather and Air Quality App

## Overview
This project is a Python-based GUI application that retrieves and analyzes weather and air quality data for a given city. It utilizes OpenWeather APIs to fetch real-time weather conditions and air pollution data and provides a visual representation of temperature and AQI correlation over time.

## Features
- Fetches real-time weather data (temperature, humidity, wind speed, etc.)
- Retrieves air quality data (AQI, PM2.5, PM10, NO2, SO2, CO levels)
- Saves retrieved data in a CSV file
- Provides a graphical analysis of temperature vs. air quality index (AQI)
- Displays weather icons and air quality information

## Technologies Used
- **Python** for backend logic
- **Tkinter** for GUI development
- **Requests** for API calls
- **Pandas** for data processing
- **Matplotlib** for visualization
- **Pillow** for image handling
- **Dotenv** for managing API keys

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/Sustainable_SE_Weather_data_and_air_quality.git
   cd Sustainable_SE_Weather_data_and_air_quality
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up the environment variables:
   - Create a `.env` file in the root directory.
   - Add the following line:
     ```sh
     API_KEY=your_openweather_api_key
     ```
   - Replace `your_openweather_api_key` with your actual OpenWeather API key.

## Usage
1. Run the application:
   ```sh
   python weather_app.py
   ```
2. Enter a city name in the input field and click **Search**.
3. View the real-time weather and air quality data.
4. Click **Analyze Data** to visualize temperature and AQI correlation over time.

## Example Output
### **Weather & Air Quality Display**
- Current temperature and description
- Air Quality Index (AQI) classification
- Weather icon display

### **Analysis & Visualization**
- Line graph comparing temperature and AQI over time
- CSV data storage for trend analysis

## API References
- [OpenWeather Geocoding API](https://openweathermap.org/api/geocoding-api)
- [OpenWeather Current Weather API](https://openweathermap.org/current)
- [OpenWeather Air Pollution API](https://openweathermap.org/api/air-pollution)

## Credits
- Inspired by [this YouTube tutorial](https://www.youtube.com/watch?v=_bPkhYVyqeA) and [source code](https://github.com/sprashantofficial/Python-Automation/blob/main/weather-app.py).

## License
This project is licensed under the MIT License.

