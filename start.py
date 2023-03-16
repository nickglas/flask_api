#used to manage flask related commands
import Utils as u
import os
import subprocess
import shutil

#Global var to start flask on startup
AUTO_START_FLASK = True

#set manage.py as flask app
os.environ['FLASK_APP'] = 'manage.py'

#main function to call cmd outlet commands. Accepts array of commands
def runCommand(commands):

    if commands == None or not len(commands) > 0 :
        return

    command = 'start cmd /c "venv\\Scripts\\activate.bat'

    for c in commands:
        command += ' & ' + c

    command += '"'

    os.system(command)

#initialized new db
def initDb():
    runCommand(['flask db init'])
    u.printMessage('Init action done', True)

#Create new migration
def migrateDb():
    runCommand(['flask db migrate'])
    u.printMessage('Migrate action done', True)

#apply newest migration
def upgradeDb():
    runCommand(['flask db upgrade'])
    u.printMessage('Upgrade action done', True)

#Removes the migrations folder, database file, init new db, create new migration and apply
def reinitializeDb():

    if u.locationExists('migrations'):
        shutil.rmtree('migrations')

    if u.fileExists('app/main/Shootsoft.db'):
        os.remove('app/main/Shootsoft.db')

    runCommand(['flask db init', 'flask db migrate', 'flask db upgrade', 'pause'])

    u.printMessage('reinitializeDb action done', True)

#Starts a new flask app instance
def startFlaskApp():
    runCommand(['flask run'])
    u.printMessage('Flask action done', True)

#Runs tests
def testFlaskApp():
    runCommand(['flask test', 'pause'])
    u.printMessage('test action done', True)

#Removes venv if exists, install new venv and installing all pip packages from requirements.txt
def initVenv():

    if u.locationExists('venv'):
        shutil.rmtree('venv')

    runCommand(['python -m virtualenv venv','venv\\Scripts\\activate.bat','pip install -r requirements.txt', 'pause'])

    u.printMessage('Venv action done', True)

#seed data into db with cli command
def seedData():
    runCommand(['flask seed'])
    u.printMessage('Seed action done', True)

#Menu with options
def openMenu():

    u.clearScreen()
    print('Flask manager team bat')
    print("""
        1. Init DB
        2. Migrate DB
        3. Upgrade DB
        4. Fully reinitialize db (DATA WILL BE LOST)
        5. Start new flask application instance
        6. Start tests
        7. Init/Reinstall venv and scripts (windows only)
        8. Seed database
        99. Exit/Quit
    """)

    choice = int(input("Please make a choice: "))
    u.clearScreen()

    if choice == 1:
        initDb()
    
    if choice == 2:
        migrateDb()

    if choice == 3:
        upgradeDb()

    if choice == 4:
        reinitializeDb()

    if choice == 5:
        startFlaskApp()

    if choice == 6:
        testFlaskApp()

    if choice == 7:
        initVenv()

    if choice == 8:
        seedData()

    if choice == 99:
        quit()

#Startup check if venv exists
def checkVenv():
    if not u.locationExists('venv'):
        u.clearScreen()
        char = u.askInput('Virtual envirioment not found... do you want to initialize a new virtual envirioment', 'Init new venv (Y/N): ', str)
        if(char.upper() == 'Y'):
            initVenv()

#Startup check if db exists
def checkDB():
    if not u.fileExists('app/main/Shootsoft.db'):
        u.clearScreen()
        char = u.askInput('database not found... do you want to initialize a new database', 'Init new database (Y/N): ', str)
        if(char.upper() == 'Y'):
            reinitializeDb()

#Main loop
def main():

    checkVenv()
    checkDB()

    if AUTO_START_FLASK:
        os.system('start cmd /c "flask run"')

    while True:
        openMenu()

#Call main
if __name__ == '__main__':
    main()