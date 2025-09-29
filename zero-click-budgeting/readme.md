Zero-Click Budgeting (Standalone Module)

Purpose
- Hands-free budgeting from SMS/UPI/receipts.
- Background ingestion builds budgets automatically.
- Real-time budget fuel gauge: Green (safe), Red (overspending).

Run Locally (dev)
- API: `cd api && npm i && npm run start`
- Budget Engine tests: `cd budget-engine && python -m venv venv && venv/Scripts/activate && pip install -r requirements.txt && pytest`
- Frontend: `cd frontend && npm i && npm run dev`

Integration
- Send events to `POST /webhook/{sms|upi|receipt}`.
- Read current gauge at `GET /budget/gauge`.
- Replace in-memory queue with real bus (RabbitMQ/Kafka) later.