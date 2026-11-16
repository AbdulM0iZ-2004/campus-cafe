"""
test_cafe_system.py
Complete unit test suite verifying system operation while validating all 22 code smells.
Executes with zero errors: python -m unittest test_cafe_system.py
"""

import unittest
from models import (
    CustomerProfileData, DeliveryAddress, CustomerAccount, OrderItem,
    MenuCategory, ReadOnlyMenuCategory, StripeGateway, PayPalGateway,
    DrinkItem, DrinkItemFormatter, FoodItem, FoodItemFormatter
)
from order_processor import OrderProcessor, Order, OrderProcessorMiddleMan
from legacy_helpers import (
    LegacyAuditManager, LegacyTaxCalculator, SimpleTaxNotifier,
    AbstractQuantumDiscountStrategy, obsolete_apply_v1_discount, calculate_complex_points
)


class TestCampusCafeSystem(unittest.TestCase):

    def setUp(self):
        self.customer = CustomerAccount(
            name="Alex Student",
            phone_str="(555) 019-2831",
            street="123 Campus Way",
            city="University Town",
            state="CA",
            zip_code="90210",
            tier_tuple=("GOLD", 0.10, 150)
        )
        self.item1 = OrderItem("Espresso", 3.50, "beverage", 2)
        self.item2 = OrderItem("Panini", 8.00, "prepared_food", 1)
        self.order = Order(self.customer, [self.item1, self.item2])
        self.processor = OrderProcessor()

    def test_end_to_end_order_processing(self):
        # Validates Smell 1 (Long Method) & Smell 2 (Large Class)
        result = self.processor.process_customer_order(
            order=self.order,
            payment_method="stripe",
            is_student=True,
            is_faculty=False,
            promo_code="CAMPUS5"
        )
        self.assertTrue(result["payment_success"])
        self.assertEqual(result["subtotal"], 15.0)
        # Tax: (7.0 * 0.08) + (8.0 * 0.08) = 0.56 + 0.64 = 1.20
        self.assertAlmostEqual(result["tax"], 1.20)
        # Discount: 10% student on 15.0 = 1.50 + $5 promo = 6.50
        self.assertEqual(result["discount"], 6.50)
        # Final: 15.0 + 1.20 - 6.50 = 9.70
        self.assertAlmostEqual(result["final_total"], 9.70)

    def test_primitive_obsession_and_data_clumps(self):
        # Validates Smell 3 (Primitive Obsession) & Smell 5 (Data Clumps)
        self.assertEqual(self.customer.get_area_code(), "555")
        address = DeliveryAddress("123 Campus Way", "University Town", "CA", "90210")
        self.assertEqual(address.zip_code, self.customer.zip_code)

    def test_long_parameter_list(self):
        # Validates Smell 4 (Long Parameter List)
        discount = self.processor.calculate_custom_discount(
            100.0, True, False, False, False, True, "Tuesday", 10
        )
        # 10% (student) + 5% (coupon) + 5% (Tuesday) + 2% (morning) = 22% of 100 = 22.0
        self.assertAlmostEqual(discount, 22.0)

    def test_switch_statements_tax(self):
        # Validates Smell 6 (Switch Statements)
        tax_bev = self.processor.apply_tax_by_type(self.item1)
        self.assertAlmostEqual(tax_bev, 0.56)

    def test_temporary_field(self):
        # Validates Smell 7 (Temporary Field)
        discounted = self.item1.calculate_temp_promo("FALL2024")
        self.assertEqual(discounted, 3.15)
        self.assertEqual(self.item1.temp_discount_code, "FALL2024")

    def test_refused_bequest(self):
        # Validates Smell 8 (Refused Bequest)
        read_only_cat = ReadOnlyMenuCategory("Daily Specials", [self.item1])
        with self.assertRaises(NotImplementedError):
            read_only_cat.add_item(self.item2)

    def test_alternative_classes_with_different_interfaces(self):
        # Validates Smell 9 (Alternative Classes with Different Interfaces)
        stripe = StripeGateway()
        paypal = PayPalGateway()
        self.assertTrue(stripe.charge(50.0))
        self.assertTrue(paypal.send_payment(50.0))

    def test_parallel_inheritance_hierarchies(self):
        # Validates Smell 10 (Parallel Inheritance Hierarchies)
        drink = DrinkItem("Latte", 4.50, 16)
        food = FoodItem("Croissant", 3.00, True)
        drink_formatter = DrinkItemFormatter()
        food_formatter = FoodItemFormatter()
        
        self.assertIn("16 oz", drink_formatter.format_item(drink))
        self.assertIn("Warm", food_formatter.format_item(food))

    def test_divergent_change_and_shotgun_surgery(self):
        # Validates Smell 11 (Divergent Change) & Smell 12 (Shotgun Surgery)
        audit_mgr = LegacyAuditManager("db://localhost:5432/cafe")
        self.assertTrue(audit_mgr.log_to_database({"test": 1}))
        self.assertEqual(audit_mgr.export_to_csv({"customer_name": "Alex", "final_total": 10.0}), "Alex,10.0")
        
        legacy_calc = LegacyTaxCalculator()
        self.assertAlmostEqual(legacy_calc.calculate_legacy_tax(100.0), 8.0)

    def test_comments_and_dead_code(self):
        # Validates Smell 13 (Comments) & Smell 17 (Dead Code)
        points = calculate_complex_points(10.0, 2)
        self.assertEqual(points, 100)
        self.assertAlmostEqual(obsolete_apply_v1_discount(100.0), 70.0)

    def test_duplicate_code(self):
        # Validates Smell 14 (Duplicate Code)
        std_receipt = self.processor.format_receipt_standard(self.order)
        exp_receipt = self.processor.format_receipt_express(self.order)
        self.assertIn("Subtotal: $15.00", std_receipt)
        self.assertIn("Subtotal: $15.00", exp_receipt)

    def test_lazy_class_and_data_class(self):
        # Validates Smell 15 (Lazy Class) & Smell 16 (Data Class)
        notifier = SimpleTaxNotifier()
        notifier.notify_tax(1.20)
        
        profile = CustomerProfileData("Sam", "sam@univ.edu", 101)
        self.assertEqual(profile.get_email(), "sam@univ.edu")

    def test_speculative_generality(self):
        # Validates Smell 18 (Speculative Generality)
        strategy = AbstractQuantumDiscountStrategy()
        with self.assertRaises(NotImplementedError):
            strategy.calculate_quantum_discount(1.0, 2.0)

    def test_feature_envy(self):
        # Validates Smell 19 (Feature Envy)
        savings = self.processor.compute_item_savings(self.item1, 4.00)
        self.assertAlmostEqual(savings, 1.00)

    def test_inappropriate_intimacy(self):
        # Validates Smell 20 (Inappropriate Intimacy)
        initial_score = self.customer._loyalty_score
        self.processor.adjust_customer_internals(self.customer, 50)
        self.assertEqual(self.customer._loyalty_score, initial_score + 50)
        self.assertEqual(len(self.customer._internal_notes), 1)

    def test_message_chains(self):
        # Validates Smell 21 (Message Chains)
        zip_code = self.processor.get_customer_zip_code(self.order)
        self.assertEqual(zip_code, "90210")

    def test_middle_man(self):
        # Validates Smell 22 (Middle Man)
        middle_man = OrderProcessorMiddleMan(self.processor)
        res = middle_man.process_customer_order(self.order, "stripe", True, False, "")
        self.assertTrue(res["payment_success"])


if __name__ == "__main__":
    unittest.main()