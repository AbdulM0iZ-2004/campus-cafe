"""
models.py
Domain models for the Campus Café Ordering System.
Contains intentional code smells for structural analysis.
"""

from typing import List, Dict, Any, Optional


class CustomerProfileData:
    """
    SMELL 16: Data Class
    Holds pure data fields with zero business logic.
    """
    def __init__(self, name: str, email: str, member_id: int):
        self.name = name
        self.email = email
        self.member_id = member_id

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_email(self) -> str:
        return self.email

    def set_email(self, email: str) -> None:
        self.email = email


class DeliveryAddress:
    """
    SMELL 5: Data Clumps
    Repeats street, city, state, zip_code structure found in CustomerAccount.
    """
    def __init__(self, street: str, city: str, state: str, zip_code: str):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code


class CustomerAccount:
    """
    SMELL 3: Primitive Obsession
    Uses raw strings and tuples for structured data (phone, address, pricing tiers).
    
    SMELL 5: Data Clumps
    Duplicates street, city, state, zip_code fields present in DeliveryAddress.
    """
    def __init__(self, name: str, phone_str: str, street: str, city: str, state: str, zip_code: str, tier_tuple: tuple):
        self.name = name
        # Primitive Obsession: parsing phone numbers out of a formatted string manually
        self.phone_str = phone_str
        
        # Data Clump: cloned address fields
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        
        # Address info object used for Message Chain smell in processor
        self.address_info = DeliveryAddress(street, city, state, zip_code)
        
        # Primitive Obsession: tuple like ("VIP", 0.15, 100) instead of a Tier object
        self.tier_tuple = tier_tuple
        
        # Private fields targeted for Inappropriate Intimacy smell
        self._loyalty_score = tier_tuple[2] if len(tier_tuple) > 2 else 0
        self._internal_notes = []

    def get_area_code(self) -> str:
        # Primitive Obsession symptom: extracting sub-data via string manipulation
        if self.phone_str.startswith("(") and ")" in self.phone_str:
            return self.phone_str.split(")")[0].replace("(", "")
        return self.phone_str.split("-")[0]


class OrderItem:
    """
    SMELL 7: Temporary Field
    Attributes temp_discount_code and temp_scratchpad are only active during calculation.
    """
    def __init__(self, name: str, price: float, category: str, quantity: int = 1):
        self.name = name
        self.price = price
        self.category = category
        self.quantity = quantity
        
        # Temporary Fields (None most of the lifecycle)
        self.temp_discount_code: Optional[str] = None
        self.temp_scratchpad: Optional[Dict[str, Any]] = None

    def calculate_temp_promo(self, code: str) -> float:
        self.temp_discount_code = code
        self.temp_scratchpad = {"applied_at": "checkout", "factor": 0.9}
        discounted_price = self.price * self.temp_scratchpad["factor"]
        # Clear fields partially to leave residual temporary state
        return discounted_price


class MenuCategory:
    """Base class for menu categories."""
    def __init__(self, category_name: str):
        self.category_name = category_name
        self.items: List[OrderItem] = []

    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)


class ReadOnlyMenuCategory(MenuCategory):
    """
    SMELL 8: Refused Bequest
    Inherits from MenuCategory but rejects the add_item capability.
    """
    def __init__(self, category_name: str, fixed_items: List[OrderItem]):
        super().__init__(category_name)
        self.items = fixed_items

    def add_item(self, item: OrderItem) -> None:
        # Refusing parent behavior
        raise NotImplementedError("ReadOnlyMenuCategory does not support adding items dynamically.")


class StripeGateway:
    """
    SMELL 9: Alternative Classes with Different Interfaces (Class 1)
    Provides payment capability using method charge().
    """
    def charge(self, amount: float) -> bool:
        return amount > 0


class PayPalGateway:
    """
    SMELL 9: Alternative Classes with Different Interfaces (Class 2)
    Provides identical capability using method send_payment().
    """
    def send_payment(self, total_val: float) -> bool:
        return total_val > 0


# SMELL 10: Parallel Inheritance Hierarchies
class BaseItem:
    """Base class for items in hierarchy A."""
    def __init__(self, name: str, base_price: float):
        self.name = name
        self.base_price = base_price


class DrinkItem(BaseItem):
    """Subclass in hierarchy A."""
    def __init__(self, name: str, base_price: float, size_oz: int):
        super().__init__(name, base_price)
        self.size_oz = size_oz


class FoodItem(BaseItem):
    """Subclass in hierarchy A."""
    def __init__(self, name: str, base_price: float, is_warmed: bool):
        super().__init__(name, base_price)
        self.is_warmed = is_warmed


class BaseItemFormatter:
    """Base class for formatters in hierarchy B."""
    def format_item(self, item: BaseItem) -> str:
        return f"Item: {item.name}, Price: ${item.base_price:.2f}"


class DrinkItemFormatter(BaseItemFormatter):
    """Parallel subclass in hierarchy B corresponding to DrinkItem."""
    def format_item(self, item: DrinkItem) -> str:
        return f"Drink: {item.name} ({item.size_oz} oz), Price: ${item.base_price:.2f}"


class FoodItemFormatter(BaseItemFormatter):
    """Parallel subclass in hierarchy B corresponding to FoodItem."""
    def format_item(self, item: FoodItem) -> str:
        status = "Warm" if item.is_warmed else "Cold"
        return f"Food: {item.name} [{status}], Price: ${item.base_price:.2f}"
