from tabulate import tabulate
from sqlalchemy import create_engine
from sqlalchemy import text


def add_item():
    """
    Prompt the user to enter details of an item and return a list containing the item information.

    Returns:
        list: List containing the item name, item amount, and price per item.
    """
    item_name = input("Item name: ")

    # Check if item_name is more than 0 or int
    while True:
        try:
            item_amount = int(input(f"Amount of {item_name}: "))
            if item_amount > 0:
                break
            else:
                print("Amount must be > 0")
        except ValueError:
            print("Amount has to be NUMBER")

    while True:
        try:
            price = int(input(f"Price per {item_name}: "))
            if price > 0:
                break
            else:
                print("Price must be > 0")
        except ValueError:
            print("Price has to be NUMBER")

    new_item = [item_name, item_amount, price]

    return new_item


def loop_add_item(item_list) -> None:
    """
    Prompt the user to input the number of product types, and then repeatedly call add_item()
    to add items to the item_list.

    Args:
        item_list (list): List to store the item information.

    Returns:
        list: Updated item_list with the added items.

    """

    # Check if item_name is more than 0 or int
    while True:
        try:
            product_amount = int(input("Amount of Product Type: "))
            if product_amount > 0:
                break
            else:
                print("Amount must be > 0")
        except ValueError:
            print("Wrong input. Please input amount in number 1 until n")

    # run add_item() based on product_amount()
    for item_order in range(product_amount):
        print(f"""\nInput item number {item_order+1}""")
        item = add_item()
        item_list.append(item)

    print("\nItem List")
    print(tabulate(item_list, headers=["item_name", "item_amount", "price"]))

    return item_list


def check_availability(item_name, list_data):
    """
    Check the availability of a specific data in a list of lists.

    Args:
        item_name: item_name to be checked for availability.
        list_data: List of lists to search for the data.

    Returns:
        str: "available" if the data is found in the list_data, otherwise "not available".
    """
    for item in list_data:
        if item[0] == item_name:
            return "available"
    return "not available"


def replace_data(updated_item_name, new_data, item_list, updated_data_type):
    """
    Replace the data of a specific item in a list of lists with the provided new data based on item_name.

    Args:
        updated_item_name: item_name data to be updated.
        new_data: New data to replace the existing data.
        item_list: List of lists containing the items and their data.
        updated_data_type: Type of data to be updated ("name", "qty", or "price").

    Returns:
        list: Updated item_list after replacing the data.

    Raises:
        ValueError: If an invalid updated_data_type (other than "name", "qty", or "price") is provided.
    """

    # Determine which column based on updated_data_type
    if updated_data_type == "name":
        kolom = 0
    elif updated_data_type == "qty":
        kolom = 1
    elif updated_data_type == "price":
        kolom = 2

    # Check the item_name to find the row, and based on the column replace the data with new_data
    for baris, item in enumerate(item_list):
        if item[0] == updated_item_name:
            item_list[baris][kolom] = new_data
            return item_list


def update_item(item_list, command_response):
    """
    Update the data of items in the item_list based on the specified command_response.

    Args:
        item_list: List of lists containing the items and their data.
        command_response: Command response specifying the type of data to be updated.

    Returns:
        list: Updated item_list after applying the requested updates.
    """
    while True:
        print("\nItem List")
        print(tabulate(item_list, headers=["item_name", "item_amount", "price"]))

        # Determine which update_type based on command response
        if command_response == "update_item_name":
            update_type = "name"
        elif command_response == "update_item_qty":
            update_type = "qty"
        elif command_response == "update_item_price":
            update_type = "price"

        # Recheck if any/more data need to be updated
        response_update_item = input(
            f"Is there any {update_type} that need updated (y/n)? "
        )

        if response_update_item == "y":
            # update item_list based on update_type using replace_data() by first check item availability in the list using check_availability()
            while True:
                updated_item_name = input(f"Item Name: ")

                item_availability = check_availability(updated_item_name, item_list)

                if item_availability == "not available":
                    print("Item not available. Only input item available in the list")

                else:
                    new_data = input(f"Put new {update_type} of {updated_item_name}: ")
                    item_list = replace_data(
                        updated_item_name, new_data, item_list, update_type
                    )
                    break

        elif response_update_item == "n":
            break

    return item_list


