# Sales Data Analysis Dashboard

Beginner portfolio project for a DI Engineer / Data Analytics role.

## Goal
Analyze sample sales transactions to understand revenue, order volume, product performance, and monthly trends. SQL query outputs can power charts and KPIs in Apache Superset.

## Tools
- MySQL 8+
- Apache Superset
- CSV sample dataset

## Quick start
1. Create the database by running `sql/01_create_table.sql`.
2. Import `data/sales_data.csv` into the `sales` table using MySQL Workbench's Table Data Import Wizard.
3. Run queries in `sql/02_analysis_queries.sql`.
4. Connect MySQL to Apache Superset and follow `SUPERSET_SETUP.md`.

Revenue formula: `quantity * unit_price * (1 - discount_percent / 100)`

This is synthetic sample data for learning, not real company data.
