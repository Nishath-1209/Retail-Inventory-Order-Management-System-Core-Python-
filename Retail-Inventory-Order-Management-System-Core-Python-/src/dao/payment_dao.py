from typing import Dict, Optional, List
from src.config import get_supabase
from datetime import datetime

_sb = get_supabase()

class PaymentDAO:
    def __init__(self):
        self.sb = _sb

    def create_payment(self, order_id: int, amount: float) -> Optional[Dict]:
        """Create a pending payment for an order"""
        resp = self.sb.table("payments").insert({
            "order_id": order_id,
            "amount": amount,
            "status": "PENDING",
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        return resp.data[0] if resp.data else None

    def process_payment(self, order_id: int, method: str) -> Optional[Dict]:
        """Mark payment as PAID"""
        self.sb.table("payments").update({
            "status": "PAID",
            "method": method,
            "paid_at": datetime.utcnow().isoformat()
        }).eq("order_id", order_id).execute()
        return self.get_payment_by_order(order_id)

    def refund_payment(self, order_id: int) -> Optional[Dict]:
        """Mark payment as REFUNDED"""
        self.sb.table("payments").update({
            "status": "REFUNDED",
            "refunded_at": datetime.utcnow().isoformat()
        }).eq("order_id", order_id).execute()
        return self.get_payment_by_order(order_id)

    def get_payment_by_order(self, order_id: int) -> Optional[Dict]:
        resp = self.sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

# Singleton
payment_dao = PaymentDAO()
