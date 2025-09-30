# FinHub Zen - Integrated Financial Management Platform

## 🚀 Overview

FinHub Zen is a comprehensive financial management platform that integrates three powerful tools with a modern React frontend:

1. **AI Tax Helper** - Smart tax deduction categorization and receipt processing
2. **Financial Insights** - Advanced spending analytics and transaction insights  
3. **Zero-Click Budgeting** - Automated budget tracking from SMS/UPI/receipts

## 📁 Project Structure

```
C:\Users\Ruhani\OneDrive - UPES\Documents\Unstop\
├── main_backend.py           # Unified Flask backend serving all 3 tools
├── requirements.txt          # Python dependencies
├── test_integration.py       # API integration tests
├── start-all.ps1            # PowerShell startup script
├── start_backend.cmd        # Backend startup script
├── start_frontend.cmd       # Frontend startup script
├── package-lock.json        # Node.js lock file
├── finhub-zen/              # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Application pages
│   │   │   ├── Dashboard.tsx
│   │   │   ├── TaxHelper.tsx
│   │   │   ├── Insights.tsx
│   │   │   ├── Budgeting.tsx
│   │   │   ├── Search.tsx      # ✅ NEW - Cross-platform search
│   │   │   ├── Security.tsx    # ✅ NEW - Account security
│   │   │   └── Settings.tsx    # ✅ NEW - App preferences
│   │   ├── layout/          # Layout components
│   │   └── ui/              # shadcn/ui components
│   ├── package.json         # Frontend dependencies
│   └── vite.config.ts       # Vite configuration
├── ai-tax-helper/           # Individual tool directory
├── insights/                # Individual tool directory
├── zero-click-budgeting/    # Individual tool directory
└── venv/                    # Python virtual environment
```

## 🛠️ Technology Stack

### Backend
- **Python 3.13.7** - Core runtime
- **Flask 2.3.3** - Web framework
- **Flask-CORS 4.0.0** - Cross-Origin Resource Sharing
- **python-dateutil 2.8.2** - Date parsing utilities

### Frontend  
- **React 18.3.1** - UI library
- **TypeScript** - Type safety
- **Vite 5.4.19** - Build tool and dev server
- **Tailwind CSS** - Styling framework
- **shadcn/ui** - Component library
- **Radix UI** - Headless UI primitives
- **Lucide React** - Icon library
- **React Router DOM** - Client-side routing
- **TanStack Query** - Data fetching
- **Recharts** - Data visualization

## 🚀 Quick Start

### Option 1: Use the Startup Script (Recommended)
```powershell
# Navigate to project directory
cd "C:\Users\Ruhani\OneDrive - UPES\Documents\Unstop"

# Run the startup script
.\start-all.ps1
```

### Option 2: Manual Startup

#### Start Backend
```powershell
cd "C:\Users\Ruhani\OneDrive - UPES\Documents\Unstop"
python main_backend.py
```

#### Start Frontend (in another terminal)
```powershell
cd "C:\Users\Ruhani\OneDrive - UPES\Documents\Unstop\finhub-zen"
npm run dev
```

## 🌐 Access URLs

- **Frontend Application**: http://localhost:8081
- **Backend API**: http://localhost:5000  
- **Health Check**: http://localhost:5000/health

## 📋 Features & Pages

### Core Financial Tools
1. **Dashboard** - `/` - Integrated overview of all financial data
2. **AI Tax Helper** - `/tax-helper` - Smart tax management
3. **Financial Insights** - `/insights` - Spending analytics and trends
4. **Zero-Click Budgeting** - `/zero-click-budgeting` - Automated budget tracking

### Additional Features (NEW)
5. **Search** - `/search` - Cross-platform search across all financial data
6. **Security** - `/security` - Account security and authentication management
7. **Settings** - `/settings` - Application preferences and configuration

## 🔌 API Endpoints

### Tax Helper APIs
- `GET /api/tax/categorized` - Get categorized transactions
- `GET /api/tax/summary` - Get tax deduction summary
- `POST /api/tax/upload-receipt` - Process receipt uploads

### Insights APIs  
- `GET /api/insights/spending-by-category` - Spending breakdown
- `GET /api/insights/monthly-trends` - Monthly spending trends
- `GET /api/insights/transactions` - Recent transactions
- `POST /api/insights/ingest/sms` - Process SMS transactions

### Budgeting APIs
- `GET /budget/gauge` - Current budget status
- `GET /budget/transactions` - All budget transactions
- `POST /budget/set-limit` - Set monthly budget limit
- `POST /webhook/sms` - SMS transaction webhook
- `POST /webhook/upi` - UPI transaction webhook  
- `POST /webhook/receipt` - Receipt transaction webhook

### General APIs
- `GET /health` - System health check
- `GET /api/dashboard-summary` - Dashboard overview data

## 🧪 Testing

### Run Integration Tests
```powershell
cd "C:\Users\Ruhani\OneDrive - UPES\Documents\Unstop"
python test_integration.py
```

This will test all API endpoints with dummy data and verify functionality.

### Frontend Build Test
```powershell
cd "C:\Users\Ruhani\OneDrive - UPES\Documents\Unstop\finhub-zen"
npm run build
```

## 📊 Demo Data

The application includes comprehensive dummy/demo data:

- **8 budget transactions** with realistic spending patterns
- **Sample tax records** with business/personal categorization
- **Monthly spending trends** across 6 months
- **Category breakdowns** for Food, Transportation, Shopping, etc.
- **Mock receipts and SMS transactions**

## 🔧 Development

### Backend Development
```powershell
# Install dependencies
pip install -r requirements.txt

# Run in development mode (with auto-reload)
python main_backend.py
```

### Frontend Development
```powershell
# Install dependencies
cd finhub-zen
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## 🚨 Troubleshooting

### Frontend Shows Blank Page
If you see a blank page, check the browser console for errors and ensure:
1. Backend is running on port 5000
2. Frontend built successfully (`npm run build`)
3. No TypeScript compilation errors

### Port Conflicts
- Backend uses port 5000 (Flask default)
- Frontend tries 5173 first, then 8080, then 8081
- Check for port conflicts if services won't start

### CORS Issues  
The backend includes CORS headers for local development. If you encounter CORS errors, ensure both services are running on the expected ports.

## 📝 Recent Updates

### Latest Changes (2025-09-29)
- ✅ **Added Search functionality** - Cross-platform search with filters
- ✅ **Added Security page** - 2FA, password management, biometric auth
- ✅ **Added Settings page** - Theme switching, notifications, profile management
- ✅ **Fixed theme provider** - Added missing `useTheme` export
- ✅ **Updated routing** - All sidebar links now functional
- ✅ **Enhanced UI components** - Modern, responsive design

## 🤝 Contributing

1. Ensure both backend and frontend build successfully
2. Test all API endpoints using the integration test script
3. Verify UI functionality across all pages
4. Update this README with any new features

## 📄 License

This project is part of the Unstop challenge submission.

---

**Happy Financial Management!** 💰📊✨