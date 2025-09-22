from datetime import datetime, timedelta
from src.dao.reporting_dao import reporting_dao

class ReportingService:

    def top_selling_products(self, top_n: int = 5):
        """Return top N selling products by total quantity"""
        all_orders = reporting_dao.fetch_all_orders()  # completed orders only
        product_sales = {}

        for order in all_orders:
            items = reporting_dao.fetch_order_items(order["order_id"])
            for item in items:
                pid = item["prod_id"]
                qty = item.get("quantity", 0)
                product_sales[pid] = product_sales.get(pid, 0) + qty

        if not product_sales:
            return []  # return empty if no sales

        # Sort products by quantity sold
        sorted_sales = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)

        return [{"prod_id": pid, "quantity_sold": qty} for pid, qty in sorted_sales[:top_n]]

    def total_revenue_last_month(self):
        """Calculate total revenue for last month"""
        today = datetime.utcnow()
        start_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        end_last_month = today.replace(day=1) - timedelta(days=1)

        all_orders = reporting_dao.fetch_all_orders()
        revenue = sum(
            o.get("total_amount", 0)
            for o in all_orders
            if start_last_month <= datetime.fromisoformat(o["created_at"]) <= end_last_month
        )
        return revenue

    def total_orders_by_customer(self):
        """Return total orders placed by each customer"""
        customers = reporting_dao.fetch_all_customers()
        result = []
        for c in customers:
            orders = [
                o for o in reporting_dao.fetch_all_orders()
                if o.get("customer_id") == c.get("cust_id")
            ]
            result.append({"customer": c["name"], "total_orders": len(orders)})
        return result

    def frequent_customers(self, min_orders: int = 2):
        """Customers who placed more than min_orders"""
        customers = reporting_dao.fetch_all_customers()
        result = []
        for c in customers:
            orders = [
                o for o in reporting_dao.fetch_all_orders()
                if o.get("customer_id") == c.get("cust_id")
            ]
            if len(orders) > min_orders:
                result.append({"customer": c["name"], "orders": len(orders)})
        return result

# Singleton
reporting_service = ReportingService()
