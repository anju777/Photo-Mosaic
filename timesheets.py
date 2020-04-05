# Name: Anju Ito

import time

# By including timesheet(numberHour, comment), can log time that worked on
# like TP!
def timesheet(comment='', numberHour=0):
    path = 'C:\\Users\\anjua\\OneDrive\\Desktop\\Photo-Mosaic\\timesheet.txt'
    csvTimesheet = readTimesheet(path)

    linedRow = '_' * 50
    statusRow, lastEntryRow, newEntryRow, totalHoursRow = 2, -3, -2, -1
    loggingOut = False
    if (numberHour == 0):
        if (csvTimesheet[statusRow][0].count('Logged Out')):
            csvTimesheet[statusRow] = ['Status: Logged In']
            returnLine = "Logged In!"
            comment = str(time.time())
        else: 
            csvTimesheet[statusRow] = ['Status: Logged Out']
            returnLine = "Logged out! Good work ^^"
            loggingOut = True
            start = float(csvTimesheet[lastEntryRow][-1].strip())
            end = time.time()
            numberHour = calculateElapsedHours(start, end)
            if (numberHour == 0): 
                # Make no change to data when less than 0.5 hr spent
                # Except changing status to Logged Out
                csvTimesheet.pop(lastEntryRow)
                writeTimesheet(path, csvTimesheet)
                return "Does not count: Less than 0.1 hours spent"
    else:
        if (csvTimesheet[statusRow][0].count('Logged In')):
            return "Please log out before you make the request"
        returnLine = "Request processed!"
        csvTimesheet[statusRow] = ['Status: Logged Out']

    newEntry = ' ' + str(numberHour) + (' ' * (3 - len(str(numberHour)))) + ' | ' + time.ctime() + ' | ' + comment    
    totalTime, totalCount = obtainPastCounts(csvTimesheet, loggingOut)
    totalTime += numberHour
    newEntry = ['   ' + str(totalCount) + '  | ' + newEntry]
    csvTimesheet[totalHoursRow] = ['Total Hours: ' + str(totalTime)]
    if (loggingOut):
        csvTimesheet[lastEntryRow] = newEntry
    else:
        csvTimesheet.insert(newEntryRow, newEntry)

    writeTimesheet(path, csvTimesheet)
    return returnLine

# Takes the status of the timesheet and its data, returning the count that
# it's on and the sum fo the totalHours spent thus far
def obtainPastCounts(csvTimesheet, loggingOut):
    rows =  len(csvTimesheet)
    totalTime = 0
    totalCount = 0 if loggingOut else 1

    for row in range(rows-2):
        data = csvTimesheet[row]

        # Data not a timesheet row (no |)
        if (len(data) <= 1): 
            continue
        hour = data[1].strip()
        if(hour.isdigit()):
            totalCount += 1
            totalTime += int(hour)
        elif (hour.find('.') == 1):
            totalCount += 1
            totalTime += float(hour)
    return totalTime, totalCount

# Takes in start time.time() and end time.time(), and returns total hours 
# passed. Hours rounded to nearest integer or 0.5 increment.
def calculateElapsedHours(start, end):
    elapsedSeconds = end - start
    elapsedHours = elapsedSeconds/3600
    numberHour = round(elapsedHours, 1)
    return numberHour

# Takes in an int or float, and rounds it to the nearest int/0.5 increment.
# Returns False if not an int or float
def roundFive(n):
    if (isinstance(n, int)):
        return n
    elif (not isinstance(n, float)):
        return False
    else:
        stringN = str(n)
        decimalIndex = stringN.find('.')
        assert(decimalIndex != -1)
        number = int(stringN[decimalIndex + 1])
        if (number < 3):
            return int(n)
        elif (number > 7):
            return int(n) + 1
        else:
            return int(n) + 0.5

# Looks into the file, and makes a 2d list of the text
# Each row is separated by the separator, which is currently set to |
# Note: All row that doesn't have | will have length of |
def readTimesheet(path):
    currentFile = readFile(path)
    csv = currentFile.splitlines()
    separator = ' | '
    for i in range(len(csv)):
        csv[i] = csv[i].split(separator)
    return csv

# Takes in 2d list of csvData and converts in original text
def writeTimesheet(path, csvData):
    rows = len(csvData)
    separator = ' | '
    for rowIndex in range(rows):
        csvData[rowIndex] = separator.join(csvData[rowIndex])
    csvData = "\n".join(csvData)
    writeFile(path, csvData)    

# bottom 2 functions taken from 15-112 website:
# https://www.cs.cmu.edu/~112/notes/notes-strings.html
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)