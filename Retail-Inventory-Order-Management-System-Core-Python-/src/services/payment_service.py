from typing import Dict
from src.dao.payment_dao import payment_dao

class PaymentError(Exception):
    pass

class PaymentService:
    def __init__(self, dao=payment_dao):
        self.dao = dao

    def create_payment_for_order(self, order: Dict):
        return self.dao.create_payment(order["order_id"], order["total_amount"])

    def pay_order(self, order_id: int, method: str):
        # Process payment
        payment = self.dao.process_payment(order_id, method)
        if not payment:
            raise PaymentError("Payment processing failed")

        # Import here to avoid circular dependency
        from src.services.order_service import order_service  
        order_service.complete_order(order_id)

        return payment

    def refund_order_payment(self, order_id: int):
        return self.dao.refund_payment(order_id)

# Singleton
payment_service = PaymentService()
