#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "⚡ AutoPulse OS: CoCo CLI Hackathon Deployment Pipeline"
echo "=========================================================="

# 1. Run DDL & Stored Procedure Setup
echo "Step 1/3: Provisioning database objects & stored procedures..."
snow sql -f scripts/01_setup_database.sql
snow sql -f scripts/02_pipelines_and_tasks.sql

# 2. Seed Mock Fleet & Telemetry Records
echo "Step 2/3: Seeding 14-day telemetry and fleet records..."
python scripts/03_seed_data.py

# 3. Deploy Streamlit Application
echo "Step 3/3: Deploying Streamlit in Snowflake (AUTOPULSE_OS)..."
snow streamlit deploy --replace

echo "=========================================================="
echo "✔ Deployment Complete! AutoPulse OS is live on Snowflake."
echo "=========================================================="