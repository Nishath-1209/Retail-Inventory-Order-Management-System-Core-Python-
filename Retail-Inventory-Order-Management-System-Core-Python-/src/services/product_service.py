from typing import List, Dict
from src.dao.product_dao import ProductDAO, product_dao

class ProductError(Exception):
    pass

class ProductService:
    def __init__(self, dao: ProductDAO = product_dao):
        self.dao = dao

    def add_product(self, name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Dict:
        if price <= 0:
            raise ProductError("Price must be greater than 0")
        existing = self.dao.get_product_by_sku(sku)
        if existing:
            raise ProductError(f"SKU already exists: {sku}")
        return self.dao.create_product(name, sku, price, stock, category)

    def update_product(self, prod_id: int, fields: Dict) -> Dict:
        p = self.dao.get_product_by_id(prod_id)
        if not p:
            raise ProductError("Product not found")
        return self.dao.update_product(prod_id, fields)

    def delete_product(self, prod_id: int) -> Dict:
        p = self.dao.get_product_by_id(prod_id)
        if not p:
            raise ProductError("Product not found")
        return self.dao.delete_product(prod_id)

    def restock_product(self, prod_id: int, delta: int) -> Dict:
        if delta <= 0:
            raise ProductError("Delta must be positive")
        p = self.dao.get_product_by_id(prod_id)
        if not p:
            raise ProductError("Product not found")
        new_stock = (p.get("stock") or 0) + delta
        return self.dao.update_product(prod_id, {"stock": new_stock})

    def get_low_stock(self, threshold: int = 5) -> List[Dict]:
        allp = self.dao.list_products(limit=1000)
        return [p for p in allp if (p.get("stock") or 0) <= threshold]

    def get_all_products(self, limit: int = 1000) -> List[Dict]:
        return self.dao.list_products(limit=limit)

# Singleton instance
product_service = ProductService()
