--===================--
-- Daily Transaction --
--===================--
use DWH
go

create procedure DailyTransaction(
@Start_Date date,
@End_Date date
) as
begin
select 
	cast(TransactionDate as DATE) as Date,
	count(TransactionID) as totalTransactions,
	sum(Amount) as TotalAmount
from FactTransaction
WHERE TransactionDate >= @Start_Date 
	AND TransactionDate < DATEADD(DAY, 1, @End_Date)
GROUP BY CAST(TransactionDate AS DATE)
end;
EXEC DailyTransaction @Start_Date='2024-01-18', @End_Date='2024-01-20';

--===================--
-- Balance per Customer --
--===================--

use DWH
go

create procedure BalancePerCustomer(
@name varchar(50)
) as
begin
select
	dc.CustomerName as CustomerName,
	da.AccountType as AccountType,
	da.Balance as Balance,
	da.Balance + isnull(sum(
	case when ft.TransactionType='Deposit' then ft.Amount
	else - ft.Amount end),0) as CurrentBalance
from FactTransaction ft
join DimAccount da on da.AccountID=ft.AccountID
join DimCustomer dc on dc.CustomerID=da.CustomerID
where da.Status = 'active' and dc.CustomerName like '%'+@name+'%'
group by dc.CustomerName, da.AccountType, da.Balance
end;
EXEC BalancePerCustomer @name='shelly';
