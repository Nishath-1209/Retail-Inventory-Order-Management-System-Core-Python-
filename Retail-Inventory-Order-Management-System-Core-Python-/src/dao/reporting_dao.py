from typing import List, Dict
from src.config import get_supabase

_sb = get_supabase()

class ReportingDAO:
    def __init__(self):
        self.sb = _sb

    def fetch_all_orders(self) -> List[Dict]:
        """Fetch all orders from DB"""
        resp = self.sb.table("orders").select("*").eq("status", "COMPLETED").execute()
        return resp.data or []

    def fetch_order_items(self, order_id: int) -> List[Dict]:
        """Fetch items for a given order"""
        resp = self.sb.table("order_items").select("*").eq("order_id", order_id).execute()
        return resp.data or []

    def fetch_all_customers(self) -> List[Dict]:
        """Fetch all customers"""
        resp = self.sb.table("customers").select("*").execute()
        return resp.data or []

    def fetch_all_products(self) -> List[Dict]:
        """Fetch all products"""
        resp = self.sb.table("products").select("*").execute()
        return resp.data or []

# Singleton
reporting_dao = ReportingDAO()
