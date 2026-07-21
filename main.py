from db import cursor, conn


def view_customers():
    cursor.execute("SELECT * FROM Customers")
    rows = cursor.fetchall()

    print("\n----- Customers -----")
    for row in rows:
        print(row)


def add_customer():
    name = input("Enter Name: ")
    phone = input("Enter Phone: ")
    email = input("Enter Email: ")
    address = input("Enter Address: ")

    cursor.execute(
        "INSERT INTO Customers (FullName, Phone, Email, Address) VALUES (?, ?, ?, ?)",
        (name, phone, email, address)
    )

    conn.commit()
    print("Customer Added Successfully!")


def create_account():
    customer_id = int(input("Enter Customer ID: "))
    account_type = input("Enter Account Type (Savings/Current): ")
    balance = float(input("Enter Initial Balance: "))

    cursor.execute(
        "INSERT INTO Accounts (CustomerID, AccountType, Balance) VALUES (?, ?, ?)",
        (customer_id, account_type, balance)
    )

    conn.commit()
    print("Account Created Successfully!")


def deposit():
    account_id = int(input("Enter Account ID: "))
    amount = float(input("Enter Amount to Deposit: "))

    cursor.execute(
        "UPDATE Accounts SET Balance = Balance + ? WHERE AccountID = ?",
        (amount, account_id)
    )

    cursor.execute(
        "INSERT INTO Transactions (AccountID, TransactionType, Amount) VALUES (?, ?, ?)",
        (account_id, "Deposit", amount)
    )

    conn.commit()
    print("Amount Deposited Successfully!")


def withdraw():
    account_id = int(input("Enter Account ID: "))
    amount = float(input("Enter Amount to Withdraw: "))

    cursor.execute(
        "SELECT Balance FROM Accounts WHERE AccountID = ?",
        (account_id,)
    )

    row = cursor.fetchone()

    if row is None:
        print("Account not found!")
        return

    balance = row[0]

    if balance >= amount:

        cursor.execute(
            "UPDATE Accounts SET Balance = Balance - ? WHERE AccountID = ?",
            (amount, account_id)
        )

        cursor.execute(
            "INSERT INTO Transactions (AccountID, TransactionType, Amount) VALUES (?, ?, ?)",
            (account_id, "Withdraw", amount)
        )

        conn.commit()
        print("Withdrawal Successful!")

    else:
        print("Insufficient Balance!")


def check_balance():
    account_id = int(input("Enter Account ID: "))

    cursor.execute(
        "SELECT Balance FROM Accounts WHERE AccountID = ?",
        (account_id,)
    )

    row = cursor.fetchone()

    if row:
        print("Current Balance:", row[0])
    else:
        print("Account not found!")


def transaction_history():

    cursor.execute("""
        SELECT
            c.FullName,
            a.AccountID,
            t.TransactionType,
            t.Amount,
            t.TransactionDate
        FROM Customers c
        JOIN Accounts a
            ON c.CustomerID = a.CustomerID
        JOIN Transactions t
            ON a.AccountID = t.AccountID
        ORDER BY t.TransactionDate DESC
    """)

    rows = cursor.fetchall()

    print("\n----- Transaction History -----")
    for row in rows:
        print(row)


def search_customer():
    customer_id = int(input("Enter Customer ID: "))

    cursor.execute(
        "SELECT * FROM Customers WHERE CustomerID = ?",
        (customer_id,)
    )

    row = cursor.fetchone()

    if row:
        print("\nCustomer Details")
        print(row)
    else:
        print("Customer not found!")


def view_accounts():
    cursor.execute("""
        SELECT
            a.AccountID,
            c.FullName,
            a.AccountType,
            a.Balance
        FROM Accounts a
        JOIN Customers c
        ON a.CustomerID = c.CustomerID
    """)

    rows = cursor.fetchall()

    print("\n----- Accounts -----")
    for row in rows:
        print(row)


def delete_customer():
    customer_id = int(input("Enter Customer ID to Delete: "))

    cursor.execute(
        "SELECT * FROM Customers WHERE CustomerID=?",
        (customer_id,)
    )

    if cursor.fetchone() is None:
        print("Customer not found!")
        return

    cursor.execute(
        "SELECT * FROM Accounts WHERE CustomerID=?",
        (customer_id,)
    )

    if cursor.fetchone():
        print("Cannot delete. Customer has an account.")
        return

    cursor.execute(
        "DELETE FROM Customers WHERE CustomerID=?",
        (customer_id,)
    )

    conn.commit()
    print("Customer deleted successfully!")
def transfer_money():
    from_account = int(input("From Account ID: "))
    to_account = int(input("To Account ID: "))
    amount = float(input("Enter Amount: "))

    cursor.execute(
        "SELECT Balance FROM Accounts WHERE AccountID = ?",
        (from_account,)
    )

    row = cursor.fetchone()

    if row is None:
        print("Source account not found!")
        return

    balance = row[0]

    if balance < amount:
        print("Insufficient Balance!")
        return

    cursor.execute(
        "UPDATE Accounts SET Balance = Balance - ? WHERE AccountID = ?",
        (amount, from_account)
    )

    cursor.execute(
        "UPDATE Accounts SET Balance = Balance + ? WHERE AccountID = ?",
        (amount, to_account)
    )

    cursor.execute(
        "INSERT INTO Transactions (AccountID, TransactionType, Amount) VALUES (?, ?, ?)",
        (from_account, "Transfer", amount)
    )

    cursor.execute(
        "INSERT INTO Transactions (AccountID, TransactionType, Amount) VALUES (?, ?, ?)",
        (to_account, "Transfer", amount)
    )

    conn.commit()
    print("Money Transferred Successfully!")

while True:

    print("\n========== Banking Management System ==========")
    print("1. View Customers")
    print("2. Add Customer")
    print("3. Search Customer")
    print("4. Delete Customer")
    print("5. Create Account")
    print("6. View Accounts")
    print("7. Deposit Money")
    print("8. Withdraw Money")
    print("9. Check Balance")
    print("10. View Transaction History")
    print("11. Transfer Money")
    print("12. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        view_customers()

    elif choice == "2":
        add_customer()

    elif choice == "3":
        search_customer()

    elif choice == "4":
        delete_customer()

    elif choice == "5":
        create_account()

    elif choice == "6":
        view_accounts()

    elif choice == "7":
        deposit()

    elif choice == "8":
        withdraw()

    elif choice == "9":
     check_balance()

    elif choice == "10":
        transaction_history()

    elif choice == "11":
         transfer_money()

    elif choice == "12":
        conn.close()
        print("Thank you for using Banking Management System!")
        break

    else:
        print("Invalid Choice! Please try again.")