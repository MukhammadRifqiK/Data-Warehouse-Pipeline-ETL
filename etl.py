# ========================================
# ETL PIPELINE 
# ========================================

import pandas as pd
from sqlalchemy import create_engine, text

# ========================================
# CONNECT DATABASE
# ========================================

# Database (Sample)
source_engine = create_engine(
    "mssql+pyodbc://DESKTOP-79KU7JM\\SQLSERVER2022/Sample?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

# Database (DWH)
engine = create_engine(
    "mssql+pyodbc://DESKTOP-79KU7JM\\SQLSERVER2022/DWH?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

print("\n🔄 Sedang menguji koneksi database")

try:
    # Tes koneksi ke database awal
    with source_engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("✅ Berhasil terhubung ke database (sample)")

    # Tes koneksi ke database tujuan
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("✅ Berhasil terhubung ke database (DWH)")

    print("\n✅ KONEKSI AMAN! Database siap digunakan")

except Exception as e:
    print("\n❌ KONEKSI GAGAL")
    print("--------------------------------------------------")
    print(f"Pesan Error: {e}")

# ========================================
# EXTRACT DIMENSION DATA
# ========================================

print("\n🔄 Memulai proses extract dimension table")

try:
    # Extract Customer
    print("  ▪ [1/5] Mengekstrak data 'customer'...", end="")
    customer = pd.read_sql("SELECT * FROM customer", source_engine)
    print(" Selesai")

    # Extract City
    print("  ▪ [2/5] Mengekstrak data 'city'...", end="")
    city = pd.read_sql("SELECT * FROM city", source_engine)
    print(" Selesai")

    # Extract State
    print("  ▪ [3/5] Mengekstrak data 'state'...", end="")
    state = pd.read_sql("SELECT * FROM state", source_engine)
    print(" Selesai")

    # Extract Account
    print("  ▪ [4/5] Mengekstrak data 'account'...", end="")
    account = pd.read_sql("SELECT * FROM account", source_engine)
    print(" Selesai")

    # Extract Branch
    print("  ▪ [5/5] Mengekstrak data 'branch'...", end="")
    branch = pd.read_sql("SELECT * FROM branch", source_engine)
    print(" Selesai")

    print("✅ Extract dimension table berhasil!")

except Exception as e:
    print("\n❌ PROSES EXTRACT DIMENSION TABLE GAGAL!")
    print("--------------------------------------------------")
    print(f"Detail Error: {e}")  

# ========================================
# TRANSFORM DIMCUSTOMER
# ========================================

print("\n🔄 Memulai proses transform dimension table")

try:
    df = customer.merge(city, on="city_id").merge(state, on="state_id")

    df["customer_name"] = df["customer_name"].str.upper()
    df["address"] = df["address"].str.upper()
    df["city_name"] = df["city_name"].str.upper()
    df["state_name"] = df["state_name"].str.upper()
    df["gender"] = df["gender"].str.upper()

    dim_customer = df.rename(columns={
        "customer_id": "CustomerID",
        "customer_name": "CustomerName",
        "address": "Address",
        "city_name": "CityName",
        "state_name": "StateName",
        "age": "Age",
        "gender": "Gender",
        "email": "Email"
    })[
        ["CustomerID", "CustomerName", "Address", "CityName", "StateName", "Age", "Gender", "Email"]
    ]

# ========================================
# TRANSFORM DIMACCOUNT
# ========================================

    dim_account = account.rename(columns={
        "account_id": "AccountID",
        "customer_id": "CustomerID",
        "account_type": "AccountType",
        "balance": "Balance",
        "date_opened": "DateOpened",
        "status": "Status"
    })

# ========================================
# TRANSFORM DIMBRANCH
# ========================================

    dim_branch = branch.rename(columns={
        "branch_id": "BranchID",
        "branch_name": "BranchName",
        "branch_location": "BranchLocation"
    })

    print("✅ Transform dimension table berhasil!")

except Exception as e:
    print("\n❌ PROSES TRANSFORM DIMENSION TABLE GAGAL!")
    print("--------------------------------------------------")
    print(f"Detail Error: {e}")

# ========================================
# LOAD DIMENSIONS
# ========================================

print("\n🔄 Memulai proses load dimension table")

try:
    print("  ▪ [1/4] Mengosongkan data lama di database DWH...", end="")
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM DimAccount")) 
        conn.execute(text("DELETE FROM DimCustomer"))
        conn.execute(text("DELETE FROM DimBranch"))
        conn.commit()
    print(" Selesai")

    # Load DimCustomer
    print("  ▪ [2/4] Memasukkan data baru ke 'DimCustomer'...", end="")
    dim_customer.to_sql("DimCustomer", engine, if_exists="append", index=False)
    print(" Selesai")

    # Load DimAccount
    print("  ▪ [3/4] Memasukkan data baru ke 'DimAccount'...", end="")
    dim_account.to_sql("DimAccount", engine, if_exists="append", index=False)
    print(" Selesai")

    # Load DimBranch
    print("  ▪ [4/4] Memasukkan data baru ke 'DimBranch'...", end="")
    dim_branch.to_sql("DimBranch", engine, if_exists="append", index=False)
    print(" Selesai")

    print("✅ Load dimension table berhasil!")

except Exception as e:
    print("\n❌ PROSES LOAD DIMENSION TABLE GAGAL!")
    print("--------------------------------------------------")
    print(f"Detail Error: {e}")

# ========================================
# EXTRACT FACT DATA
# ========================================

print("\n🔄 Memulai proses extract fact data")

try:
    db_df = pd.read_sql("SELECT * FROM transaction_db", source_engine)
    excel_df = pd.read_excel("transaction_excel.xlsx")
    csv_df = pd.read_csv("transaction_csv.csv")

    print("✅ Extract fact data berhasil!")

except Exception as e:
    print("\n❌ PROSES EKSTRACT FACT DATA GAGAL!")
    print("--------------------------------------------------")
    print(f"Detail Error: {e}")

# ========================================
# TRANSFORM FACT DATA
# ========================================

print("\n🔄 Memulai proses transform fact data")

try:
    csv_df["transaction_date"] = pd.to_datetime(csv_df["transaction_date"], dayfirst=True)
    excel_df["transaction_date"] = pd.to_datetime(excel_df["transaction_date"])

    fact = pd.concat([db_df, excel_df, csv_df])
    fact["transaction_id"] = fact["transaction_id"].astype(int)
    fact = fact.drop_duplicates()

    fact = fact.rename(columns={
    "transaction_id": "TransactionID",
    "account_id": "AccountID",
    "transaction_date": "TransactionDate",
    "amount": "Amount",
    "transaction_type": "TransactionType",
    "branch_id": "BranchID"
    })

    print("✅ Transform fact data berhasil!")

except Exception as e:
    print("\n❌ PROSES TRANSFORM FACT DATA GAGAL!")
    print("--------------------------------------------------")
    print(f"Detail Error: {e}")

# ========================================
# LOAD FACT
# ========================================

print("\n🔄 Memulai proses load fact data")

try:
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM FactTransaction"))
        conn.commit()

    fact.to_sql("FactTransaction", engine, if_exists="append", index=False)

    print("✅ Load fact data berhasil!")

except Exception as e:
    print("\n❌ PROSES LOAD FACT DATA GAGAL!")
    print("--------------------------------------------------")
    print(f"Detail Error: {e}")


print("\n PROSES ETL SELESAI✅")