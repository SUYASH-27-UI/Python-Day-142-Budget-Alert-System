
import csv
import os
from collections import defaultdict
from datetime import datetime

FILE_NAME = "expenses.csv"


def load_expenses():
    expenses = []

    if not os.path.exists(FILE_NAME):
        print("expenses.csv not found!")
        return expenses

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                datetime.strptime(row["Date"], "%Y-%m-%d")
                amount = float(row["Amount"])

                if amount < 0:
                    continue

                expenses.append({
                    "Date": row["Date"],
                    "Category": row["Category"].strip(),
                    "Amount": amount,
                    "Description": row["Description"].strip()
                })
            except (ValueError, KeyError):
                print("Skipping invalid record:", row)

    return expenses


def save_expense(expense):
    file_exists = os.path.exists(FILE_NAME)
    needs_header = (
        not file_exists or os.path.getsize(FILE_NAME) == 0
    )

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        fields = ["Date", "Category", "Amount", "Description"]
        writer = csv.DictWriter(file, fieldnames=fields)

        if needs_header:
            writer.writeheader()

        writer.writerow(expense)


def add_expense(expenses):
    try:
        amount = float(input("Enter amount: Rs. "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Enter a valid amount.")
        return

    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    expense = {
        "Date": datetime.today().strftime("%Y-%m-%d"),
        "Category": category,
        "Amount": amount,
        "Description": description
    }

    save_expense(expense)
    expenses.append(expense)
    print("Expense saved successfully!")


def budget_report(expenses):
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format.")
        return

    try:
        budget = float(input("Enter monthly budget: Rs. "))
        if budget <= 0:
            print("Budget must be greater than zero.")
            return
    except ValueError:
        print("Enter a valid budget.")
        return

    monthly = [
        e for e in expenses
        if e["Date"].startswith(month)
    ]

    category_totals = defaultdict(float)
    total = 0

    for expense in monthly:
        category_totals[expense["Category"]] += expense["Amount"]
        total += expense["Amount"]

    print(f"\n===== BUDGET REPORT: {month} =====")
    print(f"Monthly budget: Rs. {budget:.2f}")
    print(f"Total spent: Rs. {total:.2f}")
    print(f"Remaining: Rs. {budget - total:.2f}")

    if total > budget:
        print("ALERT: Monthly budget exceeded!")
    elif total >= budget * 0.8:
        print("WARNING: You have used at least 80% of your budget.")
    else:
        print("Status: Budget is under control.")

    print("\nCategory-wise spending:")
    for category, amount in sorted(category_totals.items()):
        print(f"{category}: Rs. {amount:.2f}")


def main():
    expenses = load_expenses()

    while True:
        print("\n===== BUDGET ALERT SYSTEM =====")
        print("1. Add Expense")
        print("2. View Budget Report")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            budget_report(expenses)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
