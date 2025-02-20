import tkinter as tk
from tkinter import messagebox
import requests
import os
from dotenv import load_dotenv
from PIL import Image, ImageTk
from io import BytesIO
import csv
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")
CSV_FILE = "weather_air_quality.csv"

def get_coordinates(city):
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"]
        else:
            messagebox.showerror("Error", f"City {city} not found")
    else:
        messagebox.showerror("Error", f"Geocoding API error: {response.status_code}")
    
    return None

def get_weather(coordinates):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={coordinates[0]}&lon={coordinates[1]}&appid={API_KEY}&units=metric"
    weather_response = requests.get(weather_url)

    if weather_response.status_code == 200:
        return weather_response.json()
    else:
        messagebox.showerror("Error", f"Weather API error: {weather_response.status_code}")
        return None

def get_air_quality(coordinates):
    air_quality_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={coordinates[0]}&lon={coordinates[1]}&appid={API_KEY}"
    air_quality_response = requests.get(air_quality_url)

    if air_quality_response.status_code == 200:
        return air_quality_response.json()['list'][0]
    else:
        messagebox.showerror("Error", f"Air Quality API error: {air_quality_response.status_code}")
        return None

def save_data(city, temperature, humidity, wind_speed, aqi, pm2_5, pm10, no2, so2, co):
    header = ["Timestamp", "City", "Temperature", "Humidity", "Wind Speed", "AQI", "PM2.5", "PM10", "NO2", "SO2", "CO"]
    data_row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        city, temperature, humidity, wind_speed, aqi, pm2_5, pm10, no2, so2, co
    ]
    try:
        with open(CSV_FILE, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
    except FileExistsError:
        pass
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data_row)

def analyze_data():
    df = pd.read_csv(CSV_FILE)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    plt.figure(figsize=(12, 5))
    plt.plot(df["Timestamp"], df["Temperature"], label="Temperature (°C)", marker="o")
    plt.plot(df["Timestamp"], df["AQI"], label="Air Quality Index (AQI)", marker="s")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Temperature vs. Air Quality Index Over Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()
    correlation_matrix = df[["Temperature", "Humidity", "Wind Speed", "AQI", "PM2.5", "PM10"]].corr()
    print("Correlation Matrix:")
    print(correlation_matrix)

def show_weather_and_air_quality():
    city = city_entry.get()
    if city:
        coordinates = get_coordinates(city)
        if coordinates:
            weather_data = get_weather(coordinates)
            air_data = get_air_quality(coordinates)
            if weather_data and air_data:
                temp = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']
                wind_speed = weather_data['wind']['speed']
                aqi = air_data['main']['aqi']
                pm2_5 = air_data['components']['pm2_5']
                pm10 = air_data['components']['pm10']
                no2 = air_data['components']['no2']
                so2 = air_data['components']['so2']
                co = air_data['components']['co']
                update_weather_display(weather_data)
                update_air_quality_display(air_data)
                save_data(city, temp, humidity, wind_speed, aqi, pm2_5, pm10, no2, so2, co)
    else:
        messagebox.showerror("Error", "Please enter a city name.")

def update_weather_display(weather_data):
    temp = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    icon_code = weather_data['weather'][0]['icon']
    weather_label.config(text=f"{temp}°C, {description.title()}")
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    icon_response = requests.get(icon_url)
    if icon_response.status_code != 200:
        print(f"Error fetching weather icon: {icon_response.status_code}")
        messagebox.showerror("Error", f"Failed to load weather icon. Status code: {icon_response.status_code}")
        return

    try:
        icon_image = Image.open(BytesIO(icon_response.content))
        icon_image = icon_image.resize((100, 100), Image.Resampling.LANCZOS)

        icon_photo = ImageTk.PhotoImage(icon_image)
        weather_icon_label.config(image=icon_photo)
        weather_icon_label.image = icon_photo
    except Exception as e:
        print(f"Error processing weather icon: {e}")
        messagebox.showerror("Error", "Failed to process weather icon image.")

def update_air_quality_display(air_data):
    aqi = air_data['main']['aqi']
    pollutants = air_data['components']
    air_quality_class = classify_air_quality(aqi)
    air_quality_label.config(text=f"Air quality index (AQI): {aqi} ({air_quality_class})")
    pollutants_label.config(
        text=f"PM2.5 {pollutants['pm2_5']} µg/m3\nPM10: {pollutants['pm10']} µg/m3\nNO2: "
            f"{pollutants['no2']} µg/m3\nSO2: {pollutants['so2']} µg/m3\nCO: "
            f"{pollutants['co']} µg/m3"
    )

def classify_air_quality(aqi):
    if aqi == 1:
        return "Good"
    elif aqi == 2:
        return "Moderate"
    elif aqi == 3:
        return "Unhealthy for Sensitive Groups"
    elif aqi == 4:
        return "Unhealthy"
    else:
        return "Hazardous"
        

root = tk.Tk()
root.title("Weather and Air Quality App")
root.geometry("600x800")
root.configure(bg="#2A2A2A")

# Top frame
top_frame = tk.Frame(root, bg="#2A2A2A", bd=5)
top_frame.pack(pady=20)
title_label = tk.Label(top_frame, text="Weather and Air Quality App", font=("Helvetica", 20, "bold"), fg="white", bg="#2A2A2A")
title_label.pack()

# City Entry
input_frame = tk.Frame(root, bg="#2A2A2A")
input_frame.pack(pady=10)
city_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=20, bd=2, relief="flat", fg="white", bg="#333333", insertbackground="white")

city_entry.pack(side=tk.LEFT, padx=10)

# Search button
search_btn = tk.Button(input_frame, text="Search", font=("Helvetica", 14), bg="#00AAFF", fg="white", activebackground="#00CCFF",
                       relief="flat", padx=10, pady=5, command=show_weather_and_air_quality)
search_btn.pack(side=tk.LEFT)

# Weather display section
weather_frame = tk.Frame(root, bg="#2A2A2A")
weather_frame.pack(pady=20)
weather_label = tk.Label(weather_frame, text="Weather: --", font=("Helvetica", 16), fg="white", bg="#2A2A2A")
weather_label.pack()
weather_icon_label = tk.Label(weather_frame, bg="#2A2A2A")
weather_icon_label.pack(pady=10)

# Air quality section
pollution_frame = tk.Frame(root, bg="#2A2A2A")
pollution_frame.pack(pady=20)
air_quality_label = tk.Label(pollution_frame, text="Air quality index (AQI): --", font=("Helvetica", 16), fg="white",
                             bg="#2A2A2A")
air_quality_label.pack(pady=10)
pollutants_label = tk.Label(pollution_frame, text="PM2.5: --, PM10: --, NO2: --, SO2: --, CO: --",
                           font=("Helvetica", 14), fg="white", bg="#2A2A2A", justify="left")
pollutants_label.pack()

analyze_btn = tk.Button(root, text="Analyze Data", font=("Helvetica", 14), bg="#FFA500", fg="white", activebackground="#FFB833", relief="flat", padx=10, pady=5, command=analyze_data)
analyze_btn.pack(pady=10)

root.mainloop()