SECTION 1: Project Title
# 🚀 Enterprise Gadget Store Data Warehouse
SECTION 2: Project Overview
## 📌 Project Overview

The Enterprise Gadget Store Data Warehouse & Analytics project is an end-to-end Data Engineering and Business Intelligence solution developed to analyze sales, customers, products, inventory, suppliers, shipments, and payment data.

The project follows the Medallion Architecture (Bronze → Silver → Gold) to transform raw transactional data into analytics-ready datasets. A Star Schema data warehouse is built in MySQL, and interactive dashboards are developed in Power BI to support business decision-making.

The solution demonstrates real-world Data Engineering concepts such as ETL pipelines, data validation, Slowly Changing Dimensions (SCD), incremental loading, data marts, and business intelligence reporting.
## 🎯 Project Objectives

The main objectives of this project are:

- Build a scalable Enterprise Data Warehouse.
- Implement the Medallion Architecture (Bronze, Silver, and Gold layers).
- Design and automate ETL pipelines using Python.
- Clean, validate, and transform raw data into analytics-ready data.
- Create Fact and Dimension tables using a Star Schema.
- Implement Slowly Changing Dimensions (SCD Type 1 & Type 2).
- Support Incremental Data Loading.
- Create Analytics Data Marts for business reporting.
- Develop an interactive Executive Dashboard using Power BI.
- Generate meaningful business insights for decision-making.

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | ETL Development and Data Processing |
| Pandas | Data Cleaning and Transformation |
| Faker | Synthetic Dataset Generation |
| SQL | Database Queries |
| MySQL | Enterprise Data Warehouse |
| SQLAlchemy | Python Database Connectivity |
| PyMySQL | MySQL Connection Driver |
| Power BI | Dashboard Development and Reporting |
| Git | Version Control |
| GitHub | Project Repository |
| VS Code | Development Environment |



## 🏗️ Project Architecture

The project follows the Medallion Architecture.

```text
                Raw Data (CSV)
                      │
                      ▼
               Bronze Layer
         (Raw Data Ingestion)
                      │
                      ▼
               Silver Layer
    (Cleaning & Transformation)
                      │
                      ▼
                Gold Layer
     (Business Ready Data Model)
                      │
                      ▼
        Fact & Dimension Tables
             (Star Schema)
                      │
                      ▼
            Analytics Data Marts
                      │
                      ▼
         Power BI Executive Dashboard
```

### Architecture Flow

1. Raw data is generated and stored as CSV files.
2. Data is loaded into the Bronze layer without modification.
3. The Silver layer cleans, validates, and transforms the data.
4. The Gold layer creates business-ready datasets.
5. Fact and Dimension tables are created using a Star Schema.
6. Analytics Data Marts are built for reporting.
7. Power BI connects to the Data Marts to create interactive dashboards.

## 📂 Project Folder Structure

```
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
│   └── Enterprise_Gadget_Store_Analytics.pbix
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
├── notebooks/
│
├── scripts/
│   ├── generators/
│   ├── ingestion/
│   ├── transformations/
│   ├── warehouse/
│   ├── marts/
│   ├── orchestration/
│   ├── validation/
│   ├── incremental/
│   ├── metadata/
│   └── scd/
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
│
├── utils/
│
├── README.md
├── requirements.txt
├── docker-compose.yml
├── setup_project.py
├── .env
├── .gitignore
└── LICENSE
```

### Folder Description

| Folder | Description |
|----------|-------------|
| data | Stores raw and processed datasets |
| scripts | Python ETL scripts |
| sql | SQL scripts for warehouse and marts |
| dashboards | Power BI dashboard |
| docs | Project documentation |
| tests | Data quality and pipeline tests |
| utils | Database connection and helper functions |
| config | Configuration files |
| logs | ETL execution logs |

## 📂 Dataset

The complete dataset (~7 Million+ records) is available on Google Drive.

**Download Link:**

https://drive.google.com/file/d/12FZ4sotzHLeKWTvBwk482367F3RKJwPN/view?usp=sharing

### Steps

1. Download the ZIP file.
2. Extract it.
3. Copy all CSV files into:

data/raw/

4. Run the ETL Pipeline.

## ⚙️ ETL Pipeline

The project implements a complete ETL (Extract, Transform, Load) pipeline.

### Step 1 – Extract

- Generated synthetic enterprise data using Python Faker.
- Exported datasets as CSV files.

Datasets include:

- Customers
- Products
- Categories
- Suppliers
- Orders
- Payments
- Shipments
- Inventory
- Coupons

---

### Step 2 – Bronze Layer

Raw CSV files are loaded into MySQL Bronze tables without modification.

Purpose:

- Preserve original data
- Store raw records
- Maintain source history

---

### Step 3 – Silver Layer

Data is cleaned and transformed.

Operations performed:

- Remove duplicates
- Handle null values
- Standardize formats
- Validate records
- Fix inconsistent data

---

### Step 4 – Gold Layer

Business-ready datasets are created.

Includes:

- Dimension Tables
- Fact Tables
- Surrogate Keys
- Star Schema

---

### Step 5 – Analytics Data Marts

Business-specific marts are created.

- Sales Mart
- Customer Mart
- Inventory Mart
- Payment Mart
- Supplier Mart

---

### Step 6 – Power BI

Power BI connects to Analytics Data Marts and creates interactive dashboards.

## ⭐ Database Design (Star Schema)

The Enterprise Data Warehouse follows a Star Schema design.

### Fact Tables

- fact_orders
- fact_payments
- fact_inventory
- fact_shipments

### Dimension Tables

- dim_customer
- dim_product
- dim_supplier
- dim_category
- dim_coupon
- dim_date

### Analytics Data Marts

- sales_mart
- customer_mart
- inventory_mart
- payment_mart
- supplier_mart

### Benefits of Star Schema

- Fast query performance
- Simple reporting
- Easy Power BI integration
- Optimized for analytics

## ✨ Key Features

- End-to-End Data Engineering Project
- Enterprise Data Warehouse
- Medallion Architecture
- Python ETL Pipelines
- Data Validation
- Incremental Data Loading
- Slowly Changing Dimensions (Type 1 & Type 2)
- Star Schema Design
- Analytics Data Marts
- Power BI Executive Dashboard
- Interactive Filters and KPIs
- Business Reporting
- Modular Project Structure
- Git Version Control
