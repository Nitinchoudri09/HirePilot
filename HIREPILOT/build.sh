#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# build.sh — Render production build script for Prep2Hire (Django 5 / Python 3.12)
# ─────────────────────────────────────────────────────────────────────────────
# set -o errexit causes the script to exit immediately if any command fails
set -o errexit

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Running database migrations..."
python manage.py migrate

echo "==> Build complete."
