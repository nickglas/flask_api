import os
import shutil

def clearScreen():
    os.system('cls')

def fileExists(path):
    if os.path.isfile(path):
        return True
    return False

def locationExists(path):
    if os.path.exists(path):
        return True
    return False

def getAllFileNamesFromPath(directory_path):
    if not os.path.exists(directory_path):
        return None
    
    files = []

    for path in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, path)):
            files.append(path)
    
    return files

def createOptionsArray(files):
    counterPounter = 1

    dict = {}

    for f in files:
        dict[counterPounter] = f
        counterPounter += 1

    return dict
def deleteFolder(path):
    shutil.rmtree(path)	

def deleteFile(path):
    os.remove(path)	

def askInput(message, inputMessage, datatype):
    print (message)
    value = input(inputMessage)

    if not datatype == None:
        return datatype(value)

    return value

def printMessage(message, waitForInput):
    print('\n'+message)

    if waitForInput:
        input("Press Enter to continue...")