def delete_item(item_list):
    """
    Delete an item from the item_list.

    Args:
        item_list: List of lists containing the items and their data.

    Returns:
        list: Updated item_list after deleting the specified item.
    """

    # Ask for input than delete if data is available in the list
    while True:
        print(tabulate(item_list, headers=["item_name", "item_amount", "price"]))
        item_deleted = input(f"Item name to be Deleted: ")

        item_availability = check_availability(item_deleted, item_list)

        if item_availability == "not available":
            print("Item not available. Only input item available in the list")

        else:
            item_list = [
                row for row in item_list if row[0] != item_deleted
            ]  # Only return row where the first column did not match the item_deleted
            print("\nItem List")
            print(tabulate(item_list, headers=["item_name", "item_amount", "price"]))
            break

    return item_list


def reset_transaction():
    """
    Reset the transaction by deleting all items in the item_list.

    Returns:
        list: Empty item_list after resetting the transaction.
    """
    recheck_reset = input("Confirmation to DELETE ALL item in the list (y/n)? ")

    if recheck_reset == "y":
        item_list = []
        print("All List Deleted")
        print("\nItem List")
        print(tabulate(item_list, headers=["item_name", "item_amount", "price"]))

    elif recheck_reset == "n":
        pass

    return item_list


def calculate_price_discount(item_list):
    """
    Calculate and create column of the total price, discount, and discounted price for each item in the item_list.

    Args:
        item_list (list): List of items containing item_name, item_amount, and price.

    Returns:
        list: List of items with additional columns: total_price, discount, and discounted_price.
    """
    data_upload = []

    for row in item_list:
        item_name, quantity, price_per_item = row

        total_price = quantity * price_per_item

        if total_price >= 500000:
            discount = 0.07
        elif total_price >= 300000:
            discount = 0.06
        elif total_price >= 200000:
            discount = 0.05
        else:
            discount = 0

        discounted_price = int(total_price - (total_price * discount))

        updated_row = row + [total_price, discount, discounted_price]
        data_upload.append(updated_row)

    print(
        tabulate(
            data_upload,
            headers=[
                "item_name",
                "item_amount",
                "price",
                "total_price",
                "discount",
                "discounted_price",
            ],
        )
    )
    return data_upload


def upload_data(item_list):
    """
    Upload the transaction data to the database and generate a receipt.

    Args:
        item_list (list): List of items containing item_name, item_amount, and price.

    Returns:
        list: Empty list (item_list).
    """
    data_upload = calculate_price_discount(item_list)

    # Open SQLLite connection
    engine = create_engine("sqlite:///cashierproject.db")

    conn = engine.connect()

    query_createtable = text(
        """
    CREATE TABLE IF NOT EXISTS cashier_transaction (
        no_id INTEGER PRIMARY KEY AUTOINCREMENT,
        no_trans INTEGER SECONDARY KEY,
        item_name TEXT,
        item_amount INTEGER,
        price INTEGER,
        total_price INTEGER,
        discount INTEGER,
        discounted_price INTEGER
    )
    """
    )

    conn.execute(query_createtable)

    # Query to get max_notrans
    query_notrans = text(
        """
    SELECT Max(no_trans)
    FROM cashier_transaction
    """
    )

    max_notrans = conn.execute(query_notrans).fetchone()
    max_notrans = int(max_notrans[0] if max_notrans[0] is not None else 0)

    # Add New Column max_notrans
    data_upload = [[max_notrans + 1] + row for row in data_upload]

    # Query to upload new transaction data
    query_upload = text(
        """
    INSERT INTO cashier_transaction (no_trans, item_name, item_amount, price, total_price, discount, discounted_price)
    VALUES (:no_trans, :item_name, :item_amount, :price, :total_price, :discount, :discounted_price)
    """
    )

    parameters = [
        {
            "no_trans": row[0],
            "item_name": row[1],
            "item_amount": row[2],
            "price": row[3],
            "total_price": row[4],
            "discount": row[5],
            "discounted_price": row[6],
        }
        for row in data_upload
    ]

    conn.execute(query_upload, parameters)

    total_amount = sum(row[-1] for row in data_upload)

    print(f"This is your receipt. Total Amount is Rp {total_amount}")

    item_list = (
        []
    )  # Need to be emptied to make sure that no duplicated data uploaded in the next customer

    conn.commit()

    conn.close()

    return item_list


def check_transaction_database():
    """
    Retrieve and display all transaction data from the database.

    Returns:
        None
    """

    # Open SQLLite connection
    engine = create_engine("sqlite:///cashierproject.db")

    conn = engine.connect()

    # Query all database
    query_all_database = text(
        """
        SELECT * 
        FROM cashier_transaction
    """
    )

    result = conn.execute(query_all_database)

    print(
        tabulate(
            result,
            headers=[
                "no_id",
                "no_trans",
                "item_name",
                "item_amount",
                "price",
                "total_price",
                "discount",
                "discounted_price",
            ],
        )
    )

    conn.close()
