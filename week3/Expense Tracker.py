import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import json

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("1000x600")  # Increase initial window size

        # Center-align columns
        self.root.columnconfigure((0, 1), weight=1)

        # Initialize expenses list
        self.expenses = []

        # Load existing expenses from file
        self.load_expenses()

        # Create expense input fields
        tk.Label(root, text="Amount:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.amount_entry = tk.Entry(root, font=("Arial", 12))
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.amount_entry.bind("<Return>", lambda event: self.category_entry.focus_set())  # Move focus to category entry on Enter

        tk.Label(root, text="Category:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.category_entry = tk.Entry(root, font=("Arial", 12))
        self.category_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.category_entry.bind("<Return>", lambda event: self.description_entry.focus_set())  # Move focus to description entry on Enter

        tk.Label(root, text="Description:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.description_entry = tk.Entry(root, font=("Arial", 12))
        self.description_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.description_entry.bind("<Return>", lambda event: self.add_expense())  # Trigger add_expense on Enter

        # Button to add expense
        self.add_expense_button = ttk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_expense_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Frame to contain the expenses display
        self.expenses_frame = tk.Frame(root)
        self.expenses_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Label to display total expense
        self.total_label = tk.Label(root, text="Total Expense: 0.00", font=("Arial", 12, "bold"))
        self.total_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Populate expenses display
        self.populate_expenses_display()

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            description = self.description_entry.get()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Validate amount
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than zero.")
                return

            # Add expense to the list
            self.expenses.append({"amount": amount, "category": category, "description": description, "date": date})

            # Clear entry fields
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)

            # Save expenses to file
            self.save_expenses()

            # Update expenses display
            self.populate_expenses_display()
            
            messagebox.showinfo("Success", "Expense added successfully.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for amount.")

    def populate_expenses_display(self):
        # Clear previous content
        for widget in self.expenses_frame.winfo_children():
            widget.destroy()

        # Create header labels
        headers = ["Amount", "Category", "Description", "Date", "Actions"]
        for col, header in enumerate(headers):
            tk.Label(self.expenses_frame, text=header, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

        # Populate expenses
        total_expense = 0
        for idx, expense in enumerate(self.expenses, start=1):
            tk.Label(self.expenses_frame, text=expense["amount"], font=("Arial", 12), anchor="center").grid(row=idx, column=0, padx=5, pady=5, sticky="nsew")
            tk.Label(self.expenses_frame, text=expense["category"], font=("Arial", 12), anchor="center").grid(row=idx, column=1, padx=5, pady=5, sticky="nsew")
            tk.Label(self.expenses_frame, text=expense["description"], font=("Arial", 12), anchor="center").grid(row=idx, column=2, padx=5, pady=5, sticky="nsew")
            tk.Label(self.expenses_frame, text=expense["date"], font=("Arial", 12), anchor="center").grid(row=idx, column=3, padx=5, pady=5, sticky="nsew")

            # Add edit and delete buttons
            edit_button = ttk.Button(self.expenses_frame, text="Edit", command=lambda i=idx-1: self.edit_expense(i))
            delete_button = ttk.Button(self.expenses_frame, text="Delete", command=lambda i=idx-1: self.delete_expense(i))
            edit_button.grid(row=idx, column=4, padx=5, pady=5, sticky="nsew")
            delete_button.grid(row=idx, column=5, padx=5, pady=5, sticky="nsew")

            total_expense += expense["amount"]

        # Update total expense label
        self.total_label.config(text=f"Total Expense: {total_expense:.2f}")

    def save_expenses(self):
        with open("expenses.json", "w") as f:
            json.dump(self.expenses, f)

    def load_expenses(self):
        try:
            with open("expenses.json", "r") as f:
                self.expenses = json.load(f)
        except FileNotFoundError:
            # If file does not exist, initialize expenses list
            self.expenses = []

    def edit_expense(self, index):
        expense_data = self.expenses[index]
        # Open edit expense window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Expense")
        EditExpenseWindow(edit_window, expense_data, lambda data: self.update_expense(index, data))

    def update_expense(self, index, data):
        self.expenses[index] = data
        self.save_expenses()
        self.populate_expenses_display()

    def delete_expense(self, index):
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this expense?")
        if confirmation:
            del self.expenses[index]
            self.save_expenses()
            self.populate_expenses_display()
            messagebox.showinfo("Success", "Expense deleted successfully.")

class EditExpenseWindow:
    def __init__(self, root, expense_data, callback):
        self.root = root
        self.expense_data = expense_data
        self.callback = callback

        # Create expense input fields
        tk.Label(root, text="Amount:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.amount_entry = tk.Entry(root, font=("Arial", 12))
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.amount_entry.insert(0, str(expense_data["amount"]))
        self.amount_entry.bind("<Return>", lambda event: self.category_entry.focus_set())  # Move focus to category entry on Enter

        tk.Label(root, text="Category:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.category_entry = tk.Entry(root, font=("Arial", 12))
        self.category_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.category_entry.insert(0, expense_data["category"])
        self.category_entry.bind("<Return>", lambda event: self.description_entry.focus_set())  # Move focus to description entry on Enter

        tk.Label(root, text="Description:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.description_entry = tk.Entry(root, font=("Arial", 12))
        self.description_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.description_entry.insert(0, expense_data["description"])
        self.description_entry.bind("<Return>", lambda event: self.save_edited_expense())  # Trigger save_edited_expense on Enter

        # Button to save edited expense
        self.save_button = ttk.Button(root, text="Save", command=self.save_edited_expense)
        self.save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def save_edited_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            description = self.description_entry.get()

            # Update expense data
            self.expense_data["amount"] = amount
            self.expense_data["category"] = category
            self.expense_data["description"] = description

            # Call callback function to update expense in main application
            self.callback(self.expense_data)

            messagebox.showinfo("Success", "Expense edited successfully.")
            self.root.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input for amount.")

def main():
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    # Center the window on the screen
    root.eval('tk::PlaceWindow . center')
    root.mainloop()

if __name__ == "__main__":
    main()
