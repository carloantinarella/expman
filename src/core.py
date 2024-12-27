
import os
import sqlite3
from datetime import date
from typing import List, Tuple
from enum import Enum

VERSION = "0.0.1"

DB_FOLDER = "db"
DB_NAME = "expman_db.db"

TABLE_NAME_CATEGORIES = "CATEGORIES"
TABLE_NAME_EXPENSES = "EXPENSES"
TABLE_NAME_INCOMES = "INCOMES"

COLUMN_NAME_ALL_ID = "ID"
COLUMN_NAME_ALL_DATE = "DATETIME"

COLUMN_NAME_CATEGORY_ID = "ID"
COLUMN_NAME_CATEGORY_PARENT = "PARENT"
COLUMN_NAME_CATEGORY_TITLE = "TITLE"
COLUMN_NAME_CATEGORY_DESCRIPTION = "DESCRIPTION"

COLUMN_NAME_EXPENSE_ID = "ID"
COLUMN_NAME_EXPENSE_CATEGORY = "CATEGORY"
COLUMN_NAME_EXPENSE_DATE = "DATETIME"
COLUMN_NAME_EXPENSE_AMOUNT = "AMOUNT"
COLUMN_NAME_EXPENSE_TITLE = "TITLE"
COLUMN_NAME_EXPENSE_NOTES = "NOTES"

COLUMN_NAME_INCOME_ID = "ID"
COLUMN_NAME_INCOME_CATEGORY = "CATEGORY"
COLUMN_NAME_INCOME_DATE = "DATETIME"
COLUMN_NAME_INCOME_AMOUNT = "AMOUNT"
COLUMN_NAME_INCOME_TITLE = "TITLE"
COLUMN_NAME_INCOME_NOTES = "NOTES"

COLUMN_ATTRIBUTES_CATEGORY_ID = "INTEGER NOT NULL"
COLUMN_ATTRIBUTES_CATEGORY_PARENT = "INTEGER NOT NULL"
COLUMN_ATTRIBUTES_CATEGORY_TITLE = "TEXT NOT NULL"
COLUMN_ATTRIBUTES_CATEGORY_DESCRIPTION = "TEXT"

COLUMN_ATTRIBUTES_EXPENSE_ID = "INTEGER NOT NULL"
COLUMN_ATTRIBUTES_EXPENSE_CATEGORY = "INTEGER NOT NULL"
COLUMN_ATTRIBUTES_EXPENSE_DATE = "TEXT NOT NULL"
COLUMN_ATTRIBUTES_EXPENSE_AMOUNT = "REAL NOT NULL"
COLUMN_ATTRIBUTES_EXPENSE_TITLE = "TEXT"
COLUMN_ATTRIBUTES_EXPENSE_NOTES = "TEXT"

COLUMN_ATTRIBUTES_INCOME_ID = "INTEGER NOT NULL"
COLUMN_ATTRIBUTES_INCOME_CATEGORY = "INTEGER NOT NULL"
COLUMN_ATTRIBUTES_INCOME_DATE = "TEXT NOT NULL"
COLUMN_ATTRIBUTES_INCOME_AMOUNT = "REAL NOT NULL"
COLUMN_ATTRIBUTES_INCOME_TITLE = "TEXT"
COLUMN_ATTRIBUTES_INCOME_NOTES = "TEXT"


class FormatType(Enum):
    LIST = 1
    TREE = 2

class TableColumn:
    def __init__(self, name:str, typ:type, attributes:str):
        self._name = name
        self._typ = typ
        self._attributes = attributes
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def typ(self) -> type:
        return self._typ
    
    @property
    def attributes(self) -> str:
        return self._attributes
    
    @name.setter
    def name(self, value:str):
        self._name = value

    @typ.setter
    def typ(self, value:type):
        self._typ = value
    
    @attributes.setter
    def attributes(self, value:str):
        self._attributes = value

class DBTable:
    def __init__(self, name:str, columns:Tuple[TableColumn]):
        self._name = name
        self._columns = columns
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def columns(self) -> Tuple[TableColumn]:
        return self._columns
    
    @name.setter
    def name(self, value:str):
        self._name = value

