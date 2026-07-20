# 🚀 Enterprise Gadget Store Data Warehouse & Analytics

> **An End-to-End Data Engineering & Business Intelligence Project** that demonstrates how raw enterprise retail data is transformed into analytics-ready datasets using **Python, MySQL, SQL, Docker, GitHub Actions, and Power BI** following the **Medallion Architecture (Bronze → Silver → Gold)**.

---

## 📖 Project Overview

The **Enterprise Gadget Store Data Warehouse & Analytics** project is a real-world Data Engineering solution designed to process and analyze enterprise-scale retail data. The project follows modern Data Engineering practices to transform raw transactional data into business-ready datasets that support reporting and decision-making.

The solution implements a complete ETL pipeline, builds a Star Schema data warehouse, creates business-focused data marts, and delivers interactive dashboards through Power BI.

This project demonstrates industry-standard concepts such as:

- End-to-End ETL Pipeline
- Medallion Architecture (Bronze → Silver → Gold)
- Star Schema Data Warehouse
- Slowly Changing Dimensions (SCD Type 1 & Type 2)
- Incremental Data Loading
- Data Validation & Data Quality
- Business Analytics using Power BI

---

# 🎯 Project Objectives

The primary objectives of this project are:

- Build a scalable Enterprise Data Warehouse.
- Design an automated ETL pipeline using Python.
- Implement the Medallion Architecture.
- Clean, validate, and transform raw data into analytics-ready datasets.
- Design a Star Schema with Fact and Dimension tables.
- Implement Slowly Changing Dimensions (SCD Type 1 & Type 2).
- Support Incremental Data Loading.
- Build Analytics Data Marts for business reporting.
- Create interactive Power BI dashboards.
- Generate meaningful business insights for decision-making.

---

# 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python 3.13 |
| Database | MySQL 8 |
| Data Processing | Pandas |
| Dataset Generation | Faker |
| Database Connectivity | SQLAlchemy, PyMySQL |
| Data Warehouse | Star Schema |
| Architecture | Medallion Architecture |
| Business Intelligence | Power BI |
| Containerization | Docker |
| Version Control | Git & GitHub |
| IDE | Visual Studio Code |

---

# 🌟 Key Highlights

- 📦 **6M+ Enterprise Retail Records**
- 🏗️ **Medallion Architecture (Bronze → Silver → Gold)**
- 📊 **Star Schema Data Warehouse**
- 🔄 **Automated ETL Pipelines**
- 📈 **Analytics Data Marts**
- 📉 **Interactive Power BI Dashboard**
- 🔁 **Incremental Data Loading**
- 🧹 **Data Cleaning & Validation**
- 🕒 **Slowly Changing Dimensions (Type 1 & Type 2)**
- 🐳 **Dockerized Project**
- 📚 **Well-Structured Documentation**
- 🚀 **GitHub Portfolio Ready**

---




# 🏗️ Project Architecture

The project follows the **Medallion Architecture**, where data flows through multiple layers to ensure high-quality, analytics-ready datasets.

```text
                   Raw Data (CSV Files)
                           │
                           ▼
                 🥉 Bronze Layer
              (Raw Data Ingestion)
                           │
                           ▼
                 🥈 Silver Layer
        (Cleaning, Validation & Transformation)
                           │
                           ▼
                  🥇 Gold Layer
          (Business-Ready Data Warehouse)
                           │
                           ▼
             ⭐ Star Schema (Fact & Dimension)
                           │
                           ▼
                 📊 Analytics Data Marts
                           │
                           ▼
             📈 Power BI Executive Dashboard
```

### 📌 Architecture Flow

1. Generate enterprise retail data using Python Faker.
2. Store raw datasets as CSV files.
3. Load raw data into the Bronze Layer.
4. Clean, validate, and standardize data in the Silver Layer.
5. Build Fact and Dimension tables in the Gold Layer.
6. Create Analytics Data Marts.
7. Visualize business insights using Power BI dashboards.

---

# 📂 Project Folder Structure

```text
Enterprise-Gadget-Store/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── config/
│   ├── config.yaml
│   └── database.yaml
│
├── dashboards/
│   └── Enterprise_Gadget_Store_Executive_Dashboard.pbix
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   └── project_flow.md
│
├── logs/
│
├── scripts/
│   ├── generators/
│   ├── ingestion/
│   ├── transformations/
│   ├── warehouse/
│   ├── marts/
│   ├── incremental/
│   ├── metadata/
│   ├── scd/
│   └── orchestration/
│
├── sql/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   ├── marts/
│   ├── incremental/
│   └── scd/
│
├── tests/
├── utils/
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── LICENSE
```

---

# 📁 Folder Description

