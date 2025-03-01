from datetime import date
from dateutil.relativedelta import relativedelta
import calendar
from typing import Tuple
from src.core import Expense, Income, Category, FormatType

def print_categories_tree(lCat:Tuple[Category], parentId:int, depth:int, maxDepth:int):
    if maxDepth > depth:
        lCat_parent = [cat for cat in lCat if (cat.parent == parentId)]
        for cat in lCat_parent:
            tab_char = '\t'
            print(f"{tab_char*depth}" + cat.to_string(FormatType.TREE))
            print_categories_tree(lCat, cat.id, depth+1, maxDepth)
    else:
        pass

def balance(date_from:date, date_to:date):
    """Print balance for the indicated time interval"""
    # 1. extract all expenses for the date interval
    tExp = Expense.FetchDateInterval(date_from, date_to)
    # 2. extract all incomes for the date interval
    tInc = Income.FetchDateInterval(date_from, date_to)
    # 3. sum all the expenses
    exp_sum = 0
    for exp in tExp:
        exp_sum += float(exp.amount)
    # 4. sum all the incomes
    inc_sum = 0
    for inc in tInc:
        inc_sum += float(inc.amount)
    print(f"From {date_from} to {date_to}")
    print(f"Incomes: {inc_sum:.2f}")
    print(f"Expenses: {exp_sum:.2f}")
    print(f"Balance: {(inc_sum - exp_sum):.2f}")

def balance_month(relative_month:int):
    """Print balance for the requested relative month"""
    # 1. calculate date_from and date_to
    today = date.today()
    relative_month = abs(relative_month)
    shifted_date = today - relativedelta(months=relative_month)
    date_from = shifted_date.replace(day=1)
    last_day_of_month = calendar.monthrange(shifted_date.year, shifted_date.month)[1]
    date_to = shifted_date.replace(day=last_day_of_month)
    # 2. extract and print balance
    balance(date_from, date_to)

def balance_year(relative_year:int):
    """Print balance for the requested relative year"""
    # 1. Date from is January 1st of requested year. Date to is today
    date_today = date.today()
    if 0 == relative_year:
        # current year requested
        date_to = date_today
        date_from = date_today.replace(day=1, month=1)
    else:
        # previous year requested
        year = date_today.year
        year -= abs(relative_year)
        date_from = date(year=year, month=1, day=1)
        date_to = date(year=year, month=12, day=31)
    # 2. extract balance
    balance(date_from, date_to)