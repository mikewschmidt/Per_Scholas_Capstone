
import mariadb


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


def query_db(query):
    try:
        conn = mariadb.connect(
            user='michaelwschmidt_cc_capstone',
            password='password1',
            host='65.19.141.77',
            port='3306',
            database='michaelwschmidt_creditcard_capstone')
        cur = conn.cursor()
        # cur.execute(query)
        # rows = cur.fetchall()
        conn.close()

    except mariadb.Error as e:
        print(f"ERROR connecting to MariaDB:  {e}")

    finally:
        conn.close()
        # return rows


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
                       "1) Display zipcode's transactions for a given month and year\n" +
                       "2) Display the number and total values of transactions for a given type\n" +
                       "3) Display the total number and total values of transactions for branches in a given state\n" +
                       "4) Check the existing account details of a customer\n" +
                       "5) Modify the existing account details of a customer\n" +
                       "6) Generate a monthly bill for a credit card number for a given month and year\n" +
                       "7) Display the transactions made by a customer between two dates\n" +
                       "q) quit\n")
    match user_input:
        case '1':
            zipcode = get_str_input('Zipcode', 5)
            year = get_str_input('Year', 4)
            month = get_month()
            print(
                f"Looking up transactions for {month}/{year} in zipcode {zipcode}")
            ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########

        # display the number and total values of transactions for a given type.
        case '2':
            trans_type = get_trans_type()
            ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
            # Display number of transactions
            # Display total values of transactions

        # display the total number and total values of transactions for branches in a given state.
        case '3':
            state = get_str_input('State', 2)
            ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
            # Display total number of transactions for branches in a given state
            # Display total values of transactions for branches in a given state

        # check the existing account details of a customer
        case '4':
            ssn = get_str_input('SSN', 9)
            ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
            # Display customer's account details

            # modify the existing account details of a customer
        case '5':
            print(f"pressed option {user_input}")
            ssn = get_str_input('SSN', 9)
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
                f"Generate bill on CC Num: {cc_num} for {month}/{year}")
            ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
            # Generate a monthly bill for the given month and year

            # display the transactions made by a customer between two dates. Order by year, month, and day in descending order.
        case '7':
            ssn = get_str_input('SSN', 9)
            begin_date = get_str_input('beginning date (YYYYMMDD)', 8)
            end_date = get_str_input('ending date (YYYYMMDD)', 8)
            ##########  CALL FUNCTION TO QUERY DATABASE!!! ###########
            # display the transactions made by a customer between two dates

        case 'q':
            query = "SELECT * FROM cdw_sapp_customer"
            print(query_db(query))
            exit()

        case _:
            print_bad_response(user_input)

    user_input = ""
