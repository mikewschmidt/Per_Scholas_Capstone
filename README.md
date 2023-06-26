# Data Engineering capstone project for Per Scholas 

### Overview
Created a data pipeline to extract the data from data files and an API end-point, transform the data, and load it into a remote database.
The data is mock data for banks, customers, credit card transactions, and loan application data.

![dataflow diagram](https://github.com/mikewschmidt/Per_Scholas_Capstone/blob/master/data_files/workflow_diagram.jpg)

### Raw data used

[3 json files](https://drive.google.com/drive/folders/1J4a2UndLvVWszHAL2VxJeVXyAHm3xYIp?usp=sharing)
   - CDW_SAPP_CUSTOMER.JSON: This file has the existing customer details.
   - CDW_SAPP_CREDITCARD.JSON: This file contains all credit card transaction information.
   - CDW_SAPP_BRANCH.JSON: Each branch’s information and details are recorded in this file. 

[API json location](https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json)
   - This dataset has all of the required fields for a loan application.

### Steps to working on Project

1. Downloaded and explored the data
   - Used the column names and length of the data to create the tables

2. Created a database and tables

3. Write ETL code:
   - Extract data from datafiles and API
   - Write transformation code with PySpark
   - Updated the database tables to reflect the transformations
   - Load into the database

4. Create a "front-end" terminal menu
   - Created the Queries for the front-end terminal app
   - For displaying aggregated information about transactions
   - For displaying and modifying users' information
   
5. Data Analysis and Visualization
   - Charts and graphs for the data files
   - Charts and graphs for loan API data
   - Created Visualizations in Tableau
   
### Technologies
The following technologies were used for this project:
   - GitHub
   - Visual Studio Code
   - Python
      - Libraries: pandas, pyspark, requests, tabulate, matplotlib, folium, mariadb, tabulate
   - SQL
   - MariaDB
   - Jupyter Notebook
   - Tableau
   
   
   
### Technical Challenges
1. Connection to the remote database caused many headaches I tried all the mySQL options on the MariaDB database, but I found there were issues. I searched for a few different libraries to import and JDBC drivers to download, then tried the various connection strings/snippets to connect with.

2. The overall challenge was to fulfill the requirements with the data that was given and resolved it by modifying the data to make it work.    
