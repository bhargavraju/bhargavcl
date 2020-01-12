## Cluster Management

This flask application simulate basic steps involved in managing cloud clusters and machines.

### Application URL
The application is hosted remotely at https://clmgmt.herokuapp.com/

### Local setup

To run this project on your local
1. Install mongodb on your local machine and ensure mongodb is running as a service
2. Ensure that there isn't an existing database called 'app_db' in your mongo as that is the default db name
3. If you want to change mongo settings, please do so at db/mongo_conn.py
4. Install python3.6 on your machine
5. Create a virtual environment
6. Install pip packages from requirements.txt in the root folder using "pip install -r requirements.txt'
7. Activate the virtual environment
8. Open a terminal in your root folder and run "python app.py"
9. Go to http://localhost:5000/. You should see a welcome message

### Testing the APIs

* Details necessary to test each api are provided in the corresponding docstrings.
* Every GET and DELETE request takes input params as URL string arguments.
* Most PUT and POST request take input params as form-data. The exceptions to this are
    * Add Machine API (/cluster/add_machine)
    * Modify Status by Tag API (/cluster/status/modify/tags)
* These 2 APIs consume request body as a json. The 'Content-Type' header should be set to 'application/json' in these cases.
* As the scope of the application is pretty basic, the server may not cover all possibilities of wrong request data
(although fundamental checks have been placed to advise the user on why his request data might be wrong)
* The possible values of machine states are restricted to 'Running' and 'Terminated'. "Rebooting" is not available

### Running test cases

* All test cases are present in the 'test' module
* run the command 'pytest' in the root folder to run the test cases
