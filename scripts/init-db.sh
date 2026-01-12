#!/bin/bash

# Database initialization script for North America Advisor System

echo "🚀 Initializing database for North America Advisor System..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please update DATABASE_URL and other settings."
    echo ""
fi

# Check if PostgreSQL is running
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed or not in PATH"
    echo "Please install PostgreSQL and try again."
    exit 1
fi

echo "✅ PostgreSQL found"
echo ""

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Extract database name from DATABASE_URL or use default
DB_NAME=${DATABASE_NAME:-north_america_advisor}
DB_USER=${DATABASE_USER:-postgres}

echo "📦 Database name: $DB_NAME"
echo "👤 Database user: $DB_USER"
echo ""

# Check if database exists
if psql -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "ℹ️  Database '$DB_NAME' already exists"
else
    echo "🔨 Creating database '$DB_NAME'..."
    createdb -U "$DB_USER" "$DB_NAME"
    if [ $? -eq 0 ]; then
        echo "✅ Database created successfully"
    else
        echo "❌ Failed to create database"
        exit 1
    fi
fi

echo ""
echo "🔄 Generating Prisma Client..."
npm run db:generate

echo ""
echo "🔄 Running database migrations..."
npm run db:migrate

echo ""
echo "🎉 Database initialization complete!"
echo ""
echo "Next steps:"
echo "  1. Review your .env file and update any necessary settings"
echo "  2. Run 'npm run db:seed' to populate with sample data (optional)"
echo "  3. Run 'npm run dev' to start the development server"
echo "  4. Run 'npm run db:studio' to explore the database with Prisma Studio"