def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

@singleton
class DB:
    def __init__(self):
        self.tables = {
            TABLE_NAME_CATEGORIES: DBTable(TABLE_NAME_CATEGORIES, (TableColumn(COLUMN_NAME_CATEGORY_ID, int, COLUMN_ATTRIBUTES_CATEGORY_ID),
                                                                   TableColumn(COLUMN_NAME_CATEGORY_PARENT, int, COLUMN_ATTRIBUTES_CATEGORY_PARENT),
                                                                   TableColumn(COLUMN_NAME_CATEGORY_TITLE, str, COLUMN_ATTRIBUTES_CATEGORY_TITLE),
                                                                   TableColumn(COLUMN_NAME_CATEGORY_DESCRIPTION, str, COLUMN_ATTRIBUTES_CATEGORY_DESCRIPTION)
            )),
            TABLE_NAME_EXPENSES: DBTable(TABLE_NAME_EXPENSES, (TableColumn(COLUMN_NAME_EXPENSE_ID, int, COLUMN_ATTRIBUTES_EXPENSE_ID),
                                                               TableColumn(COLUMN_NAME_EXPENSE_CATEGORY, int, COLUMN_ATTRIBUTES_EXPENSE_CATEGORY),
                                                               TableColumn(COLUMN_NAME_EXPENSE_AMOUNT, float, COLUMN_ATTRIBUTES_EXPENSE_AMOUNT),
                                                               TableColumn(COLUMN_NAME_EXPENSE_DATE, str, COLUMN_ATTRIBUTES_EXPENSE_DATE),
                                                               TableColumn(COLUMN_NAME_EXPENSE_TITLE, str, COLUMN_ATTRIBUTES_EXPENSE_TITLE),
                                                               TableColumn(COLUMN_NAME_EXPENSE_NOTES, str, COLUMN_ATTRIBUTES_EXPENSE_NOTES),
            )),
            TABLE_NAME_INCOMES: DBTable(TABLE_NAME_INCOMES, (TableColumn(COLUMN_NAME_INCOME_ID, int, COLUMN_ATTRIBUTES_INCOME_ID),
                                                             TableColumn(COLUMN_NAME_INCOME_CATEGORY, int, COLUMN_ATTRIBUTES_INCOME_CATEGORY),
                                                             TableColumn(COLUMN_NAME_INCOME_AMOUNT, float, COLUMN_ATTRIBUTES_INCOME_AMOUNT),
                                                             TableColumn(COLUMN_NAME_INCOME_DATE, str, COLUMN_ATTRIBUTES_INCOME_DATE),
                                                             TableColumn(COLUMN_NAME_INCOME_TITLE, str, COLUMN_ATTRIBUTES_INCOME_TITLE),
                                                             TableColumn(COLUMN_NAME_INCOME_NOTES, str, COLUMN_ATTRIBUTES_INCOME_NOTES),
            )),
        }
        # Create db file if not existing
        if not os.path.exists(DB_FOLDER):
            os.makedirs(DB_FOLDER)
        if not os.path.isfile(os.path.join(DB_FOLDER, DB_NAME)):
            print("Database not found. Creating a new one...")
            # Connect attempt creates file automatically
            self._connect()
            # Database shall be initialized with all the tables
            for table_name, table_value in self.tables.items():
                query = f"CREATE TABLE IF NOT EXISTS \"{table_name}\" (\n"
                table_columns = table_value.columns
                for table_column in table_columns:
                    query += f"\"{table_column.name}\" {table_column.attributes},\n"
                query += f"PRIMARY KEY(\"{COLUMN_NAME_ALL_ID}\" AUTOINCREMENT)\n"
                query += ");"
                cursor = self._conn.cursor()
                print(query)
                cursor.execute(query)
            self._conn.commit()
            self._close()

    def _connect(self):
        self._conn = sqlite3.connect(os.path.join(DB_FOLDER,DB_NAME))
    
    def _close(self):
        self._conn.close()
    
    def getColumnsAsStrings(self, table_name: str) -> Tuple[str]:
        if table_name in self.tables:
            db_table = self.tables[table_name]
            column_strings = []
            for column_obj in db_table.columns:
                column_strings.append(column_obj.name)
            return tuple(column_strings)
        else:
            raise ValueError(f"Unknown table {table_name}")

    def Create(self, table_name: str, columns: List[str], values: List[str]):
        try:
            if len(columns) != len(values):
                #todo: throw error
                pass
            self._connect()
            serialized_columns = ', '.join(columns)
            serialized_values = ', '.join(f"'{value}'" for value in values)
            query = f"INSERT INTO {table_name} ({serialized_columns}) VALUES ({serialized_values})"
            cursor = self._conn.cursor()
            cursor.execute(query)
            self._conn.commit()
            self._close()

        except sqlite3.Error as e:
            print(f"Error: {e}")

        finally:
            pass
    
    def FetchAll(self, table_name: str) -> List[dict]:
        try:
            self._connect()
            columns_tuple = self.getColumnsAsStrings(table_name)
            serialized_columns = ", ".join(columns_tuple)
            query = f"SELECT {serialized_columns} FROM {table_name}"
            cursor = self._conn.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            self._close()
            # transform into a list of dictionaries where each key has the column name
            records_dicts = []
            for record_tuple in records:
                record_dict = dict()
                i = 0
                for column in columns_tuple:
                    record_dict[column] = record_tuple[i]
                    i += 1
                records_dicts.append(record_dict)
            return records_dicts

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return []

        finally:
            pass
    
    def FetchDate(self, table_name:str, date_from: str, date_to: str) -> List[dict]:
        """Return items from a specific DB table within from_date and to_date"""
        try:
            self._connect()
            columns_tuple = self.getColumnsAsStrings(table_name)
            serialized_columns = ", ".join(columns_tuple)
            query = f"SELECT {serialized_columns} FROM {table_name} WHERE {COLUMN_NAME_ALL_DATE} BETWEEN '{date_from}' AND '{date_to}'"
            cursor = self._conn.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            self._close()
            # transform into a list of dictionaries where each key has the column name
            records_dicts = []
            for record_tuple in records:
                record_dict = dict()
                i = 0
                for column in columns_tuple:
                    record_dict[column] = record_tuple[i]
                    i += 1
                records_dicts.append(record_dict)
            return records_dicts

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return []

        finally:
            pass

