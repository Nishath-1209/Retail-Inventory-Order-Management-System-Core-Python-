from typing import List, Dict
from src.dao.customer_dao import customer_dao
from src.dao.product_dao import product_dao
from src.dao.order_dao import order_dao

class OrderError(Exception):
    pass

class OrderService:
    def __init__(self, dao=order_dao):
        self.dao = dao

    # ---------------- Create Order ----------------
    def create_order(self, cust_id: int, items: List[Dict]) -> Dict:
        customer = customer_dao.get_customer_by_id(cust_id)
        if not customer:
            raise OrderError("Customer not found")

        validated_items = []
        for item in items:
            prod_id = item.get("prod_id")
            qty = item.get("quantity")
            if prod_id is None or qty is None:
                raise OrderError("Invalid item format")
            product = product_dao.get_product_by_id(prod_id)
            if not product:
                raise OrderError(f"Product not found: {prod_id}")
            if product["stock"] < qty:
                raise OrderError(f"Insufficient stock for {product['name']}")
            validated_items.append((product, qty, float(product["price"])))

        dao_items = [
            {"prod_id": p["prod_id"], "quantity": q, "price": price}
            for p, q, price in validated_items
        ]

        order = self.dao.create_order(cust_id, dao_items)
        if not order:
            raise OrderError("Failed to create order")

        # Deduct stock
        for product, qty, _ in validated_items:
            product_dao.update_product(product["prod_id"], {"stock": product["stock"] - qty})

        # Attach order items
        order["items"] = self.dao.get_order_items(order["order_id"])

        # Create pending payment (local import avoids circular import)
        from src.services.payment_service import payment_service
        payment_service.create_pending_payment(order["order_id"], order["total_amount"])

        return order

    # ---------------- Get Order Details ----------------
    def get_order_details(self, order_id: int) -> Dict:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError("Order not found")
        order["items"] = self.dao.get_order_items(order_id)
        return order

    # ---------------- Cancel Order ----------------
    def cancel_order(self, order_id: int) -> Dict:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError("Order not found")
        if order["status"] != "PLACED":
            raise OrderError("Only PLACED orders can be cancelled")

        items = self.dao.get_order_items(order_id)
        for item in items:
            product = product_dao.get_product_by_id(item["prod_id"])
            if product:
                product_dao.update_product(product["prod_id"], {"stock": product["stock"] + item["quantity"]})

        # Refund payment (local import avoids circular import)
        from src.services.payment_service import payment_service
        payment_service.refund_order_payment(order_id)

        return self.dao.update_order_status(order_id, "CANCELLED")

    # ---------------- Complete Order ----------------
    def complete_order(self, order_id: int) -> Dict:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError("Order not found")
        if order.get("status") != "PLACED":
            raise OrderError("Only PLACED orders can be completed")
        return self.dao.update_order_status(order_id, "COMPLETED")

    # ---------------- List Orders by Customer ----------------
    def list_orders_by_customer(self, cust_id: int) -> List[Dict]:
        customer = customer_dao.get_customer_by_id(cust_id)
        if not customer:
            raise OrderError("Customer not found")
        return self.dao.list_orders_by_customer(cust_id)

# ---------------- Singleton Instance ----------------
order_service = OrderService()
