DROP TABLE IF EXISTS loans;

DROP TABLE IF EXISTS cdw_sapp_credit_card;
DROP TABLE IF EXISTS cdw_sapp_customer;
DROP TABLE IF EXISTS cdw_sapp_branch;




----- SAMPLE BRANCH DATA ------
/*
	{'BRANCH_CODE': 1, 'BRANCH_NAME': 'Example Bank', 'BRANCH_STREET': 'Bridle Court', 
    'BRANCH_CITY': 'Lakeville', 'BRANCH_STATE': 'MN', 'BRANCH_ZIP': 55044, 
    'BRANCH_PHONE': '1234565276', 'LAST_UPDATED': '2018-04-18T16:51:47.000-04:00'}
*/
CREATE TABLE IF NOT EXISTS cdw_sapp_branch (
	BRANCH_CODE int PRIMARY KEY,
	BRANCH_NAME varchar(50),
	BRANCH_STREET varchar(50),
	BRANCH_CITY varchar(50),
	BRANCH_STATE char(2),
	BRANCH_ZIP int,
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
CREATE TABLE IF NOT EXISTS cdw_sapp_customer (
	SSN int ,
    FIRST_NAME varchar(50),
	MIDDLE_NAME varchar(50),
	LAST_NAME varchar(50),
	CREDIT_CARD_NO char(16),
    FULL_STREET_ADDRESS varchar(50),
	-- APT_NO varchar(10),
	-- STREET_NAME varchar(50),
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
CREATE TABLE IF NOT EXISTS cdw_sapp_credit_card (
	TRANSACTION_ID 	int PRIMARY KEY,
    TIMEID				char(8),
	-- DAY 				int,
	-- MONTH 				int,
	-- YEAR 				int,
	CREDIT_CARD_NO 		char(16),
	CUST_SSN 			char(9),
	BRANCH_CODE 		int,
	TRANSACTION_TYPE 	varchar(50),
	TRANSACTION_VALUE	decimal,
	FOREIGN KEY (BRANCH_CODE) REFERENCES cdw_sapp_branch (BRANCH_CODE)
		ON DELETE CASCADE
);


----- SAMPLE LOAN DATA ------
/*
	{'Application_ID': 'LP001002', 'Gender': 'Male', 'Married': 'No', 'Dependents': '0',
    'Education': 'Graduate', 'Self_Employed': 'No', 'Credit_History': 1, 
    'Property_Area': 'Urban', 'Income': 'medium', 'Application_Status': 'Y'}
*/
CREATE TABLE IF NOT EXISTS loans (
	Application_ID varchar(10),
	Gender varchar(10),
	Married char(3),
	Dependents int,
	Education varchar(15),
	Self_Employed varchar(3),
	Credit_History int,
	Property_Area varchar(10),
	Income varchar(10),
	Application_Status char(1)
);

