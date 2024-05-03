CREATE PROCEDURE USP_GetOrdersCount(@Count int OUTPUT) 
AS
BEGIN
	select @Count=count(*) from orders
	select @Count
END;

