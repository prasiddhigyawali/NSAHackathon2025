# NSAHackathon2025/ Team - greenwise.ai 


# 🌱 Krisi Sahayak – AI-Powered Farmer Assistant

**Krisi Sahayak** is a web application developed by Greenwise.ai to assist farmers in Nepal. Utilizing Google Cloud APIs, it offers voice and text-based agricultural guidance in Nepali and local dialects, providing real-time weather updates and localized crop recommendations.

## 🎯 Mission

To empower Nepalese farmers with a voice-driven AI assistant that delivers **real-time market and weather insights**, helping them increase profitability while collecting crucial agricultural data for future planning and analysis.

---

## 🌟 Vision

To create the **first central repository of agricultural data in Nepal**, empowering:  
- Farmers with personalized advice  
- NGOs with ground realities  
- Policymakers with actionable insights  

This will help shape the future of food security in Nepal.
---

## 🚀 Features

- **🗣️ Voice & Text Interaction:** Communicate in Nepali or local dialects using Google Cloud's Speech-to-Text and Text-to-Speech APIs.
- **🤖 AI-Powered Recommendations:** Receive personalized crop and yield advice powered by Google Gemini LLM.
- **🌦️ Weather Updates:** Access location-based weather forecasts for informed farming decisions.
- **📊 Data Logging:** Store user interactions and responses in Google Cloud for future analysis.
- **🖥️ User-Friendly Interface:** Navigate a simple, visual dashboard designed for farmers.

---

## 🛠️ Tech Stack

- **Frontend:** Django Templates (HTML, CSS)
- **Backend:** Django + REST API
- **AI Integration:** OpenAI ChatGPT LLM
- **Cloud Services:** Google Cloud Speech-to-Text, Text-to-Speech, Cloud Storage
- **Version Control:** Git, GitHub

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/prasiddhigyawali/NSAHackathon2025.git
cd NSAHackathon2025

```
### 2️⃣ Backend Setup (Django)
```bash
cd backend
python -m venv venv
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```
(Optional for now) Set up Google Cloud credentials:
```
set GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
```

#### Run the server:
```
python manage.py runserver
```
3️⃣ Frontend Access

Access the application via local server http://127.0.0.1:8000/. 




### 🔮 Future Enhancements

- Ethnic Language Model: Expand to create the first AI model specifically trained for Nepali ethnic languages and dialects, ensuring truly localized voice and text interaction.

- Mobile Application: Offline-capable version for broader accessibility.

- NGO/INGO and Government Partnerships: Collaborate to scale impact and insights.


## 👨‍🌾 Team Greenwise.ai

🌱 Adishri Pradhan – Team Lead

🌱 Drishya Shrestha - Software Engineer

🌱 Prabesh Sunar - Business Analyst

🌱 Prasiddhi Gyawali - Software Engineer
