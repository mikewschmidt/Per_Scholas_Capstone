
import pandas as pd
import mariadb
import sqlalchemy
from tabulate import tabulate
import os


def get_month():
    user_input = ""
    while user_input == "":
        user_input = input("Enter Month Number:  ")
        if int(user_input) < 0 or int(user_input) > 12:
            print("INCORRECT Month Number! Please try again!")
            user_input = ""
            continue
    return user_input


def get_str_input(info, length):
    user_input = ""
    while user_input == "":
        user_input = input(f"Enter {info}:  ")
        if len(user_input) != length:
            print(f"INCORRECT {info}! Please try again!")
            user_input = ""
            continue
    return user_input


def get_trans_type():
    user_input = ""
    while user_input == "":
        user_input = input("Choose from the options below:\n" +
                           "1) Bills\n" +
                           "2) Healthcare\n" +
                           "3) Gas\n" +
                           "4) Education\n" +
                           "5) Test\n" +
                           "6) Entertainment\n" +
                           "7) Grocery\n" +
                           "q) quit\n")
        match user_input:
            case "1":
                user_input = "Bills"

            case "2":
                user_input = "Healthcare"

            case "3":
                user_input = "Gas"

            case "4":
                user_input = "Education"

            case "5":
                user_input = "Test"

            case "6":
                user_input = "Entertainment"

            case "7":
                user_input = "Grocery"

            case "q":
                exit()

            case _:
                user_input = ""
                print_bad_response(user_input)
    return user_input


def query_db(query, printable=True):
    try:
        df = pd.DataFrame()
        user = "michaelwschmidt_cc_capstone"
        password = os.environ.get("CREDITCARD_CAPSTONE_PASSWORD")
        host = "tommy2.heliohost.org"
        port = "3306"
        database = "michaelwschmidt_creditcard_capstone"
        print()

        '''
        # engine = sqlalchemy.create_engine(f"mariadb+mariadbconnector://{user}:{password}@{host}/{database}")
        engine = sqlalchemy.create_engine(
            f"mariadb+mariadbconnector://michaelwschmidt_cc_capstone:{password}@tommy2.heliohost.org/michaelwschmidt_creditcard_capstone")
        # print(engine.table_names())
        with engine.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM  michaelwschmidt_creditcard_capstone.cdw_sapp_branch")

        print(rows)
        '''
        conn = mariadb.connect(
            user="michaelwschmidt_cc_capstone",
            password=password,
            host="tommy2.heliohost.org",
            port=3306,
            database="michaelwschmidt_creditcard_capstone"
        )

        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        df = pd.read_sql_query(query, conn)

        if printable:
            print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
            print("\n===========================================\n\n")

    except mariadb.Error as e:
        print(f"ERROR connecting to MariaDB:  {e}")

    finally:
        conn.close()
        if not df.empty:
            return df
        else:
            print("DATAFRAME IS EMPTY!  Something went wrong!")


def update_cust_db(ssn):
    user_input = ""

    while user_input != 'q':
        results = query_db(f"SELECT first_name, middle_name, last_name, credit_card_no, full_street_address, \
                        cust_city, cust_state, cust_country, cust_zip, cust_phone, cust_email \
                        FROM cdw_sapp_customer \
                        WHERE ssn = {ssn}", False)

        print("\n\nWHICH ITEM DO YOU WANT TO MODIFY? ('q' to quit)")
        print("=======================================================\n")
        print(tabulate(results.transpose().reset_index(), tablefmt='fancy_grid'))
        print("=======================================================\n")

        user_input = input("Item number:  ")
        # test to see if user_input is out of range
        if user_input == 'q':
            print("\n\n")
            print("=======================================================\n")
            break
        elif user_input.isdigit():
            user_input = int(user_input)

        if user_input < 0 or user_input > 10:
            continue

        print("\n\nEnter a new value? ('q' to quit)")
        print("=====================================\n")
        col_name = results.columns[user_input]
        new_item = input(f"| {user_input} | {col_name} |  ")

        # Connect to the database
        try:
            password = os.environ.get("CREDITCARD_CAPSTONE_PASSWORD")
            conn = mariadb.connect(user="michaelwschmidt_cc_capstone",
                                   password=password, host="tommy2.heliohost.org",
                                   port=3306, database="michaelwschmidt_creditcard_capstone"
                                   )
            cur = conn.cursor()
            # Create update statement
            query = f"UPDATE cdw_sapp_customer \
                        SET {col_name} = '{new_item}', \
                        last_updated = CURRENT_TIMESTAMP \
                        WHERE ssn = {ssn}"
            cur.execute(query)
            conn.commit()
        finally:
            conn.close()


