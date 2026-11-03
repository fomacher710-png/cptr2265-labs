"""
CPTR 2265 - Lab 7, Part A starter: Campus Bookstore Order System
=================================================================

This program runs (try it: `python order_system.py`), but its design is poor.
It violates at least three of the five SOLID principles -- and one of those
violations already causes a crash in the demo at the bottom of the file.

Your tasks (see the Week 7 lab page for full details):
  1. Copy this file to lab07/original/ and annotate it: add a comment such as
         # SOLID VIOLATION (SRP): ...explanation...
     at every place you find a violation. Commit.
  2. Refactor the code (in lab07/refactored/) so it complies with SOLID.
     The program should still produce the same receipts and behavior. Commit.

Hint: look at who is responsible for what, what you would have to edit to add
a new customer type or payment method, whether every subclass can really be
used where its parent is expected, whether every class needs every method it
is forced to implement, and which classes create their own dependencies.
"""

import datetime
from abc import ABC, abstractmethod

# --------------------------------------------------------------------------
# Domain Classes
# --------------------------------------------------------------------------

class Item:
    def __init__(self, sku, name, price, quantity):
        self.sku = sku
        self.name = name
        self.price = price
        self.quantity = quantity


class Order(ABC):
    def __init__(self, order_id, customer_name, customer_email, customer_type, payment_strategy):
        self.order_id = order_id
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_type = customer_type
        self.payment_strategy = payment_strategy
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def subtotal(self):
        return sum(i.price * i.quantity for i in self.items)

    @abstractmethod
    def shipping_cost(self):
        pass


class PhysicalOrder(Order):
    def shipping_cost(self):
        if self.subtotal() >= 50:
            return 0.0
        return 5.99


class DigitalOrder(Order):
    def shipping_cost(self):
        return 0.0


# --------------------------------------------------------------------------
# Strategies (OCP Compliance)
# --------------------------------------------------------------------------

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, subtotal):
        pass


class StudentDiscount(DiscountStrategy):
    def calculate_discount(self, subtotal):
        return subtotal * 0.10


class StaffDiscount(DiscountStrategy):
    def calculate_discount(self, subtotal):
        return subtotal * 0.15


class PublicDiscount(DiscountStrategy):
    def calculate_discount(self, subtotal):
        return 0.0


class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, total):
        pass


class CreditCardPayment(PaymentStrategy):
    def process_payment(self, total):
        print(f"Charging ${total:.2f} to credit card on file...")
        fee = round(total * 0.029, 2)
        print(f"  Card processing fee recorded: ${fee:.2f}")


class CampusCashPayment(PaymentStrategy):
    def process_payment(self, total):
        print(f"Deducting ${total:.2f} from campus cash account...")


class InvoicePayment(PaymentStrategy):
    def process_payment(self, total):
        print(f"Generating invoice for ${total:.2f}, due in 30 days...")


# --------------------------------------------------------------------------
# Interfaces & Services (ISP & DIP Compliance)
# --------------------------------------------------------------------------

class Notifier(ABC):
    @abstractmethod
    def send(self, recipient, subject, body):
        pass


class EmailNotifier(Notifier):
    def send(self, recipient, subject, body):
        print(f"[EMAIL to {recipient}] {subject}")
        print(body)


class OrderRepository(ABC):
    @abstractmethod
    def save(self, record):
        pass


class TextFileDatabase(OrderRepository):
    def __init__(self, filename):
        self.filename = filename

    def save(self, record):
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(record + "\n")


class ReceiptFormatter:
    @staticmethod
    def format_receipt(order, subtotal, discount, tax, shipping, total):
        lines = [
            "=" * 40,
            "MCTC CAMPUS BOOKSTORE",
            f"Order #{order.order_id}   {datetime.date.today()}",
            f"Customer: {order.customer_name} ({order.customer_type})",
            "-" * 40
        ]
        for item in order.items:
            line_total = item.price * item.quantity
            lines.append(f"{item.quantity} x {item.name:<26} ${line_total:>8.2f}")
        lines.extend([
            "-" * 40,
            f"{'Subtotal':<30} ${subtotal:>8.2f}",
            f"{'Discount':<29} -${discount:>8.2f}",
            f"{'Tax':<30} ${tax:>8.2f}",
            f"{'Shipping':<30} ${shipping:>8.2f}",
            f"{'TOTAL':<30} ${total:>8.2f}",
            "=" * 40
        ])
        return "\n".join(lines)


# --------------------------------------------------------------------------
# Order Processor (SRP & DIP Compliant)
# --------------------------------------------------------------------------

class OrderProcessor:
    def __init__(self, repository: OrderRepository, notifier: Notifier):
        self.repository = repository
        self.notifier = notifier

    def validate(self, order):
        if not order.items:
            print(f"Order {order.order_id} rejected: no items")
            return False
        if "@" not in order.customer_email:
            print(f"Order {order.order_id} rejected: bad email")
            return False
        for item in order.items:
            if item.quantity <= 0 or item.price < 0:
                print(f"Order {order.order_id} rejected: bad item {item.sku}")
                return False
        return True

    def process(self, order, discount_strategy: DiscountStrategy):
        if not self.validate(order):
            return False

        subtotal = order.subtotal()
        discount = discount_strategy.calculate_discount(subtotal)
        shipping = order.shipping_cost()
        tax = round((subtotal - discount) * 0.07875, 2)
        total = round(subtotal - discount + tax + shipping, 2)

        # Process payment via polymorphism
        order.payment_strategy.process_payment(total)

        # Generate receipt
        receipt = ReceiptFormatter.format_receipt(order, subtotal, discount, tax, shipping, total)

        # Persist data
        self.repository.save(
            f"{order.order_id}|{order.customer_email}|{order.customer_type}|{total:.2f}"
        )

        # Notify customer
        self.notifier.send(
            order.customer_email,
            f"Your bookstore order #{order.order_id}",
            receipt
        )
        return True


# --------------------------------------------------------------------------
# Demo
# --------------------------------------------------------------------------

def main():
    # Dependencies injected (DIP)
    processor = OrderProcessor(TextFileDatabase("orders.txt"), EmailNotifier())

    order1 = PhysicalOrder(1001, "Ana Lopez", "ana@student.mctc.edu", "student", CreditCardPayment())
    order1.add_item(Item("TXT-2265", "Software Engineering 10e", 89.99, 1))
    order1.add_item(Item("SUP-0042", "Engineering notebook", 6.50, 2))
    processor.process(order1, StudentDiscount())

    print()
    order2 = PhysicalOrder(1002, "Dr. Kim", "kim@mctc.edu", "staff", InvoicePayment())
    order2.add_item(Item("SUP-0007", "Whiteboard markers", 12.00, 1))
    processor.process(order2, StaffDiscount())

    print()
    order3 = DigitalOrder(1003, "Sam Ortiz", "sam@student.mctc.edu", "student", CampusCashPayment())
    order3.add_item(Item("EBK-2265", "Software Engineering e-book", 54.00, 1))
    # DigitalOrder now safely handles shipping cost without crashing
    processor.process(order3, StudentDiscount())


if __name__ == "__main__":
    main()