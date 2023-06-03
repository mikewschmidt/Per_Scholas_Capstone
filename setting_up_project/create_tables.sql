
----- SAMPLE BRANCH DATA ------
/*
	{'BRANCH_CODE': 1, 'BRANCH_NAME': 'Example Bank', 'BRANCH_STREET': 'Bridle Court', 
    'BRANCH_CITY': 'Lakeville', 'BRANCH_STATE': 'MN', 'BRANCH_ZIP': 55044, 
    'BRANCH_PHONE': '1234565276', 'LAST_UPDATED': '2018-04-18T16:51:47.000-04:00'}
*/
DROP TABLE IF EXISTS branches;
CREATE TABLE IF NOT EXISTS branches (
	BRANCH_CODE int PRIMARY KEY,
	BRANCH_NAME varchar(50),
	BRANCH_STREET varchar(50),
	BRANCH_CITY varchar(50),
	BRANCH_STATE char(2),
	BRANCH_ZIP char(5),
	BRANCH_PHONE char(11),
	LAST_UPDATED timestamp
);


----- customer SAMPLE DATA -----
/*
	{'FIRST_NAME': 'Alec', 'MIDDLE_NAME': 'Wm', 'LAST_NAME': 'Hooper', 'SSN': 123456100, 
	'CREDIT_CARD_NO': '4210653310061055', 'APT_NO': '656', 'STREET_NAME': 'Main Street North', 
	'CUST_CITY': 'Natchez', 'CUST_STATE': 'MS', 'CUST_COUNTRY': 'United States', 'CUST_ZIP': '39120', 
	'CUST_PHONE': 1237818, 'CUST_EMAIL': 'AHooper@example.com', 'LAST_UPDATED': '2018-04-21T12:49:02.000-04:00'}
*/
DROP TABLE IF EXISTS customers;
CREATE TABLE IF NOT EXISTS customers (
	FIRST_NAME varchar(50),
	MIDDLE_NAME varchar(50),
	LAST_NAME varchar(50),
	SSN char(9) PRIMARY KEY,
	CREDIT_CARD_NO char(16),
	APT_NO varchar(10),
	STREET_NAME varchar(50),
	CUST_CITY varchar(50),
	CUST_STATE char(2),
	CUST_COUNTRY varchar(50),
	CUST_ZIP char(5),
	CUST_PHONE varchar(11),
	CUST_EMAIL varchar(100),
	LAST_UPDATED timestamp
);

----- SAMPLE CREDIT CARD DATA ------
/*
	{'TRANSACTION_ID': 1, 'DAY': 14, 'MONTH': 2, 'YEAR': 2018, 'CREDIT_CARD_NO': '4210653349028689', 
    'CUST_SSN': 123459988, 'BRANCH_CODE': 114, 'TRANSACTION_TYPE': 'Education', 'TRANSACTION_VALUE': 78.9}
*/
DROP TABLE IF EXISTS cc_transactions;
CREATE TABLE IF NOT EXISTS cc_transactions (
	TRANSACTION_ID 	int PRIMARY KEY,
	DAY 				int,
	MONTH 				int,
	YEAR 				int,
	CREDIT_CARD_NO 		char(16),
	CUST_SSN 			char(9),
	BRANCH_CODE 		int,
	TRANSACTION_TYPE 	varchar(50),
	TRANSACTION_VALUE	decimal,
	FOREIGN KEY (BRANCH_CODE) REFERENCES branches (BRANCH_CODE)
		ON DELETE CASCADE
		ON UPDATE RESTRICT
);

