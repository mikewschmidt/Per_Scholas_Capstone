# Capstone Project for Per Scholas

### Raw data used

[3 json files](https://drive.google.com/drive/folders/1J4a2UndLvVWszHAL2VxJeVXyAHm3xYIp?usp=sharing)

[API json location](https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json)

### Steps to working on Project

1. Downloaded and explored the data
   a. Used the column names and length of the data to create the tables

2. Created a database and tables

3. Write ETL code:
   Extract data from datafiles and API
   b. Write transformation code with PySpark
   d. Updated the database tables to reflect the transformations
   e. Load into database

4. Create a "front-end" terminal menu
   a. Created the Queries for the front-end terminal app
   b. For displaying aggregated information about transactions
   c. For displaying and modifying users information
   
5. Data Analysis and Visualization
   a. Charts and graphs for the data files
   b. Charts and graphs  
   

   
   
### Technical Challenges
1. Connection to the remote database caused many headaches I tried all the mySQL options on the MariaDB database, but I found there was issues. I searched for a few different libraries to import and jdbc drivers to download, then tried the different connection string/snippets to connect with.

2. The overall challenge was to fullfill the requirements with the data that was given. Some of the data needed some modifications to make it work.      
