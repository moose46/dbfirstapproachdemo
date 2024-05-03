-- ================================================
-- Template generated from Template Explorer using:
-- Create Procedure (New Menu).SQL
--
-- Use the Specify Values for Template Parameters 
-- command (Ctrl-Shift-M) to fill in the parameter 
-- values below.
--
-- This block of comments will not be included in
-- the definition of the procedure.
-- ================================================
USE [Northwind]
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
-- =============================================
CREATE PROCEDURE USP_GetAllOrders
AS
BEGIN
		  SELECT a.OrderID,a.OrderDate,b.CompanyName,
		  c.ProductName,d.UnitPrice,d.Quantity,
		  d.unitprice * d.Quantity as 'BillAmount'
		  from orders a inner join [order details] d on a.orderid=d.orderid inner join
		  customers b on a.customerid=b.customerid inner join
		  products c on d.productid=c.productid
		  where a.orderid between 10248 and 10255
END
GO