def generate_bill(cc_num, year, month):
    # Get customer information to display once
    cust_df = query_db(
        f"SELECT * FROM cdw_sapp_customer WHERE credit_card_no={cc_num}", False)
    print("cust_df:   ", cust_df)
    # Get transactions for a given month and year

    trans_df = query_db(f"SELECT * FROM cdw_sapp_credit_card \
                            WHERE credit_card_no = {cc_num} \
                            AND SUBSTR(timeid, 1, 4) = {year} \
                            AND SUBSTR(timeid, 5, 2) = {month}", False)
    trans_df = trans_df.drop("TRANSACTION_ID", axis=1)

    # Display customer information
    width = 108
    cust_name = [cust_df.iloc[0]["FIRST_NAME"], cust_df.iloc[0]
                 ["MIDDLE_NAME"], cust_df.iloc[0]["LAST_NAME"]]
    address = [cust_df.iloc[0]["FULL_STREET_ADDRESS"], cust_df.iloc[0]
               ["CUST_CITY"], cust_df.iloc[0]["CUST_STATE"], cust_df.iloc[0]["CUST_ZIP"]]
    contact = [cust_df.iloc[0]["CUST_PHONE"], cust_df.iloc[0]["CUST_EMAIL"]]

    # Get the offset to center the information
    def offset(l_var):
        return (width-len("".join(l_var)))//2

    print("="*width)
    print()
    print(" "*offset(cust_name), *cust_name)
    print(" "*offset(address), *address)
    print(" "*offset(contact), *contact)
    print()
    print("="*width)
    print(tabulate(trans_df, headers='keys', tablefmt='grid'))
    print("="*width, "\n")
    print(
        tabulate(["   YOUR TOTAL BILL FOR THIS MONTH IS: ", " "*15+"$XXXXX"], tablefmt='plain'))
    print()
    print("="*width, "\n")


def print_bad_response(user_input):
    print("\n####################")
    print(
        f"'{user_input}' is NOT a correct option. \nYou need to press a correct option or (q)uit: ")
    print("####################\n")


print("====================================")
print("======= CREDIT CARD TERMINAL =======")
print("====================================")

# Display menu
user_input = ""
while user_input == "":
    user_input = input("Choose from the options below:\n" +
                       "1) Display customers' transactions in a zipcode for a given month and year\n" +
                       "2) Display the number and total values of transactions for a given type\n" +
                       "3) Display the total number and total values of transactions for branches in a given state\n" +
                       "4) Check the existing account details of a customer\n" +
                       "5) Modify the existing account details of a customer\n" +
                       "6) Generate a monthly bill for a credit card number for a given month and year\n" +
                       "7) Display the transactions made by a customer between two dates\n" +
                       "q) quit\n")
    match user_input:
        # Display the transactions made by customers living in a given zip code for a given month and year
        # Order by day in descending order.
        case '1':
            zipcode = get_str_input('Zipcode', 5)
            year = get_str_input('Year', 4)
            month = get_month()
            print(
                f"Looking up transactions for {month}/{year} in zipcode {zipcode}")
            ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
            query_db(f"SELECT TIMEID, TRANSACTION_ID, c.first_name, c.last_name, cust_city, \
                            cust_state, cust_zip, TRANSACTION_TYPE, TRANSACTION_VALUE\
                        FROM cdw_sapp_credit_card cc \
                        JOIN cdw_sapp_customer c \
                            ON cc.cust_ssn = c.ssn \
                        WHERE c.cust_zip = {zipcode} \
                        AND substr(TIMEID, 1, 4) = {year} \
                        AND substr(TIMEID, 5, 2) = {month} \
                        ORDER BY substr(TIMEID, 7, 2) DESC")

        # display the number and total values of transactions for a given type.
        case '2':
            trans_type = get_trans_type()
            query_db(f"SELECT Transaction_Type, count(*) Transaction_Count, sum(transaction_value) Transaction_Total \
                        FROM cdw_sapp_credit_card \
                        WHERE transaction_type = '{trans_type}' \
                        GROUP BY transaction_type")
            ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
            # Display number of transactions
            # Display total values of transactions

        # display the total number and total values of transactions for branches in a given state.
        case '3':
            state = get_str_input('State', 2)
            query_db(f"SELECT Branch_State, count(branch_state) Total_Transactions, sum(cc.transaction_value) Total_Value \
                        FROM cdw_sapp_branch b \
                        JOIN cdw_sapp_credit_card cc \
                            ON b.branch_code = cc.BRANCH_CODE \
                        WHERE b.branch_state = '{state}' \
                        GROUP BY branch_state")
            ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
            # Display total number of transactions for branches in a given state
            # Display total values of transactions for branches in a given state

        # check the existing account details of a customer
        case '4':
            ssn = get_str_input('SSN', 9)
            query_db(f"SELECT * \
                        FROM cdw_sapp_customer c \
                        WHERE SSN = {ssn}")
            ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
            # Display customer's account details

            # modify the existing account details of a customer
        case '5':
            print(f"pressed option {user_input}")
            ssn = get_str_input('SSN', 9)
            update_cust_db(ssn)
            ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
            # Display customer's account details
            # Ask which detail they want to modify
            # Ask what is the NEW value
            # Update the database with the modification

            # generate a monthly bill for a credit card number for a given month and year
        case '6':
            year = get_str_input('Year', 4)
            month = get_month()
            cc_num = get_str_input('Credit Card Number', 16)
            print(
                f"Generate bill on CC Num: {int(cc_num)} for {int(month)}/{int(year)}")
            ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
            # Generate a monthly bill for the given month and year
            generate_bill(cc_num, year, month)

            # display the transactions made by a customer between two dates. Order by year, month, and day in descending order.
        case '7':
            ssn = get_str_input('SSN', 9)
            begin_date = get_str_input('beginning date (YYYYMMDD)', 8)
            end_date = get_str_input('ending date (YYYYMMDD)', 8)
            ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
            # display the transactions made by a customer between two dates
            query_db(f"SELECT TIMEID, CREDIT_CARD_NO, CUST_SSN, BRANCH_CODE, TRANSACTION_TYPE, TRANSACTION_VALUE \
                        FROM cdw_sapp_credit_card \
                        WHERE cust_ssn = {ssn} \
                        AND TIMEID BETWEEN '{begin_date}' AND '{end_date}' \
                        ORDER BY TIMEID ")

        case 'q':
            exit()

        case _:
            print_bad_response(user_input)

    user_input = ""
