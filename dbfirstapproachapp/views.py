import pyodbc
from django.shortcuts import render

from dbfirstapproachapp.models import Categories

# Create your views here.


# https://www.udemy.com/course/masteringdjango/learn/lecture/41669202#questions
def ShowCategories(request):
    categories = Categories.objects.all()

    return render(request, "dbfa/ShowCategories.html", {"Categories": categories})


def RawSqlDemo(request):
    query = """
		  SELECT a.OrderID,a.OrderDate,b.CompanyName,
		  c.ProductName,d.UnitPrice,d.Quantity,
		  d.unitprice * d.Quantity as 'BillAmount'
		  from orders a inner join [order details] d on a.orderid=d.orderid inner join
		  customers b on a.customerid=b.customerid inner join
		  products c on d.productid=c.productid
		  where a.orderid between 10248 and 10255
		  """
    cnxn = GetConnection()
    cursor = cnxn.cursor()
    cursor.execute(query)
    orders = cursor.fetchall()
    return render(request, "dbfa/ShowOrders.html", {"Orders": orders})


def GetConnection():
    cnxn = ""
    try:
        cnxn = pyodbc.connect(
            "Driver=ODBC Driver 17 for SQL Server;Server=.;Database=Northwind;Trusted_Connection=Yes;"
        )
        return cnxn
    except Exception as e:
        print(f"GetConnection: {e}")
        return cnxn
