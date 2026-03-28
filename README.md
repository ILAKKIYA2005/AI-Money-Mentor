# MONEY MIRROR AI – Smart Financial Mentor

A futuristic, AI-powered personal finance application designed with a Neon-Glassmorphism aesthetic to help users track expenses, receive AI-driven financial advice, and discover Indian government schemes.

## Tech Stack

- **Frontend**: React.js, Tailwind CSS, Framer Motion, Chart.js, Lucide React
- **Backend**: Python FastAPI, Motor (Async MongoDB), Pydantic, JWT, Bcrypt
- **Database**: MongoDB
- **AI Layer**: Rule-based logic with predictive capabilities (expandable to LLMs)

## Key Features

1.  **Neon Dashboard**: A modern, high-tech interface with real-time analytics.
2.  **AI Financial Advisor**: Calculates health scores, suggests SIP amounts, and provides monthly insights.
3.  **Expense Core**: Add/Edit/Delete expenses with AI classification (Essential vs. Non-essential).
4.  **Transaction Sync**: Upload CSV files to auto-populate the ledger.
5.  **Smart Notifications**: Predictive alerts for EMIs, bills, and recharges based on past behavior.
6.  **Govt. Scheme Recommender**: Automatic suggestions of Indian schemes based on user occupation and age.

## Setup Instructions

### Backend Setup
1. Navigate to `backend/`
2. Create a virtual environment: `python -m venv venv`
3. Activate venv: `source venv/bin/activate` or `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Ensure MongoDB is running on `localhost:27017`
6. Run the server: `uvicorn main:app --reload`

### Frontend Setup
1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Start the dev server: `npm run dev`
4. Access at `http://localhost:5173`

## Directory Structure
```text
money-mirror-ai/
├── backend/
│   ├── models/       # Pydantic data schemas
│   ├── routes/       # API endpoints (Auth, User, Expenses, AI)
│   ├── services/     # AI Agent & Business logic
│   ├── database.py   # MongoDB connection
│   └── main.py       # FastAPI entry point
└── frontend/
    ├── src/
    │   ├── components/ # Reusable UI widgets
    │   ├── context/    # Auth handling
    │   ├── pages/      # Main application views
    │   └── api.js      # Axios configuration
    └── tailwind.config.js # Neon theme setup
```

## Security
- JWT for session management.
- Bcrypt for secure password storage.
- Input validation via Pydantic.
- CORS protection.
