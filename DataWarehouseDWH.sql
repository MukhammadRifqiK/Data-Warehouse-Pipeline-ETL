create database DWH;
go

use DWH;
go

-- DIMENSION TABLE --
create table DimCustomer(
CustomerID int primary key,
CustomerName varchar(100),
Address varchar(100),
CityName varchar(100),
StateName varchar(100),
Age int,
Gender varchar(10),
Email varchar(100)
);
go

create table DimAccount(
AccountID int primary key,
CustomerID int,
AccountType varchar(50),
Balance decimal(18,2),
DateOpened datetime2,
Status varchar(50),

constraint FK_DimAccount_DimCustomer
foreign key(CustomerID)
references DimCustomer(CustomerID)
);
go

create table DimBranch(
BranchID int primary key,
Branchname varchar(100),
BranchLocation varchar(100)
);
go

-- FACT TABLE --
create table FactTransaction(
TransactionID int primary key,
AccountID int,
TransactionDate datetime2,
Amount decimal(18,2),
TransactionType varchar(50),
BranchID int

constraint FK_FactTransaction_DimAccount
foreign key (AccountID)
references DimAccount(AccountID),

constraint FK_FactTransaction_DimBranch
foreign key (BranchID)
references DimBranch(BranchID)
);
go