class Item:
    def __init__(self, table:str, id=0):
        self._id = id
        self._table = table
        self._query_dict = dict()
        #self._query_dict[COMMON_COL["ID"]: self._id]
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def table_name(self) ->str:
        return self._table
    
    def add_dict_element(self, column:str, data: str):
        self._query_dict[column] = data

class Category(Item):
    def get_list_header():
        return f"{' '*(5-len('ID'))}ID | {' '*(10-len('PARENT'))}PARENT | TITLE {' '*(20-len('TITLE'))}| DESCRIPTION {' '*(50-len('DESCRIPTION'))}"
        #pass

    def __init__(self, parent: int, title: str, description: str, id=0):
        super().__init__(TABLE_NAME_CATEGORIES, id)
        self._parent = parent
        self._title = title
        self._description = description

    @property
    def parent(self) -> int:
        return self._parent
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def description(self) -> str:
        return self._description
    
    @parent.setter
    def parent(self, value):
        self._parent = value
    
    @title.setter
    def title(self, value):
        self._title = value
    
    @description.setter
    def description(self, value):
        self._description = value
    
    def to_string(self, format:FormatType=FormatType.LIST) -> str:
        if format == FormatType.LIST:
            return f"{self.id:5} | {self.parent:10} | {self.title:<20} | {self.description:<50}"
        elif format == FormatType.TREE:
            return f"{self.id} | {self.title} ({self.description})"
        else:
            return ""
    
    @staticmethod
    def FetchAll():
        """Fetch all categories from database and return a tuple of objects"""
        db = DB()
        category_dict_list = db.FetchAll(TABLE_NAME_CATEGORIES)
        category_list = []
        for category_dict in category_dict_list:
            category_list.append(Category(category_dict[COLUMN_NAME_CATEGORY_PARENT], 
                                            category_dict[COLUMN_NAME_CATEGORY_TITLE], 
                                            category_dict[COLUMN_NAME_CATEGORY_DESCRIPTION],
                                            category_dict[COLUMN_NAME_CATEGORY_ID]))
        return tuple(category_list)

    
