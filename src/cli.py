import argparse
from datetime import date

from src.core import Expense, Income, Category, FormatType
from src.utils import print_categories_tree, balance_month, balance_year

VERSION = "1.0.3"

parser = argparse.ArgumentParser(description="Expenses manager")
top_level_subparsers = parser.add_subparsers(dest="item", required=True, help="Available commands")
# 'version' command
version_parser = top_level_subparsers.add_parser("version", help="Show version")
# 'exp' command
exp_parser = top_level_subparsers.add_parser("exp", help="Manage expense records")
exp_subparser = exp_parser.add_subparsers(dest="exp_command", required=True, help="Expense(s) manager command")
# 'exp' -> 'list'
exp_list_parser = exp_subparser.add_parser("list", help="List last expenses")
exp_list_parser.add_argument("-n", "--number", type=int, default=20, help="Number of last items to be shown (default: 20)")
exp_list_parser.add_argument("-c", "--category", type=int, default=-1, help="Filter expenses for a specific category ID. -1 means no filter. (default: -1)") # todo
# 'exp' -> 'add'
add_parser = exp_subparser.add_parser("add", help="Add expense")
add_parser.add_argument("-a", "--amount", required=True, type=float, default=0.0, help="Amount of the expense (required)")
add_parser.add_argument("-c", "--category", required=True, type=int, help="ID of the category for the expense (required)")
add_parser.add_argument("-d", "--date", type=str, default="", help="Date of the expense in yyyy-mm-dd format. If not specified, today date is used.")
add_parser.add_argument("-t", "--title", type=str, default="", help="Title of the expense")
add_parser.add_argument("-n", "--notes", type=str, default="", help="Notes for the expense")

# 'inc' command
inc_parser = top_level_subparsers.add_parser("inc", help="Manage income records")
inc_subparser = inc_parser.add_subparsers(dest="inc_command", required=True, help="income(s) manager command")
# 'inc' -> 'list'
inc_list_parser = inc_subparser.add_parser("list", help="List last incomes")
inc_list_parser.add_argument("-n", "--number", type=int, default=20, help="Number of last items to be shown (default: 20)")
inc_list_parser.add_argument("-c", "--category", type=int, default=-1, help="Filter incomes for a specific category ID. -1 means no filter. (default: -1)") # todo
# 'inc' -> 'add'
add_parser = inc_subparser.add_parser("add", help="Add income")
add_parser.add_argument("-a", "--amount", required=True, type=float, default=0.0, help="Amount of the income")
add_parser.add_argument("-d", "--date", type=str, default="", help="Date of the income in yyyy-mm-dd format. If not specified, today date is used.")
add_parser.add_argument("-t", "--title", type=str, default="", help="Title of the income")
add_parser.add_argument("-c", "--category", type=int, default=0, help="ID of the category for the income")
add_parser.add_argument("-n", "--notes", type=str, default="", help="Notes for the income")

# 'cat' command
cat_parser = top_level_subparsers.add_parser("cat", help="Manage category records")
cat_subparser = cat_parser.add_subparsers(dest="cat_command", required=True, help="Category manager command")
# 'cat' -> 'list'
cat_list_parser = cat_subparser.add_parser("list", help="List categories")
# 'cat' -> 'tree'
cat_tree_parser = cat_subparser.add_parser("tree", help="Show categories as a hierarchical tree")

# 'balance' command # todo
balance_parser = top_level_subparsers.add_parser("balance", help="Print balance statistics")
balance_subparser = balance_parser.add_subparsers(dest="balance_command", required=True, help="Balance command")
# 'balance' -> 'month' # todo
balance_month_parser = balance_subparser.add_parser("month", help="Monthly balance")
balance_month_parser.add_argument("-m", "--month", type=int, default=0, help="Month to be analyzed relative to the current month (0: current month, -1: previous month...)")
# 'balance' -> 'year' # todo
balance_year_parser = balance_subparser.add_parser("year", help="Yearly balance")
balance_year_parser.add_argument("-y", "--year", type=int, default=0, help="Year to be analyzed relative to the current year (0: current year, -1: previous year...)")

def main_function():
    args = parser.parse_args()

    if args.item == "version":
        print(f"EXPMAN version {VERSION}")
    elif args.item == "exp":
        if args.exp_command == "add":
            # add expense
            exp_date = date.today()
            if (args.date is not None) and (args.date != ""):
                exp_date = args.date
            else:
                pass
            expense = Expense(args.category, exp_date, args.amount, args.title, args.notes)
            #expense.Create()
            expense.Add()
            print(f"Expense added to the database")
        elif args.exp_command == "list":
            # list expenses
            tExp = Expense.FetchNumber(abs(args.number))
            for exp in tExp:
                print(exp.to_string())
    elif args.item == "inc":
        if args.inc_command == "add":
            # add income
            inc_date = date.today()
            if (args.date is not None) and (args.date != ""):
                inc_date = args.date
                # todo: add date validation
            income = Income(args.category, inc_date, args.amount, args.title, args.notes)
            #income.Create()
            income.Add()
            print(f"Income added to the database")
        elif args.inc_command == "list":
            # list all incomes
            tInc = Income.FetchNumber(abs(args.number))
            for inc in tInc:
                print(inc.to_string())
    elif args.item == "cat":
        if args.cat_command == "list":
            # list categories
            tCat = Category.FetchAll()
            print(Category.get_list_header())
            for cat in tCat:
                print(cat.to_string(FormatType.LIST))
        elif args.cat_command == "tree":
            tCat = Category.FetchAll()
            print_categories_tree(tCat, 0, 0, 10)
    elif args.item == "balance":
        if args.balance_command == "month":
            balance_month(args.month)
        elif args.balance_command == "year":
            balance_year(args.year)