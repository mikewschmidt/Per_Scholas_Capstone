# Capstone Project for Per Scholas

### Raw data used

[3 json files](https://drive.google.com/drive/folders/1J4a2UndLvVWszHAL2VxJeVXyAHm3xYIp?usp=sharing)

[API json location](https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json)

### Steps to working on Project

1. Downloaded and explored the data
   a. Used the column names and length of the data to create the tables

2. Created a database and tables

3. Write ETL code:
   a. Extract data from datafiles and API
   b. Write transformation code with PySpark
   i. Updated the database tables to reflect the transformations
   c. Load into database

4. Created the Queries for the front-end terminal app

5. Create a "front-end" terminal menu
   a. For displaying aggragated information about transactions
   b. For displaying and modifying users information
   
   
### Technical Challenges
1. Connection to the remote database caused many headaches. I searched for a few different libraries to import and jdbc drivers to download, then tried the different connection string/snippets to connect with.

2.    