class TransactionItem(Item):
    def __init__(self, table: str, category_id: int, date: str, amount: float, title: str, notes: str, id=0):
        if (TABLE_NAME_EXPENSES != table) and (TABLE_NAME_INCOMES != table):
            raise ValueError(f"Table {table} not recognized")
        super().__init__(table, id)
        self._category_id = category_id
        self._date = date
        self._amount = amount
        self._title = title
        self._notes = notes
        self._table = table
    
    @property
    def category_id(self) -> int:
        return self._category_id
    
    @property
    def date(self) -> date:
        return self._date
    
    @property
    def amount(self) -> float:
        return self._amount
    
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def notes(self) -> str:
        return self._notes

    @category_id.setter
    def category_id(self, value: int):
        self._category_id = value
    
    @date.setter
    def date(self, value: date):
        self.date = value

    @amount.setter
    def amount(self, value: float):
        self.amount = value

    @title.setter
    def title(self, value: str):
        self.title = value

    @notes.setter
    def notes(self, value: str):
        self.notes = value
    
    def to_string(self):
        return f"{self.id:5} | {self.category_id:5} | {self.amount:8} | {self.date:12} | {self.title:20} | {self.notes}"

class Expense(TransactionItem):
    table_name = TABLE_NAME_EXPENSES

    def __init__(self, category_id: int, date: date, amount: float, title: str, notes: str, id=0):
        super().__init__(TABLE_NAME_EXPENSES, category_id, date, amount, title, notes, id=0)
    
    def Add(self):
        self.add_dict_element(COLUMN_NAME_EXPENSE_CATEGORY, str(self.category_id))
        self.add_dict_element(COLUMN_NAME_EXPENSE_DATE,     self.date)
        self.add_dict_element(COLUMN_NAME_EXPENSE_AMOUNT,   str(self.amount))
        self.add_dict_element(COLUMN_NAME_EXPENSE_TITLE,    self.title)
        self.add_dict_element(COLUMN_NAME_EXPENSE_NOTES,    self.notes)
        db = DB()
        db.Create(Expense.table_name, self._query_dict.keys(), self._query_dict.values())
    
    @staticmethod
    def _from_dict_to_tuple(expense_dict_list):
        expense_list = []
        for expense_dict in expense_dict_list:
            expense_list.append(Expense(    category_id =   expense_dict[COLUMN_NAME_EXPENSE_CATEGORY], 
                                            date =          expense_dict[COLUMN_NAME_EXPENSE_DATE], 
                                            amount =        expense_dict[COLUMN_NAME_EXPENSE_AMOUNT],
                                            title =         expense_dict[COLUMN_NAME_EXPENSE_TITLE],
                                            notes =         expense_dict[COLUMN_NAME_EXPENSE_NOTES],
                                            id =            expense_dict[COLUMN_NAME_EXPENSE_ID]))
        return tuple(expense_list)

    @staticmethod
    def FetchAll():
        """Fetch all expenses items from database and return a tuple of objects"""
        db = DB()
        expense_dict_list = db.FetchAll(Expense.table_name)
        return Expense._from_dict_to_tuple(expense_dict_list)

    @staticmethod
    def FetchDateInterval(date_from:str, date_to:str):
        """Fetch all expenses between a date interval"""
        db = DB()
        expense_dict_list = db.FetchDate(Expense.table_name, date_from, date_to)
        return Expense._from_dict_to_tuple(expense_dict_list)