| Folder | Description |
|---------|-------------|
| `config/` | Database and application configuration |
| `data/` | Raw and processed datasets |
| `scripts/` | Python ETL pipeline scripts |
| `sql/` | SQL scripts for warehouse and marts |
| `dashboards/` | Power BI dashboard |
| `docs/` | Project documentation |
| `tests/` | Data quality and pipeline testing |
| `utils/` | Helper functions and database connection |
| `logs/` | ETL execution logs |

---

# 📊 Dataset Information

The project uses a **synthetic enterprise retail dataset** generated using **Python Faker** to simulate real-world business operations.

### Dataset Includes

- 👥 Customers
- 📦 Products
- 🏷️ Categories
- 🚚 Suppliers
- 🛒 Orders
- 💳 Payments
- 📦 Inventory
- 🚛 Shipments
- 🎁 Coupons

### Dataset Statistics

| Metric | Value |
|---------|-------|
| Total Records | 6M+ |
| Database | MySQL |
| Dataset Type | Synthetic Enterprise Retail Data |
| Format | CSV |

> **Note:** The dataset is provided separately due to its large size and is not stored directly in the GitHub repository.

---

# 🔄 ETL Pipeline

The project follows a complete **Extract → Transform → Load (ETL)** process.

## 📥 Step 1 - Extract

- Generate enterprise retail datasets using Python Faker.
- Export datasets as CSV files.
- Store the datasets in the `data/raw/` directory.

---

## 🥉 Step 2 - Bronze Layer

The Bronze Layer stores raw data exactly as received.

### Purpose

- Preserve original source data.
- Maintain historical records.
- Perform no transformations.

---

## 🥈 Step 3 - Silver Layer

The Silver Layer cleans and standardizes the data.

### Operations Performed

- Remove duplicate records
- Handle null values
- Standardize formats
- Validate records
- Improve data quality

---

## 🥇 Step 4 - Gold Layer

The Gold Layer creates business-ready datasets.

### Includes

- Dimension Tables
- Fact Tables
- Surrogate Keys
- Business Metrics
- Star Schema

---

## 📊 Step 5 - Analytics Data Marts

Business-focused marts are created for reporting and analytics.

- Sales Mart
- Customer Mart
- Inventory Mart
- Payment Mart
- Supplier Mart

---

## 📈 Step 6 - Power BI

Power BI connects directly to the Analytics Data Marts to create interactive dashboards, KPI cards, charts, and business reports for decision-making.


---

# ⭐ Data Warehouse Design (Star Schema)

The Enterprise Gadget Store Data Warehouse follows a **Star Schema** design to optimize analytical queries and improve reporting performance.

## 📌 Fact Tables

| Fact Table | Description |
|------------|-------------|
| `fact_orders` | Stores order transaction details |
| `fact_payments` | Stores payment transactions |
| `fact_inventory` | Stores inventory movement and stock details |
| `fact_shipments` | Stores shipment and delivery information |

---

## 📌 Dimension Tables

| Dimension Table | Description |
|-----------------|-------------|
| `dim_customer` | Customer information |
| `dim_product` | Product details |
| `dim_supplier` | Supplier information |
| `dim_category` | Product categories |
| `dim_coupon` | Coupon details |
| `dim_date` | Date dimension for time-based analysis |

---

## 📌 Analytics Data Marts

Business-ready Data Marts created for reporting:

| Data Mart | Purpose |
|-----------|----------|
| `sales_mart` | Sales performance analysis |
| `customer_mart` | Customer insights |
| `inventory_mart` | Inventory tracking |
| `payment_mart` | Payment analysis |
| `supplier_mart` | Supplier performance |

---

## ✅ Benefits of Star Schema

- Faster analytical queries
- Better Power BI performance
- Simplified reporting
- Optimized joins
- Scalable data warehouse design

---

# 📊 Power BI Dashboard

An interactive Executive Dashboard was developed using **Power BI** to provide business insights.

### Dashboard Includes

- 📈 Executive Dashboard
- 💰 Sales Analysis
- 👥 Customer Analysis
- 📦 Inventory Analysis
- 💳 Payment Analysis
- 🚚 Shipment Analysis
- 🏷️ Product & Category Analysis

---

## 📈 Dashboard KPIs

The dashboard includes the following Key Performance Indicators (KPIs):

- 💰 Total Revenue
- 🛒 Total Orders
- 👥 Total Customers
- 📦 Total Products
- 📈 Average Order Value
- 🚚 Shipment Status
- 📊 Monthly Sales Trend
- 🏆 Top Selling Products
- 🏷️ Top Categories
- 💳 Payment Method Distribution
- 📦 Inventory Availability
- 🌍 Sales by Region

---

# 📷 Dashboard Preview

> **Replace the images below with your actual dashboard screenshots.**

## Executive Dashboard

```text
images/executive_dashboard.png
```

## Sales Dashboard

```text
images/sales_dashboard.png
```

## Customer Dashboard

```text
images/customer_dashboard.png
```

