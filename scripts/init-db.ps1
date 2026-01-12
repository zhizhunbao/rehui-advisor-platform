# Database initialization script for North America Advisor System (PowerShell)

Write-Host "🚀 Initializing database for North America Advisor System..." -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-not (Test-Path .env)) {
    Write-Host "⚠️  .env file not found. Creating from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ Created .env file. Please update DATABASE_URL and other settings." -ForegroundColor Green
    Write-Host ""
}

# Check if PostgreSQL is installed
$pgPath = Get-Command psql -ErrorAction SilentlyContinue
if (-not $pgPath) {
    Write-Host "❌ PostgreSQL is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install PostgreSQL and try again."
    exit 1
}

Write-Host "✅ PostgreSQL found" -ForegroundColor Green
Write-Host ""

# Load environment variables from .env
if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            Set-Item -Path "env:$name" -Value $value
        }
    }
}

# Extract database settings
$DB_NAME = if ($env:DATABASE_NAME) { $env:DATABASE_NAME } else { "north_america_advisor" }
$DB_USER = if ($env:DATABASE_USER) { $env:DATABASE_USER } else { "postgres" }

Write-Host "📦 Database name: $DB_NAME" -ForegroundColor Cyan
Write-Host "👤 Database user: $DB_USER" -ForegroundColor Cyan
Write-Host ""

# Check if database exists
$dbExists = & psql -U $DB_USER -lqt | Select-String -Pattern "\b$DB_NAME\b"

if ($dbExists) {
    Write-Host "ℹ️  Database '$DB_NAME' already exists" -ForegroundColor Yellow
} else {
    Write-Host "🔨 Creating database '$DB_NAME'..." -ForegroundColor Cyan
    & createdb -U $DB_USER $DB_NAME
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Database created successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to create database" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🔄 Generating Prisma Client..." -ForegroundColor Cyan
npm run db:generate

Write-Host ""
Write-Host "🔄 Running database migrations..." -ForegroundColor Cyan
npm run db:migrate

Write-Host ""
Write-Host "🎉 Database initialization complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review your .env file and update any necessary settings"
Write-Host "  2. Run 'npm run db:seed' to populate with sample data (optional)"
Write-Host "  3. Run 'npm run dev' to start the development server"
Write-Host "  4. Run 'npm run db:studio' to explore the database with Prisma Studio"
