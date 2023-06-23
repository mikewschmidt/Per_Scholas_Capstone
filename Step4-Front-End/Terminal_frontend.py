
import pandas as pd
import sqlalchemy
from sqlalchemy import text, engine, create_engine
from tabulate import tabulate
import os
import time
from datetime import datetime


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
    os.system('clear')
    user_input = ""
    while user_input != "q":
        print("------------------------------------")
        print("-------   Transaction Type   -------")
        print("------------------------------------")
        user_input = input("Choose from the options below:\n" +
                           "1) Bills\n" +
                           "2) Healthcare\n" +
                           "3) Gas\n" +
                           "4) Education\n" +
                           "5) Test\n" +
                           "6) Entertainment\n" +
                           "7) Grocery\n" +
                           "q) quit\n\n>> ")
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
                user_input = 'q'

            case _:
                user_input = ""
                print_bad_response(user_input)
        return user_input


def query_db(query, printable=True, transpose=False):
    try:
        df = pd.DataFrame()

        with open('../.secrets', 'r') as f:
            CREDITCARD_CAPSTONE_PASSWORD = f.read()

        user = "michaelwschmidt_cc_capstone"
        password = CREDITCARD_CAPSTONE_PASSWORD
        host = "tommy2.heliohost.org"
        port = "3306"
        database = "michaelwschmidt_creditcard_capstone"
        print()

        engine = sqlalchemy.create_engine(
            f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")

        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn)

        if printable and transpose:
            print(tabulate(df.transpose().reset_index(), tablefmt='fancy_grid'))
            print("\n", "="*50, "\n\n")

        elif printable:
            print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
            print("\n", "="*50, "\n\n")

    except Exception as e:
        print(f"ERROR connecting to remote MariaDB:  {e}")

    finally:
        time.sleep(5)
        if not df.empty:
            return df
        else:
            print("No Data found!")


def update_cust_db(ssn):
    os.system('clear')
    user_input = ""

    while user_input != 'q':
        os.system('clear')
        print("One moment....Querying data")
        results = query_db(f"SELECT first_name, middle_name, last_name, credit_card_no, full_street_address, \
                        cust_city, cust_state, cust_country, cust_zip, cust_phone, cust_email \
                        FROM cdw_sapp_customer \
                        WHERE ssn = {ssn}", False)

        os.system('clear')
        print("=======================================================")
        print("WHICH ITEM DO YOU WANT TO MODIFY? ('q' to quit)")
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
        else:
            print("I do NOT understand the input, Please Try again....")
            continue

        # Check if the number is between 0-10 since those are the only columns
        if user_input < 0 or user_input > 10:
            print("NOT in range please choose between 0 - 10")
            time.sleep(5)
            continue

        print("\n\nEnter a new value: ('q' to quit)")
        print("=====================================\n")
        col_name = results.columns[user_input]
        new_item = input(f"| {user_input} | {col_name} |  ")
        if new_item == 'q':
            break
        print(f"Updating database item: {col_name} with {new_item}")

        # Connect to the database update table
        try:
            with open('../.secrets', 'r') as f:
                CREDITCARD_CAPSTONE_PASSWORD = f.read()

            user = "michaelwschmidt_cc_capstone"
            password = CREDITCARD_CAPSTONE_PASSWORD
            host = "mikey.helioho.st"
            port = "3306"
            database = "michaelwschmidt_creditcard_capstone"

            engine = sqlalchemy.create_engine(
                f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")

            # cur = conn.cursor()
            # Create update statement
            query = f"UPDATE cdw_sapp_customer \
                        SET {col_name} = '{new_item}', \
                        last_updated = CURRENT_TIMESTAMP \
                        WHERE ssn = {ssn}"
            # cur.execute(query)
            with engine.connect() as conn:
                conn.execute(text(query))
            # conn.commit()
        finally:
            pass
            # conn.close()

            # Clear screen because exiting this function (update_cust_db)
    os.system('clear')


def generate_bill():
    year = get_str_input('Year', 4)
    month = get_month()
    cc_num = get_str_input('Credit Card Number', 16)
    print(
        f"\nGenerating bill for CC Num: {int(cc_num)} on {int(month)}/{int(year)}")

    # Get customer information to display once
    print("\nOne moment....Querying data")
    cust_df = query_db(
        f"SELECT * FROM cdw_sapp_customer WHERE credit_card_no={cc_num}", False)

    # Get credit card transactions for a given month and year
    trans_df = query_db(f"SELECT * FROM cdw_sapp_credit_card \
                            WHERE credit_card_no = {cc_num} \
                            AND SUBSTR(timeid, 1, 4) = {year} \
                            AND SUBSTR(timeid, 5, 2) = {month}", False)
    if trans_df is None:
        os.system('clear')
        print(
            f"Could not find infomation on {year}/{month} for Credit Card #: {cc_num}")
        print("Please try again.")
        generate_bill()
        return

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

    os.system('clear')

    print()
    print("="*width)
    print()
    date = datetime(int(year), int(month), 1).strftime("%B %Y")
    title = f"CREDIT CARD BILL FOR {date}"
    print(" "*offset(title), title)
    print()
    print()
    print(" "*offset(cust_name), *cust_name)
    print(" "*offset(address), *address)
    print(" "*offset(contact), *contact)
    print()
    print("="*width)
    print(tabulate(trans_df, headers='keys', tablefmt='grid'))
    print("="*width, "\n")
    # print(tabulate(["   YOUR TOTAL BILL FOR THIS MONTH IS: ", " "*15+'$'+str(trans_df["TRANSACTION_VALUE"].sum())], tablefmt='plain'))
    print(" "*15,   f"YOUR TOTAL BILL FOR {date} IS: ", " " *
          15+'$'+str(round(trans_df["TRANSACTION_VALUE"].sum(), 2)))
    print()
    print("="*width, "\n")


def print_bad_response(user_input):
    print("\n####################")
    print(
        f"'{user_input}' is NOT a correct option. \nYou need to press a correct option or (q)uit: ")
    print("####################\n")


def main():
    os.system('clear')
    # Display menu
    user_input = ""
    while user_input != "q":

        print("=========================================")
        print("======= MAIN CREDIT CARD TERMINAL =======")
        print("=========================================")

        user_input = input("Choose from the options below:\n" +
                           "1) Display customers' transactions in a zipcode for a given month and year\n" +
                           "2) Display the number and total values of transactions for a given type\n" +
                           "3) Display the total number and total values of transactions for branches in a given state\n" +
                           "4) Check the existing account details of a customer\n" +
                           "5) Modify the existing account details of a customer\n" +
                           "6) Generate a monthly bill for a credit card number for a given month and year\n" +
                           "7) Display the transactions made by a customer between two dates\n" +
                           "q) quit\n\n>>  ")
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
                if trans_type == 'q':
                    continue
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
                            WHERE SSN = {ssn}", transpose=True)

                ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
                # Display customer's account details

                # modify the existing account details of a customer
            case '5':
                ssn = get_str_input('SSN', 9)
                update_cust_db(ssn)
                ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
                # Display customer's account details
                # Ask which detail they want to modify
                # Ask what is the NEW value
                # Update the database with the modification

                # generate a monthly bill for a credit card number for a given month and year
            case '6':
                ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
                # Generate a monthly bill for the given month and year
                generate_bill()

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
                user_input = 'q'

            case _:
                print_bad_response(user_input)


if __name__ == "__main__":
    main()
    os.system('clear')
    print(">"*60)
    print("\nExiting the Credit Card Terminal program. Thank you!\n")
    print(">"*60)
