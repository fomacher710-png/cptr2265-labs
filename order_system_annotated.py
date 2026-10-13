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


# --------------------------------------------------------------------------
# Domain classes
# --------------------------------------------------------------------------

class Item:
    def __init__(self, sku, name, price, quantity):
        self.sku = sku
        self.name = name
        self.price = price
        self.quantity = quantity


class Order:
    def __init__(self, order_id, customer_name, customer_email, customer_type,
                 payment_type):
        self.order_id = order_id
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_type = customer_type      # "student", "staff", "public"
        self.payment_type = payment_type        # "card", "campus_cash", "invoice"
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def subtotal(self):
        return sum(i.price * i.quantity for i in self.items)

    def shipping_cost(self):
        if self.subtotal() >= 50:
            return 0.0
        return 5.99

#(LSP) The base class (Order) presumably defines a shipping_cost() method that callers expect to return a valid cost 
class DigitalOrder(Order):
    """An order for e-books and access codes. Nothing physical ships."""

    def shipping_cost(self):
        raise NotImplementedError("Digital orders do not ship!")


# --------------------------------------------------------------------------
# Notification
# --------------------------------------------------------------------------
# (ISP) Notifier forces all notification subclasses to implement SMS, push notifications, and emails, even if they only support a single channel.
class Notifier:
    """Every notifier must support every channel."""

    def send_email(self, to, subject, body):
        raise NotImplementedError

    def send_sms(self, phone, message):
        raise NotImplementedError

    def send_push(self, device_id, message):
        raise NotImplementedError


class EmailNotifier(Notifier):
    def send_email(self, to, subject, body):
        print(f"[EMAIL to {to}] {subject}")
        print(body)

    def send_sms(self, phone, message):
        raise Exception("EmailNotifier cannot send SMS")

    def send_push(self, device_id, message):
        raise Exception("EmailNotifier cannot send push notifications")


# --------------------------------------------------------------------------
# Storage
# --------------------------------------------------------------------------

class TextFileDatabase:
    def __init__(self, filename):
        self.filename = filename

    def save_line(self, line):
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(line + "\n")


# --------------------------------------------------------------------------
# The order processor
# --------------------------------------------------------------------------
#  (SRP) OrderProcessor handles too many responsibilities: input validation, discount logic, tax/shipping
class OrderProcessor:
    def __init__(self):
        self.database = TextFileDatabase("orders.txt")
        self.notifier = EmailNotifier()

    def process(self, order):
        # ---- validate ----
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

        # ---- discounts ----
        subtotal = order.subtotal()
        if order.customer_type == "student":
            discount = subtotal * 0.10
        elif order.customer_type == "staff":
            discount = subtotal * 0.15
        elif order.customer_type == "public":
            discount = 0.0
        else:
            raise ValueError("Unknown customer type: " + order.customer_type)

        # ---- shipping & tax ----
        shipping = order.shipping_cost()
        tax = round((subtotal - discount) * 0.07875, 2)
        total = round(subtotal - discount + tax + shipping, 2)

        # ---- payment ----
        if order.payment_type == "card":
            print(f"Charging ${total:.2f} to credit card on file...")
            fee = round(total * 0.029, 2)
            print(f"  Card processing fee recorded: ${fee:.2f}")
        elif order.payment_type == "campus_cash":
            print(f"Deducting ${total:.2f} from campus cash account...")
        elif order.payment_type == "invoice":
            print(f"Generating invoice for ${total:.2f}, due in 30 days...")
        else:
            raise ValueError("Unknown payment type: " + order.payment_type)

        # ---- receipt formatting ----
        lines = []
        lines.append("=" * 40)
        lines.append("MCTC CAMPUS BOOKSTORE")
        lines.append(f"Order #{order.order_id}   {datetime.date.today()}")
        lines.append(f"Customer: {order.customer_name} ({order.customer_type})")
        lines.append("-" * 40)
        for item in order.items:
            line_total = item.price * item.quantity
            lines.append(f"{item.quantity} x {item.name:<26} ${line_total:>8.2f}")
        lines.append("-" * 40)
        lines.append(f"{'Subtotal':<30} ${subtotal:>8.2f}")
        lines.append(f"{'Discount':<29} -${discount:>8.2f}")
        lines.append(f"{'Tax':<30} ${tax:>8.2f}")
        lines.append(f"{'Shipping':<30} ${shipping:>8.2f}")
        lines.append(f"{'TOTAL':<30} ${total:>8.2f}")
        lines.append("=" * 40)
        receipt = "\n".join(lines)

        # ---- persist ----
        self.database.save_line(
            f"{order.order_id}|{order.customer_email}|{order.payment_type}|{total:.2f}"
        )

        # ---- notify ----
        self.notifier.send_email(order.customer_email,
                                 f"Your bookstore order #{order.order_id}",
                                 receipt)
        return True


# --------------------------------------------------------------------------
# Demo
# --------------------------------------------------------------------------

def main():
    processor = OrderProcessor()

    order1 = Order(1001, "Ana Lopez", "ana@student.mctc.edu", "student", "card")
    order1.add_item(Item("TXT-2265", "Software Engineering 10e", 89.99, 1))
    order1.add_item(Item("SUP-0042", "Engineering notebook", 6.50, 2))
    processor.process(order1)

    print()
    order2 = Order(1002, "Dr. Kim", "kim@mctc.edu", "staff", "invoice")
    order2.add_item(Item("SUP-0007", "Whiteboard markers", 12.00, 1))
    processor.process(order2)

    print()
    order3 = DigitalOrder(1003, "Sam Ortiz", "sam@student.mctc.edu", "student",
                          "campus_cash")
    order3.add_item(Item("EBK-2265", "Software Engineering e-book", 54.00, 1))
    try:
        processor.process(order3)
    except NotImplementedError as e:
        # Something is wrong with the design if callers need this try/except!
        print(f"*** Order 1003 crashed: {e}")


if __name__ == "__main__":
    main()
