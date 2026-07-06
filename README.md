# Data Warehouse dan Pipeline ETL Perbankan
📌 Project Overview

Project ini merupakan Final Task Data Engineer untuk membangun sebuah Data Warehouse pada studi kasus industri perbankan. klien memiliki beberapa sumber data yang berbeda, yaitu SQL Server, CSV, dan Excel. Kondisi ini menyebabkan proses pelaporan dan analisis transaksi menjadi kurang efisien karena data belum terpusat dalam satu sistem.

Untuk menyelesaikan permasalahan tersebut, project ini membangun sebuah database Data Warehouse bernama DWH, membuat tabel dimensi dan tabel fakta, serta mengembangkan pipeline ETL menggunakan Python. Pipeline ini bertugas untuk mengekstrak data dari berbagai sumber, melakukan transformasi data, menghapus data transaksi duplikat, melakukan validasi, dan memuat data akhir ke dalam Data Warehouse.

Selain itu, project ini juga menyediakan Stored Procedure untuk membantu kebutuhan reporting, yaitu ringkasan transaksi harian dan perhitungan saldo customer berdasarkan transaksi.
