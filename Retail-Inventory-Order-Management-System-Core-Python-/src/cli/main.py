# src/cli/main.py
import argparse
import json
from src.services.product_service import product_service
from src.services.customer_service import customer_service
from src.services.order_service import order_service
from src.services.payment_service import payment_service
from src.services.reporting_service import reporting_service
# ---------------- Product Commands ----------------
def cmd_product_add(args):
    try:
        p = product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
        print("Created product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_list(args):
    try:
        ps = product_service.get_all_products(limit=100)
        print(json.dumps(ps, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_update(args):
    try:
        fields = {}
        if args.name: fields["name"] = args.name
        if args.price: fields["price"] = args.price
        if args.stock: fields["stock"] = args.stock
        if args.category: fields["category"] = args.category
        p = product_service.update_product(args.prod_id, fields)
        print("Updated product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_delete(args):
    try:
        p = product_service.delete_product(args.prod_id)
        print("Deleted product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_restock(args):
    try:
        p = product_service.restock_product(args.prod_id, args.delta)
        print("Product restocked:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# ---------------- Customer Commands ----------------
def cmd_customer_add(args):
    try:
        c = customer_service.add_customer(args.name, args.email, args.phone, args.city)
        print("Created customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_list(args):
    try:
        cs = customer_service.list_customers()
        print(json.dumps(cs, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_update(args):
    try:
        updated = customer_service.update_customer(args.email, args.phone, args.city)
        print("Customer updated:")
        print(json.dumps(updated, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_delete(args):
    try:
        deleted = customer_service.delete_customer(args.email)
        print("Customer deleted:")
        print(json.dumps(deleted, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_search(args):
    try:
        results = customer_service.search_customer(args.email, args.city)
        print(json.dumps(results, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# ---------------- Order Commands ----------------
def cmd_order_create(args):
    items = []
    for item in args.item:
        try:
            pid, qty = item.split(":")
            items.append({"prod_id": int(pid), "quantity": int(qty)})
        except Exception:
            print("Invalid item format:", item)
            return
    try:
        ord = order_service.create_order(args.customer, items)
        print("Order created:")
        print(json.dumps(ord, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_show(args):
    try:
        o = order_service.get_order_details(args.order)
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_cancel(args):
    try:
        o = order_service.cancel_order(args.order)
        print("Order cancelled:")
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_complete(args):
    try:
        o = order_service.complete_order(args.order)
        print("Order completed:")
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_list_customer(args):
    try:
        o = order_service.list_orders_by_customer(args.customer)
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
def cmd_payment_process(args):
    try:
        payment = payment_service.pay_order(args.order, args.method)
        print("Payment processed:")
        print(json.dumps(payment, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_payment_refund(args):
    try:
        payment = payment_service.refund_order_payment(args.order)
        print("Payment refunded:")
        print(json.dumps(payment, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
def cmd_report_top_products(args):
    report = reporting_service.top_selling_products(args.top)
    print(json.dumps(report, indent=2))

def cmd_report_revenue_last_month(args):
    revenue = reporting_service.total_revenue_last_month()
    print("Total revenue last month:", revenue)

def cmd_report_orders_by_customer(args):
    report = reporting_service.total_orders_by_customer()
    print(json.dumps(report, indent=2))

def cmd_report_frequent_customers(args):
    report = reporting_service.frequent_customers(args.min_orders)
    print(json.dumps(report, indent=2))
# ---------------- Reporting Commands ----------------
def cmd_report_top_products(args):
    top_n = args.top or 5
    result = reporting_service.top_selling_products(top_n)
    print(json.dumps(result, indent=2, default=str))

def cmd_report_revenue(args):
    revenue = reporting_service.total_revenue_last_month()
    print(f"Total revenue last month: {revenue}")

def cmd_report_orders_by_customer(args):
    result = reporting_service.total_orders_by_customer()
    print(json.dumps(result, indent=2, default=str))

def cmd_report_frequent_customers(args):
    min_orders = args.min or 2
    result = reporting_service.frequent_customers(min_orders)
    print(json.dumps(result, indent=2, default=str))
# ---------------- Build Parser ----------------
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")

    # ---------------- Product parser ----------------
    p_prod = sub.add_parser("product", help="product commands")
    pprod_sub = p_prod.add_subparsers(dest="action")
    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)
    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)
    updatep = pprod_sub.add_parser("update")
    updatep.add_argument("--prod_id", type=int, required=True)
    updatep.add_argument("--name")
    updatep.add_argument("--price", type=float)
    updatep.add_argument("--stock", type=int)
    updatep.add_argument("--category")
    updatep.set_defaults(func=cmd_product_update)
    deletep = pprod_sub.add_parser("delete")
    deletep.add_argument("--prod_id", type=int, required=True)
    deletep.set_defaults(func=cmd_product_delete)
    restockp = pprod_sub.add_parser("restock")
    restockp.add_argument("--prod_id", type=int, required=True)
    restockp.add_argument("--delta", type=int, required=True)
    restockp.set_defaults(func=cmd_product_restock)

    # ---------------- Customer parser ----------------
    pcust = sub.add_parser("customer", help="customer commands")
    pcust_sub = pcust.add_subparsers(dest="action")
    addc = pcust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city", default=None)
    addc.set_defaults(func=cmd_customer_add)
    listc = pcust_sub.add_parser("list")
    listc.set_defaults(func=cmd_customer_list)
    updatec = pcust_sub.add_parser("update")
    updatec.add_argument("--email", required=True)
    updatec.add_argument("--phone")
    updatec.add_argument("--city")
    updatec.set_defaults(func=cmd_customer_update)
    deletec = pcust_sub.add_parser("delete")
    deletec.add_argument("--email", required=True)
    deletec.set_defaults(func=cmd_customer_delete)
    searchc = pcust_sub.add_parser("search")
    searchc.add_argument("--email")
    searchc.add_argument("--city")
    searchc.set_defaults(func=cmd_customer_search)

    # ---------------- Order parser ----------------
    porder = sub.add_parser("order", help="order commands")
    porder_sub = porder.add_subparsers(dest="action")
    createo = porder_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
    createo.set_defaults(func=cmd_order_create)
    showo = porder_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=cmd_order_show)
    cano = porder_sub.add_parser("cancel")
    cano.add_argument("--order", type=int, required=True)
    cano.set_defaults(func=cmd_order_cancel)
    comp = porder_sub.add_parser("complete")
    comp.add_argument("--order", type=int, required=True)
    comp.set_defaults(func=cmd_order_complete)
    listcust = porder_sub.add_parser("list-customer")
    listcust.add_argument("--customer", type=int, required=True)
    listcust.set_defaults(func=cmd_order_list_customer)

    # ---------------- Payment parser ----------------
    ppay = sub.add_parser("payment", help="payment commands")
    ppay_sub = ppay.add_subparsers(dest="action")
    processp = ppay_sub.add_parser("process")
    processp.add_argument("--order", type=int, required=True)
    processp.add_argument("--method", choices=["Cash", "Card", "UPI"], required=True)
    processp.set_defaults(func=cmd_payment_process)
    refundp = ppay_sub.add_parser("refund")
    refundp.add_argument("--order", type=int, required=True)
    refundp.set_defaults(func=cmd_payment_refund)

    # ---------------- Reporting parser (single, no duplicates) ----------------
    prep = sub.add_parser("report", help="reporting commands")
    prep_sub = prep.add_subparsers(dest="action")

    # Top products
    topprod = prep_sub.add_parser("top-products")
    topprod.add_argument("--top", type=int, default=5, help="Number of top products to show")
    topprod.set_defaults(func=cmd_report_top_products)

    # Revenue last month
    revenue = prep_sub.add_parser("revenue")
    revenue.set_defaults(func=cmd_report_revenue)

    # Orders by customer
    orders_by_customer = prep_sub.add_parser("orders-by-customer")
    orders_by_customer.set_defaults(func=cmd_report_orders_by_customer)

    # Frequent customers
    frequent_cust = prep_sub.add_parser("frequent-customers")
    frequent_cust.add_argument("--min", type=int, default=2, help="Minimum number of orders")
    frequent_cust.set_defaults(func=cmd_report_frequent_customers)

    return parser


# ---------------- Main ----------------
def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
