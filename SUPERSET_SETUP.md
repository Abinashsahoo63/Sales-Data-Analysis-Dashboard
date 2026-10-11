# Apache Superset Setup

## Connect MySQL
1. Create the `sales_analysis` database and import the CSV into the `sales` table.
2. In Superset, open the database connections area and add a MySQL connection.
3. A common SQLAlchemy URI format is:
   `mysql+pymysql://USERNAME:PASSWORD@HOST:3306/sales_analysis`
4. Ensure your Superset environment has a compatible MySQL driver. Test and save the connection. Do not share database credentials.

## Add dataset
- Go to Data → Datasets → Add Dataset.
- Select the MySQL connection and `sales` table.
- Save the dataset.

## Charts to create
- KPI / Big Number: total revenue, total orders, units sold.
- Line chart: monthly revenue.
- Bar chart: revenue by category.
- Bar chart: revenue by region.
- Bar chart: top five products by revenue.
- Optional stacked bar chart: monthly revenue by category.

## Dashboard layout
Create a dashboard called **Sales Performance Dashboard** and add the KPI cards and charts above. Add date/region filters if available in your Superset version.

## Interview explanation
“I created a Sales Data Analysis Dashboard using MySQL and Apache Superset. I used SQL aggregation queries to calculate revenue, orders, units sold, monthly trends, and category and region performance. I displayed the results as KPI cards and charts to make sales performance easier to understand. The data is synthetic sample data created for learning.”

## Resume description (use only after building and testing it)
**Sales Data Analysis Dashboard**
- Analyzed sample sales transactions using MySQL to calculate revenue, order volume, monthly trends, and product/category performance.
- Wrote SQL aggregation and grouping queries to prepare metrics for an Apache Superset dashboard.
- Built KPI cards and charts to present trends by month, product category, and region.
