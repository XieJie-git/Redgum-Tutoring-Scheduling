# Redgum Tutoring Scheduling System
A web‑based application for session scheduling and tracking at the Redgum Tutoring Center.

## Prerequisites
- Python 3.10+
- pip

## Setup Instructions
1. Clone the repository:
```bash
git clone https://github.com/XieJie‑git/Redgum‑Tutoring‑Scheduling.git
cd Redgum‑Tutoring‑Scheduling

# Create virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Environment configuration
cp .env-sample .env

# Start Flask application
flask --app src/app.py run

# Run unit tests
pytest
