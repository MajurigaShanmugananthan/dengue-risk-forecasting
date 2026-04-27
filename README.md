# 🦟 Dengue Risk Forecasting System

An AI-powered mobile application that predicts dengue risk using real-time climate data, location, and machine learning.

---

## 📌 Overview

This project aims to help users identify dengue risk levels in their area using environmental and historical data. The system integrates a machine learning model with a mobile application to provide real-time predictions and alerts.

---

## 🎯 Objectives

- Predict dengue risk (Low, Medium, High)
- Use real-time weather data (temperature, rainfall, wind)
- Provide user-friendly explanations (Explainable AI)
- Alert users when risk is high
- Visualize location-based risk using a map

---

## 🧠 Technologies Used

### Frontend
- Flutter (Dart)
- OpenStreetMap (flutter_map)

### Backend
- Flask (Python)

### Machine Learning
- Random Forest Classifier
- Scikit-learn
- SHAP (Explainable AI)

### APIs
- Weather API (real-time climate data)

---

## ⚙️ System Architecture

1. User location is obtained via GPS
2. Weather data is fetched using API
3. Data is sent to backend
4. Machine learning model predicts risk
5. SHAP generates explanations
6. Results are displayed in mobile app
7. Alerts are triggered if risk is high

---

## 📊 Features

- 📍 Location-based dengue risk prediction  
- 🌦️ Real-time weather integration  
- 🧠 Explainable AI (why this prediction?)  
- 🔔 Notification alerts  
- 🗺️ Map visualization  
- 📈 Probability-based risk levels  

---

## 📱 App Screens

Example:
![Home Screen](screenshots/home.png)

---

## 🚀 How to Run the Project

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
