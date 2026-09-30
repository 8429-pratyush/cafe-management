import json
import os
from datetime import datetime

GST_RATE = 5
ADMIN_PASSWORD = "admin123"


menu = {"Coffee": 60, "Tea": 30, "Cold Coffee": 90, "Sandwich": 80,
        "Burger": 100, "Pasta": 130, "Brownie": 70}
orders = []


def is_good_order(o):

    if type(o) != dict:
        return False
    if "date" not in o or "items" not in o or "total" not in o:
        return False
    for item in o["items"]:
        if "name" not in item or "qty" not in item:
            return False
    return True


if os.path.exists("menu.json"):
    try:
        f = open("menu.json")
        data = json.load(f)
        f.close()
        new_menu = {}
        for name in data:
            price = data[name]
 
            if type(price) == dict:
                price = price.get("price")
            if type(price) == int or type(price) == float:
                new_menu[name] = price
        if len(new_menu) > 0:
            menu = new_menu
    except Exception:
        print("menu.json padh nahi paaye, default menu use ho raha hai")

if os.path.exists("orders.json"):
    try:
        f = open("orders.json")
        data = json.load(f)
        f.close()
        for o in data:
            if is_good_order(o):
                orders.append(o)
    except Exception:
        print("orders.json padh nahi paaye, naye orders se shuru")
        orders = []


def save():
   
    f = open("menu.json", "w")
    json.dump(menu, f, indent=4)
    f.close()
    f = open("orders.json", "w")
    json.dump(orders, f, indent=4)
    f.close()


def show_menu():
    print("\n------ CAFE MENU ------")
    if len(menu) == 0:
        print("menu is empty")
        return
    number = 1
    for name in menu:
        print(str(number) + ". " + name + " - Rs " + str(menu[name]))
        number = number + 1


def take_order():
    if len(menu) == 0:
        print("menu is empty, ask admin to add items")
        return
    show_menu()
    names = list(menu.keys())
    cart = {}   

    while True:
        try:
            n = int(input("\nItem number (0 to finish): "))
        except ValueError:
            print("please enter a number")
            continue
        if n == 0:
            break
        if n < 1 or n > len(names):
            print("no such item")
            continue
        try:
            qty = int(input("Quantity: "))
        except ValueError:
            print("quantity should be a number")
            continue
        if qty < 1:
            print("quantity should be at least 1")
            continue

        name = names[n - 1]
        if name in cart:
            cart[name] = cart[name] + qty
        else:
            cart[name] = qty
        print(qty, name, "added")

    if len(cart) == 0:
        print("nothing ordered")
        return
    customer = input("Customer name (press enter to skip): ").strip()
    if customer == "":
        customer = "Guest"
    make_bill(cart, customer)


def make_bill(cart, customer):
    bill_no = len(orders) + 1
    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    items = []
    subtotal = 0
    for name in cart:
        price = menu[name]
        qty = cart[name]
        amount = price * qty
        subtotal = subtotal + amount
        items.append({"name": name, "price": price, "qty": qty, "amount": amount})

    gst = round(subtotal * GST_RATE / 100, 2)
    total = round(subtotal + gst, 2)

   
    print("\n" + "=" * 42)
    print("                CAFE BILL")
    print("=" * 42)
    print("Bill No :", bill_no)
    print("Date    :", date)
    print("Customer:", customer)
    print("-" * 42)
    print("Item".ljust(18) + "Price".rjust(7) + "Qty".rjust(5) + "Amount".rjust(10))
    print("-" * 42)
    for it in items:
        print(it["name"].ljust(18) + str(it["price"]).rjust(7)
              + str(it["qty"]).rjust(5) + str(it["amount"]).rjust(10))
    print("-" * 42)
    print("Subtotal".ljust(30) + ("%.2f" % subtotal).rjust(12))
    print(("GST (" + str(GST_RATE) + "%)").ljust(30) + ("%.2f" % gst).rjust(12))
    print("TOTAL".ljust(30) + ("%.2f" % total).rjust(12))
    print("=" * 42)
    print("     Thank you! Visit again :)")

   
    order = {"order_id": bill_no, "date": date, "customer": customer,
             "items": items, "subtotal": subtotal, "gst": gst, "total": total}
    orders.append(order)
    save()


def pick_item():
    
    show_menu()
    if len(menu) == 0:
        return None
    try:
        n = int(input("Item number: "))
    except ValueError:
        print("please enter a number")
        return None
    names = list(menu.keys())
    if n < 1 or n > len(names):
        print("no such item")
        return None
    return names[n - 1]


def admin():
    p = input("Enter admin password: ")
    if p != ADMIN_PASSWORD:
        print("wrong password")
        return

    while True:
        print("\n--- ADMIN PANEL ---")
        print("1. Add item")
        print("2. Change price")
        print("3. Remove item")
        print("4. Back")
        ch = input("Choose: ")

        if ch == "1":
            name = input("Item name: ").strip()
            if name == "":
                print("name cannot be empty")
            elif name in menu:
                print("this item is already in the menu")
            else:
                try:
                    price = int(input("Price: Rs "))
                    if price < 1:
                        print("price should be at least 1")
                    else:
                        menu[name] = price
                        save()
                        print(name, "added")
                except ValueError:
                    print("price should be a number")

        elif ch == "2":
            name = pick_item()
            if name is not None:
                try:
                    price = int(input("New price: Rs "))
                    if price < 1:
                        print("price should be at least 1")
                    else:
                        menu[name] = price
                        save()
                        print("price changed")
                except ValueError:
                    print("price should be a number")

        elif ch == "3":
            name = pick_item()
            if name is not None:
                del menu[name]
                save()
                print(name, "removed")

        elif ch == "4":
            break
        else:
            print("invalid choice")


def report():
    print("\n------ SALES REPORT ------")
    if len(orders) == 0:
        print("no orders yet")
        return

    money = 0
    sold = {}   
    for o in orders:
        money = money + o["total"]
        for it in o["items"]:
            name = it["name"]
            if name in sold:
                sold[name] = sold[name] + it["qty"]
            else:
                sold[name] = it["qty"]

    
    best = ""
    best_count = 0
    for name in sold:
        if sold[name] > best_count:
            best = name
            best_count = sold[name]

    print("Total orders  :", len(orders))
    print("Total revenue : Rs", "%.2f" % money)
    print("Best seller   :", best, "-", best_count, "sold")
    print("\nItems sold:")
    
    for name in sorted(sold, key=sold.get, reverse=True):
        print("  " + name.ljust(20) + str(sold[name]).rjust(4))


def main():
    print("=" * 30)
    print("   WELCOME TO PYTHON CAFE")
    print("=" * 30)
    while True:
        print("\n--- MAIN MENU ---")
        print("1. Show menu")
        print("2. Take order")
        print("3. Sales report")
        print("4. Admin panel")
        print("5. Exit")
        ch = input("Choose an option: ")

        if ch == "1":
            show_menu()
        elif ch == "2":
            take_order()
        elif ch == "3":
            report()
        elif ch == "4":
            admin()
        elif ch == "5":
            print("Bye, thanks for visiting!")
            break
        else:
            print("invalid choice, try again")


main()