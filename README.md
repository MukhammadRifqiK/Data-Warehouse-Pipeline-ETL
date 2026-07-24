# Data Warehouse dan Pipeline ETL Studi Kasus Perbankan
_______________________________________________________________________
📌 Pendahuluan
-----------------------------------------------------------------------
Project ini merancang, membangun, dan mengoptimasi sebuah Data Warehouse pada studi kasus industri perbankan. Permasalahan klien kesulitan mengolah beberapa sumber data yang berbeda secara bersamaan, sumber datanya ada database SQL Server, CSV, dan Excel. Kondisi ini menyebabkan proses pelaporan dan analisis transaksi menjadi terlambat karena data belum terintegrasi dan terpusat. Oleh sebab itu, tujuan studi kasus ini membangun dan merancang sistem Data Warehouse hingga proses pipeline ETL serta melakukan penyederhanaan pemeliharaan sistem database dengan implementasi stored procedure. Disisi lain, stored procedure juga membantu _stakeholder_ mudah memperoleh informasi untuk pelaporan.
_______________________________________________________________________
🎯 Permasalahan bisnis
-----------------------------------------------------------------------
Klien memiliki data transaksi dan data master yang tersebar di beberapa sumber data, yaitu:

- File Excel
- File CSV
- Database SQL Server

Data yang tersebar ini menyebabkan proses reporting menjadi terlambat karena data harus dikumpulkan dan diolah dari berbagai sumber secara manual. Selain itu, terdapat kemungkinan data transaksi duplikat dapat menyebabkan hasil analisis menjadi tidak akurat.

Oleh karena itu, dibutuhkan sebuah solusi membangun sistem Data Warehouse dan pipeline ETL. Alasannya sebagai berikut:
- Mengintegrasi data dari beragam sumber
- Otomatisasi dalam membersihkan, hapus duplikat, melakukan standarisasi format data supaya terstruktur
- Data tervalidasi sebelum disimpan ke Data Warehouse
- Sistem yang telah dibangun hasilnya Pelaporan tepat waktu dan mudah diakses
________________________________________________________________________
🎯 Tujuan
------------------------------------------------------------------------
- Membangun Data Warehouse transaksi perbankan yang terpusat
- Mengimplementasikan pipeline ETL menggunakan Python
- Mengintegrasikan data dari berbagai sumber data
- Melakukan pembersihan, hapus data duplikat didalam transformasi data
- Melakukan validasi data dan menyimpan di Data Warehouse bernama DWH
- Membuat Stored Procedure untuk kebutuhan pelaporan
________________________________________________________________________
🧾 Data mentah
------------------------------------------------------------------------
Project ini menggunakan beberapa sumber data yang terdiri dari database SQL Server dan file eksternal.

|Source|Type|Description|
| :---: | :---: | :--- |
|transaction_db|SQL Server|Data transaksi dari database|
|transaction_csv|CSV|Data transaksi dari file CSV|
|transaction_excel|xlsx|Data transaksi dari file Excel|
|account|SQL Server|Data rekening customer|
|customer|SQL Server|Data customer|
|branch|SQL Server|Data kantor cabang|
|city|SQL Server|Data kota|
|state|SQL Server|Data provinsi/state|
________________________________________________________________________
🏗️ Data Warehouse Schema
------------------------------------------------------------------------
Data Warehouse menggunakan model Star Schema dengan satu tabel fakta dan beberapa tabel dimensi

**Dimension Tables**

1. DimCustomer

Tabel ini menyimpan informasi customer data city dan state.

Kolom utama:

- CustomerID
- CustomerName
- Address
- CityName
- StateName
- Age
- Gender
- Email

Transformasi utama:

- Join tabel customer, city, dan state
- Mengubah nama kolom menjadi PascalCase
- Mengubah CustomerName, Address, CityName, StateName, dan Gender menjadi huruf kapital
- Mengubah Age menjadi integer

2. DimAccount

Tabel ini menyimpan informasi rekening milik customer

Kolom utama:

- AccountID
- CustomerID
- AccountType
- Balance
- DateOpened
- Status
  
Transformasi utama:

- Mengubah nama kolom menjadi PascalCase
- Mengubah DateOpened menjadi format date
- Mengubah Balance menjadi numeric
- Memastikan CustomerID valid terhadap DimCustomer

3. DimBranch

Tabel ini menyimpan informasi kantor cabang bank

Kolom utama:

- BranchID
- BranchName
- BranchLocation

Transformasi utama:

- Mengubah nama kolom menjadi PascalCase
- Mengubah BranchName dan BranchLocation menjadi huruf kapital

**Fact Table**

FactTransaction

Tabel ini menyimpan seluruh data transaksi dari berbagai sumber

Kolom utama:

- TransactionID
- AccountID
- TransactionDate
- Amount
- TransactionType
- BranchID
 
Transformasi utama:

- Menggabungkan transaksi dari SQL Server, CSV, dan Excel
- Mengubah nama kolom menjadi PascalCase
- Mengubah TransactionDate menjadi format date
- Mengubah Amount menjadi integer
- Mengubah TransactionType menjadi huruf kapital
- Menghapus transaksi duplikat berdasarkan TransactionID
- Memastikan AccountID dan BranchID valid terhadap tabel dimensi
________________________________________________________________________
🔄 Pipeline ETL
------------------------------------------------------------------------
Pipeline ETL pada project ini terdiri dari beberapa tahapan:

1. Extract
Mengambil data dari sumber SQL Server, CSV, dan Excel.

2. Transform
Membersihkan data, mengganti nama kolom mengikuti kaidah PascalCase, melakukan join antar tabel, mengubah tipe data, dan menghapus duplikasi.

3. Validate
Memastikan data sudah sesuai sebelum dimuat ke Data Warehouse, seperti pengecekan primary key, duplicate value, dan foreign key.

4. Load
Setelah dipastikan sesuai kriteria muat data ke tabel Data Warehouse.
________________________________________________________________________
🧾Stored Procedures
------------------------------------------------------------------------
Pada project ini terdapat dua stored procedure untuk membantu pelaporan

1. DailyTransaction

Stored Procedure ini digunakan untuk menampilkan ringkasan transaksi harian berdasarkan rentang tanggal.

Parameter:

- @start_date
- @end_date

Output:

- Date
- TotalTransactions
- TotalAmount

2. BalancePerCustomer

Stored Procedure ini digunakan untuk menghitung saldo akhir customer berdasarkan transaksi dan hanya active account. Perhitungannya seperti ini:

- transactiontype deposit → Menjumlahkan balance
- transactiontype lainnya → Mengurangi balance

Parameter:

- @name

Output:

- CustomerName
- AccountType
- Balance
- CurrentBalance
________________________________________________________________________
📁 Struktur Project
------------------------------------------------------------------------
```
Project Data-Warehouse-Pipeline-ETL
│
├── README.md
|
|── project_ssms_dw
|       └── DataWarehouseDWH.sql
|       └── StoredProcedure.sql
| 
|── project_python
|        └── etl
|             └── etl.py
|
|── transaction_csv.csv
|── transaction_excel.xlsx
```
________________________________________________________________________
👤 Author
------------------------------------------------------------------------
Jika memiliki masukan atau ingin berdiskusi mengenai project ini, silakan hubungi saya melalui:

Linkedin: www.linkedin.com/in/mukhammadrifqikhawari
Gmail: khawaririfqi@gmail.com
