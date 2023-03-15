#### SHOOTSOFT FLASK PROJECT BUILD ON RESTX BOILER-PLATE WITH JWT(PYTHON 3.9)

### Requirements
In order for this application to work you will need to `pip`, `python 3.9` and a `virtual envirioment`
The windows build uses `venv` and can be activated manually from the project root by typing `venv\Scripts\activate.bat` into a cmd prompt

    To run application: run the start.py file or the start.bat(WINDOWS ONLY)

The flask application will start with no database. In order to create a new database you will need to follow the options inside the menu. Menu item 5 will drop the database, create a new migration and create a new database.

### Viewing the app ###
    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:5000/


### Using Postman / Insomnia ####
    Authorization header is in the following format:

    Key: Authorization
    Value: "token_generated_during_login"

    For testing authorization, url for getting all user requires an admin token while url for getting a single
    user by public_id requires just a regular authentication.


### Based on : Full description and guide (beware this guide targets an older python version!) ###
https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563

