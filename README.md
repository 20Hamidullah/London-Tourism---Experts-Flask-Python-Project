# 🚖 London Tourism & Transport — Full-Stack Web Application

A production-ready, fully dynamic web application built for a London-based 
tourist pick-and-drop service. Designed to modern UI/UX standards with a 
secure admin control interface for complete content management.

---

## ✨ Features

- **Chatbot** -This project includes an AI chatbot designed to answer questions related to London tourism and transport services. Instead of relying on a single AI provider, the chatbot uses a fallback architecture: it first attempts to generate a response through Groq, then Hugging Face, and finally a safe fallback message if both are unavailable. This approach improves uptime, reduces the impact of quota limits, and makes the chatbot more resilient for users.
- **Responsive UI** — Mobile-first design that adapts seamlessly across all 
  screen sizes and devices
- **Dynamic Content** — Posts and service listings are fetched directly from 
  a live database with pagination support
- **Alternating Post Layout** — Clean image-text layout that alternates 
  per post for an engaging reading experience
- **Admin Dashboard** — Secure control panel allowing the admin to create, 
  edit, and delete posts in real time
- **Authentication** — Protected admin routes to prevent unauthorised access
- **SEO-Friendly Slugs** — Human-readable URLs generated automatically for 
  every post
- **Optimised Card Components** — Service cards with responsive typography, 
  trust signals, and clear CTAs
- **About & Contact Pages** — Purpose-built pages designed to build user 
  trust and drive enquiries

---

## 🛠️ Tech Stack

| Layer       | Technology                          |
|-------------|--------------------------------------|
| Backend     | Python, Flask, SQLAlchemy            |
| Frontend    | HTML5, CSS3, Bootstrap 5, Jinja2     |
| Database    | MySQL                                |
| Icons       | Bootstrap Icons                      |

---
# London Tourism & Experts Chatbot

An AI-powered assistant designed to support visitors with transport inquiries, including airport pickups, hotel transfers, tourist site logistics, pricing, and booking information.

## AI Chatbot Features

This project features a resilient, AI-powered chatbot designed to ensure constant availability for our users.

* **Smart Fallback Architecture**: To maintain high reliability without relying on a single paid service, the chatbot employs a multi-provider fallback system:
    1. **Primary**: Uses **Groq** for high-speed AI responses.
    2. **Secondary**: Automatically fails over to the **Hugging Face Inference API** if Groq is unavailable or rate-limited.
    3. **Safety Net**: Returns a custom, branded fallback message if all AI providers are unreachable.
* **Tourism-Focused**: The model is custom-instructed to handle only transport and tourism-related queries, maintaining a friendly and professional tone.
* **Booking Integration**: If users express intent to book, the chatbot proactively provides direct contact options (WhatsApp/Email).

## Installation

Ensure you have [Python](https://python.org) installed, then install the necessary dependencies:

```bash
pip install flask python-dotenv groq huggingface_hub
```

## Environment Configuration

This project uses environment variables to keep your API keys secure. Create a `.env` file in the root directory of your project and add your credentials:

```env
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```

*Note: Ensure your `.env` file is included in your `.gitignore` to prevent accidental exposure of your keys.*

## Usage

Once configured, run the Flask application:

```bash
python main.py
```

The chatbot will then be accessible via the configured API route.

## Chatbot Workflow

1. **Request**: The frontend sends a user message to the `/chat` POST endpoint.
2. **Processing**: The application attempts to generate a response via the `generate_with_fallback` logic.
3. **Resilience**: 
   - The system iterates through the defined providers (`Groq` → `Hugging Face`).
   - Exceptions are logged internally, allowing the system to switch to the backup provider immediately.
4. **Response**: A clean JSON response is returned to the user, including the name of the provider that successfully fulfilled the request for monitoring purposes.


## 📸 Screenshots
![websitePreview1](screenShots/websitePreview1.PNG)
![websitePreview2](screenShots/websitePreview2.PNG)
![websitePreview3](screenShots/websitePreview3.PNG)
![websitePreview4](screenShots/websitePreview4.PNG)
![websitePreview5](screenShots/websitePreview5.PNG)
---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/20Hamidullah/London-Tourism---Experts-Flask-Python-Project.git
cd London-Tourism---Experts-Flask-Python-Project

# Create a virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
flask run
```

### Admin Access
Navigate to `/admin` and log in with the following admin logini credentials to access 
the post management dashboard.
-username: admin
password: admin

---

## 📁 Project Structure

london-tourism/
├── static/
│   ├── assets/img/          # Post and service images
│   └── css/                 # Custom stylesheets
├── templates/
│   ├── layout.html            # Base layout
│   ├── index.html           # Homepage with paginated posts
│   ├── about.html           # About us page
│   ├── contact.html         # Contact page
│   └── admin/               # Admin dashboard templates
├── main.py                   # Main Flask application

## 👤 Author

**Sayed Hamidullah Fazlly**  
[LinkedIn](www.linkedin.com/in/sayed-hamidullah-fazlly-382489170) · 

