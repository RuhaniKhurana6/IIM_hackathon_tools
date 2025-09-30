# FinHub Zen Startup Script
Write-Host "🚀 Starting FinHub Zen - Integrated Financial Platform" -ForegroundColor Green
Write-Host ""

# Start Backend
Write-Host "📊 Starting Backend Services..." -ForegroundColor Yellow
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\Ruhani\OneDrive - UPES\Documents\Unstop'; python main_backend.py"

Start-Sleep -Seconds 3

# Start Frontend  
Write-Host "🎨 Starting Frontend..." -ForegroundColor Yellow
Start-Process PowerShell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\Ruhani\OneDrive - UPES\Documents\Unstop\finhub-zen'; npm run dev"

Start-Sleep -Seconds 5

# Open browser
Write-Host "🌐 Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:8081"

Write-Host ""
Write-Host "✅ FinHub Zen is starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Frontend: http://localhost:8081" -ForegroundColor Cyan
Write-Host "📍 Backend:  http://localhost:5000" -ForegroundColor Cyan
Write-Host "📍 Health:   http://localhost:5000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 Features Available:" -ForegroundColor White
Write-Host "  • Dashboard - Integrated overview" -ForegroundColor Gray
Write-Host "  • AI Tax Helper - Smart tax management" -ForegroundColor Gray  
Write-Host "  • Financial Insights - Spending analytics" -ForegroundColor Gray
Write-Host "  • Zero-Click Budgeting - Auto budget tracking" -ForegroundColor Gray
Write-Host "  • Search - Cross-platform search" -ForegroundColor Gray
Write-Host "  • Security - Account protection" -ForegroundColor Gray
Write-Host "  • Settings - App customization" -ForegroundColor Gray
Write-Host ""
Write-Host "✨ All features working with demo data!" -ForegroundColor Green