---

# ✨ Project Features

## Data Engineering

- End-to-End ETL Pipeline
- Medallion Architecture
- Enterprise Data Warehouse
- Automated Data Processing
- Data Validation
- Incremental Loading
- Logging & Monitoring

---

## Data Warehouse

- Star Schema
- Fact & Dimension Tables
- Analytics Data Marts
- Business-Ready Data Model
- Optimized SQL Queries

---

## Python Development

- Modular ETL Scripts
- Configuration Management
- Logging
- Error Handling
- Reusable Code Structure

---

## Business Intelligence

- Interactive Power BI Dashboard
- KPI Cards
- Charts & Visualizations
- Drill-down Analysis
- Business Insights

---

# 📈 Business Insights

This project enables organizations to answer business questions such as:

- Which products generate the highest revenue?
- Who are the top customers?
- Which payment methods are most frequently used?
- What are the monthly sales trends?
- Which suppliers contribute the most inventory?
- Which categories perform the best?
- How does shipment performance impact customer satisfaction?
- What is the inventory status across products?

---

# 📌 Project Workflow

```text
Generate Dataset
        │
        ▼
Raw CSV Files
        │
        ▼
Bronze Layer
        │
        ▼
Silver Layer
        │
        ▼
Gold Layer
        │
        ▼
Fact & Dimension Tables
        │
        ▼
Analytics Data Marts
        │
        ▼
Power BI Dashboard
        │
        ▼
Business Insights
```
---

# ⚙️ Installation Guide

## Prerequisites

Before running this project, ensure the following software is installed:

- Python 3.13 or later
- MySQL 8.0+
- Power BI Desktop
- Git
- Docker Desktop (Optional)
- Visual Studio Code

---

## 📥 Clone the Repository

```bash
git clone https://github.com/rameshwrmaharnor/Enterprise-Gadget-Store-Data-Warehouse.git

cd Enterprise-Gadget-Store-Data-Warehouse
```

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configure Database

Update the database configuration file:

```
config/config.yaml
```

Provide the following details:

- MySQL Host
- Port
- Username
- Password
- Database Name

---

## 📂 Download Dataset

The dataset is available separately due to its large size.

### Steps

1. Download the dataset ZIP file.
2. Extract the ZIP file.
3. Copy all CSV files into:

```
data/raw/
```

4. Start the ETL pipeline.

---

# 🚀 Project Execution

Run the project step by step.

### Generate Dataset

```bash
python -m scripts.generators.generate_customers
python -m scripts.generators.generate_products
python -m scripts.generators.generate_orders
```

### Load Bronze Layer

```bash
python -m scripts.ingestion.load_bronze
```

### Transform Silver Layer

```bash
python -m scripts.transformations.transform_customers
python -m scripts.transformations.transform_orders
```

### Load Gold Layer

```bash
python -m scripts.warehouse.run_gold_pipeline
```

### Create Analytics Data Marts

```bash
python -m scripts.marts.run_marts_pipeline
```

---

# 🐳 Docker Support

Build the Docker image:

```bash
docker build -t enterprise-gadget-store .
```

Run the project using Docker Compose:

```bash
docker compose up
```

Stop the containers:

```bash
docker compose down
```

---

# 🧪 Testing

Run the project test suite:

```bash
python -m pytest tests/
```

---

# 📊 Project Statistics

| Component | Status |
|-----------|--------|
| Dataset Generation | ✅ Completed |
| Bronze Layer | ✅ Completed |
| Silver Layer | ✅ Completed |
| Gold Layer | ✅ Completed |
| Fact Tables | ✅ Completed |
| Dimension Tables | ✅ Completed |
| Data Marts | ✅ Completed |
| Power BI Dashboard | ✅ Completed |
| Docker Support | ✅ Completed |
| GitHub Repository | ✅ Completed |

---

# 🔮 Future Enhancements

The following improvements can be added in future versions:

- Apache Airflow for workflow orchestration
- Apache Spark for distributed data processing
- Kafka for real-time data streaming
- Snowflake Data Warehouse
- Azure Data Factory Integration
- AWS Cloud Deployment
- CI/CD Pipeline Enhancement
- Real-time Dashboard Updates
- Machine Learning based Sales Forecasting
- Automated Data Quality Monitoring

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

# 👨‍💻 Author

**Rameshwr Maharnor**

🎓 BE Student | Data Analytics & Data Engineering Enthusiast

### Skills

- Python
- SQL
- MySQL
- Power BI
- Data Engineering
- ETL Pipelines
- Data Warehousing

### GitHub

https://github.com/rameshwrmaharnor

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.

---

# 🙏 Acknowledgements

Special thanks to:

- Open Source Community
- Python Community
- MySQL
- Power BI
- Docker
- GitHub

---

⭐ **If you found this project useful, consider giving it a Star on GitHub!**
