import os
import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
import matplotlib.cm as get_cmap

def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    monthly_budget = monthly_budget_entry.get()

    if date and category and amount:
        with open("expenses.txt", "a") as file:
            file.write(f"{date},{category},{amount},{monthly_budget}\n")
        status_label.config(text="Expense added successfully!", fg="green")
        date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        monthly_budget_entry.delete(0, tk.END)
        view_expenses()
    else:
        status_label.config(text="Please fill all the fields!", fg="red")

def delete_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        date, category, amount, monthly_budget = item_text
        with open("expenses.txt", "r") as file:
            lines = file.readlines()
        with open("expenses.txt", "w") as file:
            for line in lines:
                if line.strip() != f"{date},{category},{amount},{monthly_budget}":
                    file.write(line)
        status_label.config(text="Expense deleted successfully!", fg="green")
        view_expenses()
    else:
        status_label.config(text="Please select an expense to delete!", fg="red")

def view_expenses():
  global expenses_tree
  if os.path.exists("expenses.txt"):
    total_expense = 0
    expenses_tree.delete(*expenses_tree.get_children())
    with open("expenses.txt", "r") as file:
      for line in file:
        data = line.strip().split(",")
        if len(data) == 4:
          date, category, amount, monthly_budget = data
          expenses_tree.insert("", tk.END, values=(date, category, amount, monthly_budget))
          total_expense += float(amount)

    total_label.config(text=f"Total Expense: {total_expense:.2f}")
  else:
    total_label.config(text="No expenses recorded.")
    expenses_tree.delete(*expenses_tree.get_children())

  # set background colors once
  expenses_tree.tag_configure('over_budget', background='red')
  expenses_tree.tag_configure('within_budget', background='green')  

  # Checking for color coding
  for child in expenses_tree.get_children():
    expenses_tree.item(child, tags='')  
    amount = float(expenses_tree.item(child, "values")[2])
    monthly_budget = expenses_tree.item(child, "values")[3]
    if monthly_budget:
      if amount > float(monthly_budget):
        expenses_tree.item(child, tags=('over_budget',))  
      else:
        expenses_tree.item(child, tags=('within_budget',)) 
    else:
      expenses_tree.item(child, tags='') 


def visualize_expenses_by_month():
  """
  This function reads expense data and creates visualizations to analyze expenses:
    - Bar chart showing total expenses each month.
    - Pie chart showing expenses by category.
    - Line chart for each category tracking expenses against the budget.
    - Scatter graph for each category
  """
  expenses_by_month = {}
  expenses_by_category = {}
  category_budgets = {}  

  if os.path.exists("expenses.txt"):
    with open("expenses.txt", "r") as file:
      for line in file:
        date, category, amount, monthly_budget = line.strip().split(",")
        month = date.split("-")[1]  
        expenses_by_month[month] = expenses_by_month.get(month, 0) + float(amount)
        expenses_by_category[category] = expenses_by_category.get(category, 0) + float(amount)
        category_budgets[category] = float(monthly_budget) if monthly_budget else 0 

  months = list(expenses_by_month.keys())
  expenses = list(expenses_by_month.values())
  category_expense_data = {}

  for category, amount in expenses_by_category.items():
    category_expense_data[category] = []
    for month in months:
      category_expense_data[category].append(expenses_by_month.get(month, 0) if category in expenses_by_category else 0)

  plt.figure(figsize=(14, 8)) #output screen plotting
  
  plt.subplot(2, 2, 1)
  plt.bar(months, expenses)
  plt.xlabel("Month")
  plt.ylabel("Total Expense")
  plt.title("Expenses by Month")
  plt.xticks(rotation=45)

 
  plt.subplot(2, 2, 2) 
  plt.pie(list(expenses_by_category.values()), labels=list(expenses_by_category.keys()), autopct="%1.1f%%")
  plt.title("Expenses by Category")

  
  start_col = 4  # Starting column for line charts
  for i, (category, expense_data) in enumerate(category_expense_data.items()):
    plt.subplot(2, 2, 3) 
    plt.plot(months, expense_data, label=category)
    plt.plot(months, [category_budgets[category]] * len(months), label=f"{category} Budget")  # Plot budget line
    plt.xlabel("Month")
    plt.ylabel("Expense")
    plt.title(f"Expense Trend for {category}")
    plt.legend()  

  plt.subplot(2, 2, 4)
  colors = plt.cm.get_cmap('tab20').colors  # Define a colormap for categories
  for i, (category, expense_data) in enumerate(category_expense_data.items()):
    plt.scatter(months, expense_data, label=category, c=colors[0])  
  plt.xlabel("Month")
  plt.ylabel("Expense")
  plt.title("Scatter Plot: Expense vs Month")
  plt.legend()
  
  plt.tight_layout()
  plt.show()
  
# Create the main application window
root = tk.Tk()
root.title("Expense Tracker")

# Create labels and entries for adding expenses
date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
date_label.grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

category_label = tk.Label(root, text="Category:")
category_label.grid(row=1, column=0, padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=2, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

monthly_budget_label = tk.Label(root, text="Monthly Budget:")
monthly_budget_label.grid(row=3, column=0, padx=5, pady=5)
monthly_budget_entry = tk.Entry(root)
monthly_budget_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

visualize_button = tk.Button(root, text="Visualize Expenses", command=visualize_expenses_by_month)
visualize_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)

# Create a treeview to display expenses
columns = ("Date", "Category", "Amount", "Monthly Budget")
expenses_tree = ttk.Treeview(root, columns=columns, show="headings")
expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Amount", text="Amount")
expenses_tree.heading("Monthly Budget", text="Monthly Budget")
expenses_tree.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

# Create a label to display the total expense
total_label = tk.Label(root, text="")
total_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Create a label to show the status of expense addition and deletion
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Create buttons to view and delete expenses
view_button = tk.Button(root, text="View Expenses", command=view_expenses)
view_button.grid(row=8, column=0, padx=5, pady=10)

delete_button = tk.Button(root, text="Delete Expense", command=delete_expense)
delete_button.grid(row=8, column=1, padx=5, pady=10)

# Check if the 'expenses.txt' file exists; create it if it doesn't
if not os.path.exists("expenses.txt"):
    with open("expenses.txt", "w"):
        pass

# Display existing expenses on application start
view_expenses()

root.mainloop()