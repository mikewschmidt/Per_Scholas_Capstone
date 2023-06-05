-- Query 1: Used to display the transactions made by customers living in a given zip code for a given month and year. Order by day in descending order.
SELECT TIMEID, TRANSACTION_ID, c.first_name, c.last_name, cust_city, cust_state, cust_zip, TRANSACTION_TYPE, TRANSACTION_VALUE
FROM cdw_sapp_credit_card cc
JOIN cdw_sapp_customer c
	ON cc.cust_ssn = c.ssn
WHERE c.cust_zip = 19438
AND substr(TIMEID, 1, 4) = '2018'
AND substr(TIMEID, 5, 2) = '11'
ORDER BY substr(TIMEID, 7, 2) DESC
;

-- Query 2: Used to display the number and total values of transactions for a given type.
SELECT Transaction_Type, count(*) Transaction_Count, sum(transaction_value) Transaction_Total
FROM cdw_sapp_credit_card
WHERE transaction_type = "Bills"
GROUP BY transaction_type
;

-- Query 3: Used to display the total number and total values of transactions for branches in a given state.
SELECT Branch_State, count(branch_state) Total_Transactions, sum(cc.transaction_value) Total_Value 
FROM cdw_sapp_branch b
JOIN cdw_sapp_credit_card cc
	ON b.branch_code = cc.BRANCH_CODE
WHERE b.branch_state = 'IL'
GROUP BY branch_state
;

-- Query 4: Used to check the existing account details of a customer.
SELECT *
FROM cdw_sapp_customer c 
WHERE SSN = 123454487
;

-- Query 5: Used to modify the existing account details of a customer.
UPDATE cdw_sapp_customer
SET first_name = first_name,
	middle_name = 'Ezequiel',
	last_name = last_name,
	credit_card_no = credit_card_no,
	full_street_address = full_street_address,
	cust_city = cust_city,
	cust_state = cust_state,
	cust_country = cust_country,
	cust_zip = cust_zip,
	cust_phone = cust_phone,
	cust_email = cust_email,
    last_updated = CURRENT_TIMESTAMP
WHERE ssn = 123454487
;

-- Query 6: Used to generate a monthly bill for a credit card number for a given month and year.
SELECT first_name, middle_name, last_name, cust_email,
		full_street_address, cust_city, cust_state, cust_zip, cust_country
		cust_ssn, cc.credit_card_no, 
        timeid, transaction_type, branch_code, transaction_value
FROM cdw_sapp_credit_card cc
JOIN cdw_sapp_customer c
	ON cc.credit_card_no = c.credit_card_no
WHERE c.credit_card_no = 4210653349028689
AND SUBSTR(timeid, 1, 4) = 2018
AND SUBSTR(timeid, 5, 2) = 10
;


-- Query 7: Used to display the transactions made by a customer between two dates. Order by year, month, and day in descending order.
SELECT *
FROM cdw_sapp_credit_card
WHERE cust_ssn = 123459988
AND TIMEID BETWEEN '20180101' AND '201810522'
ORDER BY TIMEID 
;



