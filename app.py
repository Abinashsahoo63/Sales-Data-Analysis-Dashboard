
import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

st.set_page_config(
    page_title="Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Data Analysis Dashboard")
st.caption("Analyze revenue, orders, products, and regions")

# ---------------- DATA SOURCE ----------------
st.sidebar.header("Data Source")

source = st.sidebar.radio(
    "Choose data source",
    ["CSV File", "MySQL Database"]
)

@st.cache_data
def load_csv():
    return pd.read_csv("data/sales_data.csv")

def load_mysql():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="",  # Enter your MySQL password if required
        database="sales_analysis"
    )

    try:
        df = pd.read_sql("SELECT * FROM sales", conn)
    finally:
        conn.close()

    return df

try:
    if source == "CSV File":
        df = load_csv()
    else:
        with st.spinner("Connecting to MySQL..."):
            df = load_mysql()
        st.success("Connected to MySQL successfully!")

except Exception as e:
    st.error(f"Could not load data: {e}")
    st.info(
        "Check that MySQL is running, the database and table exist, "
        "and your connection settings are correct."
    )
    st.stop()

# ---------------- CLEAN DATA ----------------
df.columns = df.columns.str.strip().str.lower()

required = [
    "order_date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "discount_percent"
]

missing = [c for c in required if c not in df.columns]

if missing:
    st.error(f"Missing columns: {', '.join(missing)}")
    st.write("Columns found:", df.columns.tolist())
    st.stop()

# Remove an accidentally imported CSV header row
df = df[
    df["category"].astype(str).str.lower() != "category"
].copy()

df["order_date"] = pd.to_datetime(
    df["order_date"], errors="coerce"
)

for col in ["quantity", "unit_price", "discount_percent"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(
    subset=["order_date", "quantity", "unit_price"]
).copy()

df["discount_percent"] = df["discount_percent"].fillna(0)

# Calculate revenue after discount
df["revenue"] = (
    df["quantity"]
    * df["unit_price"]
    * (1 - df["discount_percent"] / 100)
)

if df.empty:
    st.warning("No valid sales records found.")
    st.stop()

# ---------------- FILTERS ----------------
st.sidebar.header("Filters")

categories = sorted(
    df["category"].dropna().astype(str).unique()
)
regions = sorted(
    df["region"].dropna().astype(str).unique()
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories
)

selected_regions = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=regions
)

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered = df[
    df["category"].astype(str).isin(selected_categories)
    & df["region"].astype(str).isin(selected_regions)
].copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        filtered["order_date"].dt.date.between(
            start_date, end_date
        )
    ]

if filtered.empty:
    st.warning("No sales data matches your filters.")
    st.stop()

# ---------------- KEY METRICS ----------------
total_revenue = filtered["revenue"].sum()
total_orders = filtered["order_id"].nunique()
total_units = filtered["quantity"].sum()

average_order_value = (
    total_revenue / total_orders if total_orders else 0
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
c2.metric("Total Orders", f"{total_orders:,}")
c3.metric("Units Sold", f"{total_units:,.0f}")
c4.metric("Average Order Value", f"₹{average_order_value:,.2f}")

st.divider()

# ---------------- MONTHLY REVENUE ----------------
st.subheader("Monthly Revenue")

monthly = filtered.copy()
monthly["month"] = (
    monthly["order_date"].dt.to_period("M").astype(str)
)

monthly = monthly.groupby(
    "month", as_index=False
)["revenue"].sum()

fig1 = px.line(
    monthly,
    x="month",
    y="revenue",
    markers=True,
    title="Revenue Trend"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- CATEGORY AND REGION ----------------
left, right = st.columns(2)

with left:
    st.subheader("Revenue by Category")

    category_sales = (
        filtered.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    fig2 = px.bar(
        category_sales,
        x="category",
        y="revenue",
        color="category",
        title="Category Performance"
    )

    st.plotly_chart(fig2, use_container_width=True)

with right:
    st.subheader("Revenue by Region")

    region_sales = filtered.groupby(
        "region", as_index=False
    )["revenue"].sum()

    fig3 = px.pie(
        region_sales,
        names="region",
        values="revenue",
        title="Regional Sales Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

# ---------------- TOP PRODUCTS ----------------
st.subheader("Top 5 Products")

top_products = (
    filtered.groupby("product", as_index=False)["revenue"]
    .sum()
    .nlargest(5, "revenue")
)

fig4 = px.bar(
    top_products,
    x="product",
    y="revenue",
    title="Top Products by Revenue"
)

st.plotly_chart(fig4, use_container_width=True,key="monthly_revenue")

# ---------------- SALES DETAILS ----------------
st.subheader("Sales Details")
st.dataframe(filtered, use_container_width=True)

# ---------------- DOWNLOAD ----------------
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered Sales CSV",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)