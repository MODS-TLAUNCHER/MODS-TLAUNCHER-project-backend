#!/bin/bash

# =====================================================
# MODS-TLAUNCHER Backend Setup Script
# =====================================================

echo "======================================="
echo " SETTING UP MODS-TLAUNCHER BACKEND"
echo "======================================="

# Stop execution if an error occurs
set -e

# -----------------------------------------------------
# Check Python installation
# -----------------------------------------------------

if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed."
    exit 1
fi

# -----------------------------------------------------
# Create virtual environment
# -----------------------------------------------------

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# -----------------------------------------------------
# Activate virtual environment
# -----------------------------------------------------

source venv/bin/activate

# -----------------------------------------------------
# Upgrade pip
# -----------------------------------------------------

echo "Upgrading pip..."
pip install --upgrade pip

# -----------------------------------------------------
# Install dependencies
# -----------------------------------------------------

if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found."
fi

# -----------------------------------------------------
# Environment variables setup
# -----------------------------------------------------

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    touch .env
fi

# -----------------------------------------------------
# Run basic tests
# -----------------------------------------------------

echo "Running basic tests..."

if [ -d "tests" ]; then
    pytest || echo "Tests failed or are not configured yet."
else
    echo "No tests directory found."
fi

# -----------------------------------------------------
# Start backend server
# -----------------------------------------------------

echo "Starting backend server..."

# Replace main.py with the actual entry point if needed
python main.py

echo "======================================="
echo " BACKEND STARTED SUCCESSFULLY"
echo "======================================="