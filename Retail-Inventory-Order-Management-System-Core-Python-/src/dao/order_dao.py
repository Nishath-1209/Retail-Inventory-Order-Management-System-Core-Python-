from typing import List, Dict, Optional
from src.config import get_supabase

_sb = get_supabase()

class OrderDAO:
    def __init__(self):
        self.sb = _sb

    def create_order(self, cust_id: int, items: List[Dict]) -> Optional[Dict]:
        """
        Create an order and insert its items.
        Each item dict should have: prod_id, quantity, price
        """
        # Calculate total
        total = sum(item.get("price", 0) * item.get("quantity", 0) for item in items)

        # Insert order
        order_resp = self.sb.table("orders").insert({
            "cust_id": cust_id,
            "total_amount": total,
            "status": "PLACED"
        }).execute()
        if not order_resp.data:
            return None

        order_id = order_resp.data[0]["order_id"]

        # Insert order items
        for item in items:
            prod_id = item.get("prod_id")
            qty = item.get("quantity")
            price = item.get("price")
            if prod_id is None or qty is None or price is None:
                raise ValueError(f"Invalid item: {item}")
            self.sb.table("order_items").insert({
                "order_id": order_id,
                "prod_id": prod_id,
                "quantity": qty,
                "price": price
            }).execute()

        return self.get_order_by_id(order_id)

    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        """
        Get order details along with its items
        """
        resp = self.sb.table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        if not resp.data:
            return None
        order = resp.data[0]
        order["items"] = self.get_order_items(order_id)
        return order

    def get_order_items(self, order_id: int) -> List[Dict]:
        """
        Get all items for a given order
        """
        resp = self.sb.table("order_items").select("*").eq("order_id", order_id).execute()
        return resp.data or []

    def update_order_status(self, order_id: int, status: str) -> Optional[Dict]:
        """
        Update order status and return updated order with items
        """
        self.sb.table("orders").update({"status": status}).eq("order_id", order_id).execute()
        return self.get_order_by_id(order_id)

    def list_orders_by_customer(self, cust_id: int) -> List[Dict]:
        """
        List all orders for a customer, each with its items
        """
        resp = self.sb.table("orders").select("*").eq("cust_id", cust_id).execute()
        orders = resp.data or []
        for order in orders:
            order["items"] = self.get_order_items(order["order_id"])
        return orders
    def list_all_orders(self) -> List[Dict]:
        resp = self.sb.table("orders").select("*").execute()
        return resp.data or []

# Singleton instance
order_dao = OrderDAO()
