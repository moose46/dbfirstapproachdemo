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


def StoredProcedureDemo(request):
    GrandTotal = 0
    runningTotal = 0
    runningOrderTotal = 0

    cnxn = GetConnection()
    cursor = cnxn.cursor()
    cursor.execute("{call USP_GetAllOrders}")
    orders = cursor.fetchall()

    newOrders = []
    previousOrderId = 0
    for order in orders:
        if previousOrderId == 0:
            previousOrderId = order.OrderID
            runningTotal += order.BillAmount
            runningOrderTotal += order.BillAmount
            GrandTotal += order.BillAmount
            newOrders.append(pushData(order, runningTotal, runningOrderTotal))
        elif previousOrderId == order.OrderID:
            runningTotal += order.BillAmount
            runningOrderTotal += order.BillAmount
            GrandTotal += order.BillAmount
            newOrders.append(pushData(order, runningTotal, runningOrderTotal))
        else:
            previousOrderId = order.OrderID
            runningOrderTotal = 0
            runningTotal += order.BillAmount
            runningOrderTotal += order.BillAmount
            GrandTotal += order.BillAmount
            newOrders.append(pushData(order, runningTotal, runningOrderTotal))

    return render(
        request, "dbfa/ShowOrders.html", {"Orders": newOrders, "GrandTotal": GrandTotal}
    )


def pushData(order, runningTotal, runningOrderTotal):
    dataToPush = {
        "OrderID": order.OrderID,
        "OrderDate": order.OrderDate,
        "CompanyName": order.CompanyName,
        "ProductName": order.ProductName,
        "UnitPrice": order.UnitPrice,
        "Quantity": order.Quantity,
        "BillAmount": order.BillAmount,
        "RunningTotal": runningTotal,
        "RunningOrderTotal": runningOrderTotal,
    }
    return dataToPush


def SPWithOutpuParametersDemo(request):
    cnxn = GetConnection()
    cursor = cnxn.cursor()
    count = 0
    cursor.execute("{call USP_GetOrdersCount(?)}", count)
    count = cursor.fetchval()

    cursor.execute("{call USP_GetAllOrders}")
    orders = cursor.fetchall()

    return render(request, "dbfa/ShowOrders.html", {"Orders": orders, "Count": count})


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
