# 📊 Graduation Project Interface

A web-based dashboard interface developed to provide users with a centralized platform for accessing data-driven reports, KPIs, and interactive Power BI dashboards.

The application combines a Flask backend with a responsive web interface and embedded Power BI reports to provide an interactive data analysis experience.

---

## 🚀 Project Overview

This project provides a centralized interface where authenticated users can:

- 🔐 Log in securely to the platform
- 📊 Access interactive Power BI dashboards
- 📈 View KPI and data analysis reports
- 📅 Navigate between different reporting years
- 👤 View and manage user profile information
- 📝 Report problems related to dashboards or pages
- 🔎 Navigate between different dashboard sections

The Flask application controls authentication, routing, user information, dashboard navigation, and Power BI report integration.

---

## 🛠️ Technologies Used

### Backend
- Python
- Flask

### Frontend
- HTML5
- CSS3
- JavaScript

### Data Visualization
- Microsoft Power BI
- Power BI Embedded Reports

### Development Tools
- Git
- GitHub
- PyCharm / VS Code

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Web Interface     │
                    │ HTML / CSS / JS      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Flask Backend    │
                    │                     │
                    │ Authentication      │
                    │ Routing             │
                    │ Sessions             │
                    │ User Profiles       │
                    │ Dashboard Control   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Power BI        │
                    │ Interactive Reports │
                    │ KPIs & Analytics    │
                    └─────────────────────┘
