#used to manage flask related commands
import Utils as u
import os
import subprocess
import shutil

AUTO_START_FLASK = True
os.environ['FLASK_APP'] = 'manage.py'

def initDb():
    os.system('start cmd /c "flask db init & pause"')
    u.printMessage('Init action done', True)

def migrateDb():
    os.system('start cmd /c "flask db migrate & pause"')
    u.printMessage('Migrate action done', True)

def upgradeDb():
    os.system('start cmd /c "flask db upgrade & pause"')
    u.printMessage('Upgrade action done', True)

def reinitializeDb():

    if u.locationExists('migrations'):
        shutil.rmtree('migrations')

    if u.fileExists('app/main/flask_boilerplate_main.db'):
        os.remove('app/main/flask_boilerplate_main.db')

    os.system('start cmd /c "flask db init & flask db migrate & flask db upgrade"')
    u.printMessage('reinitializeDb action done', True)

def startFlaskApp():
    os.system('start cmd /c "flask run"')
    u.printMessage('Flask action done', True)

def testFlaskApp():
    os.system('start cmd /c "flask test & pause"')
    u.printMessage('test action done', True)

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

    if choice == 99:
        quit()


def main():

    if AUTO_START_FLASK:
        os.system('start cmd /c "flask run"')

    while True:
        openMenu()


if __name__ == '__main__':
    main()