class Income(TransactionItem):
    table_name = TABLE_NAME_INCOMES

    def __init__(self, category_id: int, date: date, amount: float, title: str, notes: str, id=0):
        super().__init__(TABLE_NAME_INCOMES, category_id, date, amount, title, notes, id=0)

    def Add(self):
        self.add_dict_element(COLUMN_NAME_INCOME_CATEGORY, str(self.category_id))
        self.add_dict_element(COLUMN_NAME_INCOME_DATE,     self.date)
        self.add_dict_element(COLUMN_NAME_INCOME_AMOUNT,   str(self.amount))
        self.add_dict_element(COLUMN_NAME_INCOME_TITLE,    self.title)
        self.add_dict_element(COLUMN_NAME_INCOME_NOTES,    self.notes)
        db = DB()
        db.Create(Income.table_name, self._query_dict.keys(), self._query_dict.values())
    
    @staticmethod
    def _from_dict_to_tuple(income_dict_list):
        income_list = []
        for income_dict in income_dict_list:
            income_list.append(Income(  category_id =   income_dict[COLUMN_NAME_INCOME_CATEGORY], 
                                        date =          income_dict[COLUMN_NAME_INCOME_DATE], 
                                        amount =        income_dict[COLUMN_NAME_INCOME_AMOUNT],
                                        title =         income_dict[COLUMN_NAME_INCOME_TITLE],
                                        notes =         income_dict[COLUMN_NAME_INCOME_NOTES],
                                        id =            income_dict[COLUMN_NAME_INCOME_ID]))
        return tuple(income_list)

    @staticmethod
    def FetchAll():
        """Fetch all incomes items from database and return a tuple of objects"""
        db = DB()
        income_dict_list = db.FetchAll(Income.table_name)
        return Income._from_dict_to_tuple(income_dict_list)
    
    @staticmethod
    def FetchDateInterval(date_from: str, date_to: str):
        """Fetch all incomes between a date interval"""
        db = DB()
        income_dict_list = db.FetchDate(Income.table_name, date_from, date_to)
        return Income._from_dict_to_tuple(income_dict_list)

"""
def print_categories_tree(lCat:Tuple[Category], parentId:int, depth:int, maxDepth:int):
    if maxDepth > depth:
        lCat_parent = [cat for cat in lCat if (cat.parent == parentId)]
        for cat in lCat_parent:
            tab_char = '\t'
            print(f"{tab_char*depth}" + cat.to_string(FormatType.TREE))
            print_categories_tree(lCat, cat.id, depth+1, maxDepth)
    else:
        pass

def balance_month(relative_month:int):
    # 1. calculate date_from and date_to
    today = date.today()
    relative_month = abs(relative_month)
    shifted_date = today - relativedelta(months=relative_month)
    date_from = shifted_date.replace(day=1)
    last_day_of_month = calendar.monthrange(shifted_date.year, shifted_date.month)[1]
    date_to = shifted_date.replace(day=last_day_of_month)
    # 2. extract all expenses for the date interval
    tExp = Expense.FetchDateInterval(date_from, date_to)
    # 3. extract all incomes for the date interval
    tInc = Income.FetchDateInterval(date_from, date_to)
    # 4. sum all the expenses
    exp_sum = 0
    for exp in tExp:
        exp_sum += float(exp.amount)
    # 5. sum all the incomes
    inc_sum = 0
    for inc in tInc:
        inc_sum += float(inc.amount)
    print(f"From {date_from} to {date_to}")
    print(f"Incomes: {inc_sum:.2f}")
    print(f"Expenses: {exp_sum:.2f}")
    print(f"Balance: {(inc_sum - exp_sum):.2f}")
"""

"""
parser = argparse.ArgumentParser(description="Expenses manager")
top_level_subparsers = parser.add_subparsers(dest="item", required=True, help="Available commands")
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

    if args.item == "exp":
        if args.exp_command == "add":
            # add expense
            exp_date = date.today()
            if (args.date is not None) and (args.date != ""):
                exp_date = args.date
                # todo: add date validation
            expense = Expense(args.category, exp_date, args.amount, args.title, args.notes)
            #expense.Create()
            expense.Add()
            print(f"Expense added to the database")
        elif args.exp_command == "list":
            # list all expenses
            tExp = Expense.FetchAll()
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
            tInc = Income.FetchAll()
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
            pass
"""
