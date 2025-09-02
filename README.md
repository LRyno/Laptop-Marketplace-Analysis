# 💻 Laptop Marketplace Analysis  

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)  
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-yellow.svg)](https://pandas.pydata.org/)  
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-green.svg)](https://matplotlib.org/)  
[![Seaborn](https://img.shields.io/badge/Seaborn-EDA-orange.svg)](https://seaborn.pydata.org/)  

📊 A complete project that scrapes, cleans, and analyzes laptop product data from **Tokopedia** marketplace.  
This repository is part of my Data Analyst learning journey, showcasing end-to-end data workflow.  

---

## 📌 Project Overview  
- ✅ Scraped laptop product data from **Tokopedia**  
- ✅ Collected key features: `Product Name`, `Price`, `Location`, `Rating`, `Units Sold`  
- ✅ Cleaned and processed raw dataset  
- ✅ Performed **Exploratory Data Analysis (EDA)**  
- ✅ Visualized insights using Python  

---

## ⚙️ Tech Stack  
- **Python** (Pandas, NumPy, Matplotlib, Seaborn, Requests, BeautifulSoup/Selenium)  
- **Jupyter Notebook** for analysis  
- **GitHub** for version control & portfolio  

---

## ⚙️ Setup ChromeDriver

This project uses **Selenium** for web scraping on Tokopedia.  
To run it, make sure you have downloaded **chromedriver** that matches your Google Chrome version.

- Check your Chrome version at `chrome://settings/help`.
- Download chromedriver: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
- Place `chromedriver.exe` in this project folder (or adjust the path in `scraping.py`).

> Note: The `chromedriver.exe` file is **not uploaded to GitHub** due to its large size and security reasons.

---

## 📊 Key Insights  
- 💡 **Average Rating by Brand** → Microsoft, Spc, Tecno are the 3 brands with the highest ratings
- 💡 **Average Price by Brand** → MSI is a laptop brand with the most expensive average price
- 💡 **Brand Distribution Based on Seller Location** → Asus & Lenovo have many sellers in the Jakarta area
- 💡 **Brand Popularity Map Based on Sales Volume per Location** → Jakarta Utara dominate laptop sellers  
- 💡 **Brand Popularity by Price Volume** → The average buyer likes low to medium prices
- 💡 **Popular Locations Based on Satisfaction Ratings** → The most popular and satisfying location is the Jakarta

---

## 🚀 Future Improvements  
- 🔍 Add sentiment analysis on customer reviews  
- 📈 Build  more interactive dashboard (Streamlit/PowerBI)  
- 🌐 Compare across multiple e-commerce platforms  

---

## ✨ Author  
Made with ❤️ by **Syamza Ryno Lingga Mawanta**  
📩 Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/rynolingga/) or check out my other projects!  

---
