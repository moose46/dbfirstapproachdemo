from ast import Or

import pyodbc
from django.shortcuts import render

from dbfirstapproachapp.models import Categories, Employees, OrderDetails, Orders

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
    cursor.close()
    cnxn.close()

    return render(request, "dbfa/ShowOrders.html", {"Orders": orders})


def StoredProcedureDemo(request):
    GrandTotal = 0
    runningTotal = 0
    runningOrderTotal = 0
    subTotal = 0

    cnxn = GetConnection()
    cursor = cnxn.cursor()
    cursor.execute("{call USP_GetAllOrders}")
    orders = cursor.fetchall()

    newOrders = []
    previousOrderId = 0
    for order in orders:
        if previousOrderId == 0:
            runningTotal += order.BillAmount
            previousOrderId = order.OrderID
            runningOrderTotal += order.BillAmount
            GrandTotal += order.BillAmount
            subTotal += order.BillAmount
            newOrders.append(pushData(order, runningTotal, runningOrderTotal))
        elif previousOrderId == order.OrderID:
            runningTotal += order.BillAmount
            runningOrderTotal += order.BillAmount
            GrandTotal += order.BillAmount
            subTotal += order.BillAmount
            newOrders.append(pushData(order, runningTotal, runningOrderTotal))
        else:
            newOrders.append(pushData(0, subTotal, 0))
            subTotal = 0
            previousOrderId = order.OrderID
            runningOrderTotal = 0
            runningTotal += order.BillAmount
            runningOrderTotal += order.BillAmount
            subTotal += order.BillAmount
            GrandTotal += order.BillAmount
            newOrders.append(pushData(order, runningTotal, runningOrderTotal))

    newOrders.append(pushData(0, subTotal, 0))
    cursor.close()
    cnxn.close()
    return render(
        request, "dbfa/ShowOrders.html", {"Orders": newOrders, "GrandTotal": GrandTotal}
    )


def pushData(order, runningTotal, runningOrderTotal):
    if order == 0:
        dataToPush = {
            "OrderID": "",
            "OrderDate": "",
            "CompanyName": "",
            "ProductName": "",
            "UnitPrice": "",
            "Quantity": "",
            "BillAmount": "",
            "RunningTotal": runningTotal,
            "RunningOrderTotal": "",
        }
    else:
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


from django.db.models import Avg, Count, Max, Min, Q, Sum


def FilteringQuerySetsDemo(request):
    # orders = Orders.objects.all()
    # orders = Orders.objects.filter(freight__gt=20)
    # orders = Orders.objects.filter(freight__gte=20)
    # orders = Orders.objects.filter(freight__lt=20)
    # orders = Orders.objects.filter(freight__lte=20)
    # orders = Orders.objects.filter(shipcountry__exact="Germany")
    # orders = Orders.objects.filter(shipcountry__contains="land")
    # orders = Orders.objects.filter(orderid__exact=10248)
    # orders = Orders.objects.filter(employeeid__in=[1, 3, 5])
    # orders = Orders.objects.filter(employeeid__in=[1, 3, 5]).order_by("-employeeid")
    # orders = Orders.objects.filter(employeeid__in=[1, 3, 5]).order_by("-employeeid")
    # orders = Orders.objects.filter(shipname__startswith="A").order_by("-employeeid")
    # orders = Orders.objects.filter(shipname__endswith="e")
    # orders = Orders.objects.filter(freight__range=[10, 20])
    # orders = Orders.objects.filter(shipname__startswith="A") | Orders.objects.filter(
    #     freight__lt=20
    # )
    # orders = Orders.objects.filter(Q(shipname__startswith="S") | Q(freight__lt=20))
    # orders = Orders.objects.filter(Q(shipname__startswith="S") & Q(freight__lt=20))
    # orders = Orders.objects.filter(shipname__startswith="S") & Orders.objects.filter(
    #     freight__gte=15
    # )
    # orders = Orders.objects.filter(Q(shipname__startswith="S") & Q(freight__gte=15))
    # orders = Orders.objects.filter(shipname__startswith="A", freight__gte=15)
    # orders = Orders.objects.exclude(shipname__startswith="S")
    # orders = Orders.objects.filter(~Q(shipname__startswith="S"))
    # orders = Orders.objects.all().order_by("orderid")
    # orders = Orders.objects.all().order_by("-orderid")
    # orders = Orders.objects.all().order_by("shipcountry")
    year = 1997
    orders = Orders.objects.filter(orderdate__year=year).order_by(
        "-orderdate", "employeeid"
    )
    avg = Orders.objects.all().aggregate(Avg("freight"))
    max = Orders.objects.all().aggregate(Max("freight"))
    min = Orders.objects.all().aggregate(Min("freight"))
    sum = Orders.objects.all().aggregate(Sum("freight"))
    count = Orders.objects.all().aggregate(Count("freight"))

    context = {
        "Orders": orders,
        "avg": avg["freight__avg"],
        "max": max["freight__max"],
        "min": min["freight__min"],
        "sum": sum["freight__sum"],
        "count": count["freight__count"],
    }
    # print(type(Orders))
    # print(str(orders.query))
    return render(request, "dbfa/FilteringDemo.html", {"Orders": context})


def TwoLevelAccordianDemo(request):
    orders = Orders.objects.filter(orderid__range=[10248, 10255]).order_by("orderid")
    order_ids = [order.orderid for order in orders]
    order_details_list = OrderDetails.objects.filter(orderid__in=order_ids).order_by(
        "orderid"
    )
    return render(
        request,
        "dbfa/OrdersWithAccordian.html",
        {"orders": orders, "order_details": order_details_list},
    )


def MultilevelAccordianDemo(request):
    employees_list = Employees.objects.all().order_by("employeeid")
    order_ids = (
        Orders.objects.filter(employeeid__in=employees_list)
        .values_list("orderid", flat=True)
        .distinct()
    )

    orders = Orders.objects.filter(
        orderid__in=order_ids, orderid__range=[10248, 10255]
    ).order_by("orderid")
    order_ids = [order.orderid for order in orders]

    order_details_list = OrderDetails.objects.filter(orderid__in=order_ids).order_by(
        "orderid"
    )
    return render(
        request,
        "dbfa/MultilevelAccordianDemo.html",
        {
            "employees": employees_list,
            "orders": orders,
            "order_details": order_details_list,
        },
    )
