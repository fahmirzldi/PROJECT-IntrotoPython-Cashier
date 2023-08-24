from modul_cashier import *
from sqlalchemy import create_engine

main_menu = """
----------WELCOME TO CASHIER SYSTEM----------
COMMAND LIST
1. add_item
2. update_item_name
3. update_item_qty
4. update_item_price
5. delete_item
6. reset_transaction
7. check_order
8. check_out
9. LEAVE
"""

item_list = []

# Run program until it LEAVE command
while True:
    print(main_menu)
    command_response = input("INPUT COMMAND: ")
    print("========================================")
    print(f"COMMAND: {command_response}")

    if command_response == "add_item":
        item_list = loop_add_item(item_list)

    elif command_response in [
        "update_item_name",
        "update_item_qty",
        "update_item_price",
    ]:
        item_list = update_item(item_list, command_response)

    elif command_response == "delete_item":
        item_list = delete_item(item_list)

    elif command_response == "reset_transaction":
        item_list = reset_transaction()

    elif command_response == "check_order":
        data_upload = calculate_price_discount(item_list)

    elif command_response == "check_out":
        item_list = upload_data(item_list)

    elif command_response == "check_transaction_database":
        check_transaction_database()

    elif command_response == "LEAVE":
        break
