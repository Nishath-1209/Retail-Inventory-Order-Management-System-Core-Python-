from typing import List, Dict
from src.dao.customer_dao import customer_dao

class CustomerError(Exception):
    pass

class CustomerService:
    def __init__(self, dao=customer_dao):
        self.dao = dao

    def add_customer(self, name: str, email: str, phone: str, city: str | None = None) -> Dict:
        all_customers = self.dao.list_customers()
        if any(c.get("email") == email for c in all_customers):
            raise CustomerError(f"Email already exists: {email}")
        return self.dao.add_customer(name, email, phone, city)

    def update_customer(self, email: str, phone: str | None = None, city: str | None = None) -> Dict:
        all_customers = self.dao.list_customers()
        cust = next((c for c in all_customers if c.get("email") == email), None)
        if not cust:
            raise CustomerError("Customer not found")
        fields = {}
        if phone:
            fields["phone"] = phone
        if city:
            fields["city"] = city
        return self.dao.update_customer(cust["cust_id"], fields)

    def delete_customer(self, email: str) -> Dict:
        all_customers = self.dao.list_customers()
        cust = next((c for c in all_customers if c.get("email") == email), None)
        if not cust:
            raise CustomerError("Customer not found")
        # Optional: check orders before deletion
        # if order_service.has_orders(cust["cust_id"]):
        #     raise CustomerError("Customer has orders, cannot delete")
        return self.dao.delete_customer(cust["cust_id"])

    def list_customers(self) -> List[Dict]:
        return self.dao.list_customers()

    def search_customer(self, email: str | None = None, city: str | None = None) -> List[Dict]:
        customers = self.dao.list_customers()
        if email:
            customers = [c for c in customers if c.get("email") == email]
        if city:
            customers = [c for c in customers if c.get("city") == city]
        return customers

# Singleton instance
customer_service = CustomerService()
