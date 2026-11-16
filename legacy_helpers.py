"""
legacy_helpers.py
Legacy helper functions, audit management, and tax notification code.
Contains intentional code smells for structural analysis.
"""

from typing import Dict, Any


class LegacyAuditManager:
    """
    SMELL 11: Divergent Change
    This class is modified for database connections, CSV formatting, and cryptographic hashing.
    """
    def __init__(self, db_connection_string: str):
        self.db_conn = db_connection_string

    def log_to_database(self, record: Dict[str, Any]) -> bool:
        # Reason to change 1: Database schema updates
        return True

    def export_to_csv(self, record: Dict[str, Any]) -> str:
        # Reason to change 2: CSV format style updates
        return f"{record.get('customer_name')},{record.get('final_total')}"

    def hash_audit_record(self, record: Dict[str, Any]) -> str:
        # Reason to change 3: Security algorithm updates
        import hashlib
        return hashlib.md5(str(record).encode()).hexdigest()


class LegacyTaxCalculator:
    """
    SMELL 12: Shotgun Surgery (Participant)
    Changing the default tax rate requires editing this class, OrderProcessor, and models.py.
    """
    def calculate_legacy_tax(self, amount: float) -> float:
        # Shared hardcoded tax rate: 0.08
        return amount * 0.08


class SimpleTaxNotifier:
    """
    SMELL 15: Lazy Class
    A class that barely does anything, containing only a single trivial print method.
    """
    def notify_tax(self, tax_amount: float) -> None:
        print(f"Tax calculated: {tax_amount}")


class AbstractQuantumDiscountStrategy:
    """
    SMELL 18: Speculative Generality
    Over-engineered abstract architecture built for future discount possibilities that are never used.
    """
    def calculate_quantum_discount(self, vector_a: float, vector_b: float) -> float:
        raise NotImplementedError("Future quantum discount engine not implemented.")


def obsolete_apply_v1_discount(price: float) -> float:
    """
    SMELL 17: Dead Code
    Unused function remaining in the repository.
    """
    return price * 0.70


def calculate_complex_points(subtotal: float, tier_multiplier: int) -> int:
    """
    SMELL 13: Comments
    Excessive comments explaining simple code instead of making code self-documenting.
    """
    # First step: multiply subtotal by 10 to convert dollars to base points scale
    step1 = subtotal * 10
    # Second step: multiply the result by the customer tier multiplier integer
    step2 = step1 * tier_multiplier
    # Third step: divide by 2 because the café runs a half-point promotion on Tuesdays
    step3 = step2 / 2
    # Fourth step: cast to integer to drop fractional points
    final_points = int(step3)
    # Return the computed integer points value
    return final_points