def load_expenses(filename):
    try:
        with open(filename,"r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError as e:
        print(f"error:{e}")
        return[]
    



def save_expenses(filename, expenses):
    with open(filename,"w") as f:
        json.dump(expenses,f,indent=2)




from datetime import date

def add_expense(expenses):
    amt=float(input('Enter the amount '))
    category=input('Enter the category')
    note=input('Enter the note')
    today_date = date.today()

    expense = {
        "amount":amt,
        "category": category,
        "note": note,
        "date": today_date
    }

    expenses.append(expense)
    return expenses





def view_expenses(expenses):
    if len(expenses) == 0:
        print("No expenses yet!")
        return
    print("--- All Expenses ---")
    for i, expense in enumerate(expenses, 1):
        print(f"{i}. {expense['date']} | {expense['category']} | {expense['note']} | ₹{expense['amount']}")




def summarize_expenses(expenses):
    if len(expenses) == 0:
        print("No expenses yet!")
        return
    
    cateogory_wise_expense={}

    for expense in expenses:
        if expense['category'] in cateogory_wise_expense:
            cateogory_wise_expense[expense['category']] += expense['amount']
        else:
            category_wise_expense[expense['category']] = expense['amount']


    total_amt=0
    
    print("--- Summary ---")
    for categ,amt in cateogory_wise_expense.items():
        total_amt += amt    
        print(f"{categ} :  ₹{amt} ")

    print("-" * 20)
    print(f"Total : ₹{total_amt}") 





FILENAME = "expenses.json"

def main():

    expenses=load_expenses(FILENAME)

    while TRUE:
         
        print("\n=== Expense Tracker ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Summary")
        print("4. Exit")

        value = input("Enter choice: ")

        match value:
            case "1":
                expenses = add_expense(expenses)
                save_expenses(expenses)
            case "2":
                view_expenses(expenses)
            case "3":
                summarize_expenses(expenses)
            case "4":
                print("Goodbye!")
                break
            case _:
                print("Invalid choice")
            
    

main()