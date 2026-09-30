# Cafe Management System

This is my Python project for a cafe billing system. You run it in the terminal, and it does the basic work a small cafe needs: it shows the menu, takes orders, makes the bill with GST, and keeps a record of everything sold.

I picked this idea because I have seen small shops write bills by hand and add the GST on a calculator. I wanted to see how much of that I could do with a few functions and two json files.

## Running it

Just Python 3 is needed, nothing to install.

```
python cafe_management.py
```

The first screen asks what you want to do. Option 1 shows the menu, 2 takes an order, 3 shows the sales report, 4 is the admin panel and 5 closes the program.

## Taking an order

Choose 2, then type the item number and how many you want. Keep doing that for each item and type 0 when the order is done. It asks for a customer name (you can just press Enter) and then prints the bill. If you type a wrong item number or a letter instead of a quantity, it says so and asks again.

Here is a real bill from the program:

```
==========================================
                CAFE BILL
==========================================
Bill No : 1
Date    : 29-09-2026 11:43
Customer: Rahul
------------------------------------------
Item                Price  Qty    Amount
------------------------------------------
Coffee                 60    2       120
Cold Coffee            90    1        90
------------------------------------------
Subtotal                            210.00
GST (5%)                             10.50
TOTAL                               220.50
==========================================
     Thank you! Visit again :)
```

## Admin panel

Option 4 asks for a password, which is `admin123` right now. After that you can add a new item, change the price of an item or delete one. Changes are saved straight away, so the next time you open the program the new menu is already there. If you want a different password or a different GST rate, both are variables at the top of the code (`ADMIN_PASSWORD` and `GST_RATE`).

## Sales report

This goes through all the saved bills and shows the number of orders, the total money earned and which item sold the most, followed by the count for every item.

## Files

`cafe_management.py` is the whole program. `menu.json` and `orders.json` are made by the program itself, the first when you change the menu and the second when you take your first order. If you delete them the program starts fresh with the default 7 items. `statement.md` is the project statement.

## Not done yet

There is no proper window or buttons, only the terminal. The admin password sits inside the code, so anyone who opens the file can read it. It also has no discounts and no stock count. If I get time I want to try a Tkinter version and PDF bills.