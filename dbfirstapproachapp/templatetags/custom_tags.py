from django import template

from dbfirstapproachapp.models import OrderDetails, Orders

register = template.Library()
@register.inclusion_tag("dbfa/OrdersWithAccordian_CTT.html")
def show_orders(start=10248,end=10255):
    orders = Orders.objects.filter(orderid__range=[start, end]).order_by("orderid")
    order_ids = [order.orderid for order in orders]
    order_details_list = OrderDetails.objects.filter(orderid__in=order_ids).order_by("orderid")
    return ({
        "orders": orders,
        "order_details": order_details_list}
        )
