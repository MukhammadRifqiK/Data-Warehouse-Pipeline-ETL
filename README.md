# Data Warehouse dan Pipeline ETL Perbankan
_______________________________________________________________________
📌 Pendahuluan
-----------------------------------------------------------------------
Project ini merancang, membangun, dan mengoptimasi sebuah Data Warehouse pada studi kasus industri perbankan. Permasalahan klien kesulitan mengolah beberapa sumber data yang berbeda secara bersamaan, sumber datanya ada database SQL Server, CSV, dan Excel. Kondisi ini menyebabkan proses pelaporan dan analisis transaksi menjadi terlambat karena data belum terintegrasi dan terpusat. Oleh sebab itu, tujuan studi kasus ini membangun dan merancang sistem Data Warehouse hingga proses pipeline ETL serta melakukan penyederhanaan pemeliharaan sistem database dengan implementasi stored procedure. Disisi lain, stored procedure juga membantu _stakeholder_ mudah memperoleh informasi untuk pelaporan.
_______________________________________________________________________
🎯 Permasalahan bisnis
-----------------------------------------------------------------------
Klien memiliki data transaksi dan data master yang tersebar di beberapa sumber data, yaitu:

File Excel
File CSV
Database SQL Server
Data yang tersebar ini menyebabkan proses reporting menjadi terlambat karena data harus dikumpulkan dan diolah dari berbagai sumber secara manual. Selain itu, terdapat kemungkinan data transaksi duplikat dapat menyebabkan hasil analisis menjadi tidak akurat.

Oleh karena itu, dibutuhkan sebuah solusi membangun sistem Data Warehouse dan pipeline ETL. Alasannya sebagai berikut:

Mengintegrasi data dari beragam sumber
Otomatisasi dalam membersihkan, hapus duplikat, melakukan standarisasi format data supaya terstruktur
Data tervalidasi sebelum disimpan ke Data Warehouse
Sistem yang telah dibangun hasilnya Pelaporan tepat waktu dan mudah diakses
________________________________________________________________________
🎯 Objektivitas
------------------------------------------------------------------------


