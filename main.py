from datetime import datetime, timedelta, date
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Used in generating the dictionaries used in other functions
def generateYearDays(year):
    # Start and end date for the year
    startDate = date(year, 1, 1)
    endDate = date(year, 12, 31)
    
    # Generate all dates of the year
    delta = timedelta(days=1)
    currentDate = startDate
    datesDict = {}
    
    while currentDate <= endDate:
        datesDict[currentDate.strftime("%Y-%m-%d")] = 0
        currentDate += delta
    
    return datesDict
def generateYearWeeks(year):
    # Find the first Sunday of the year
    startDate = date(year, 1, 1)
    while startDate.weekday() != 6:  # Sunday is 6 in Python's weekday()
        startDate += timedelta(days=1)
    
    # Generate all Sundays of the year
    datesDict = {}
    while startDate.year == year:
        datesDict[startDate.strftime("%Y-%m-%d")] = 0
        startDate += timedelta(weeks=1)
    
    return datesDict

# Converts the data from daily format to weekly
def convertToWeekly(data): 
    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame(list(data.items()), columns=["date", "value"])

    # Convert the 'date' column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Group by weekly periods (starting on Sundays by default)
    weekly_totals = df.resample('W-SUN', on="date")["value"].sum()

    # Convert the result back to a dictionary if needed
    return weekly_totals.to_dict()

# Load the data from the NotionData.json file
with open('NotionData.json', 'r', encoding='utf-8') as notionFile:  
    notionData = json.load(notionFile)

# Converts the Notion Task List data into a more consistent format
def parseTasks(data):
    filtered = []
    monthToNumber = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }

    for task in data:
        # Date examples =   "March 22, 2024"
        #                   "January 3, 2024 2:57 PM"
        #                   "March 11, 2024 23:59 (GMT+3)"
        #                   "May 11, 2024 15:00 (GMT+3) → 16:30"
        taskDate = task['Date'].split(' ')[:3]
            
    
        taskMonthString = task['Date'].split(' ')[0]        # Get the month name
        taskMonthNum = monthToNumber[taskMonthString]       # Convert month name to number
        
        taskDay = task['Date'].split(' ')[1].strip()[:-1]   # Get the day
        if len(taskDay) == 1:
            taskDay = '0' + taskDay

        taskYear = task['Date'].split(' ')[2].strip()       # Get the year
        taskDate = taskYear + '-' + taskMonthNum + '-' + taskDay
        filtered.append({'Name': task['Name'], 'Date': taskDate})
    filtered.sort(key=lambda x: x['Date'])
    return filtered

def plotTaskDataHistogram(data):
    df = pd.DataFrame(list(data.items()), columns=['Date', 'Number of Tasks'])
    df['Date'] = pd.to_datetime(df['Date'], format='%B %d, %Y', errors='coerce')
    df.set_index('Date', inplace=True)
    plt.figure(figsize=(12, 8))
    plt.bar(df.index, df['Number of Tasks'], color='b', label='Number of Tasks')
    plt.title('Tasks by Date', fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Number of Tasks', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()
def plotTaskDataLine(data):
    plt.figure(figsize=(12, 8))
    plt.plot(data.keys(), data.values(), marker='o', linestyle='-', color='b', label='Total Time')
    plt.title('Total Time by Week', fontsize=16)
    plt.xlabel('Week', fontsize=14)
    plt.ylabel('Total Time', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Converts data to a dictionary format where each day of the year is a key and the number of tasks in that day are the values
def numTasksByDay(data):
    tasksByDay = generateYearDays(2024)
    for task in data:
        date = task['Date']
        tasksByDay[date] += 1
    return tasksByDay

# Filters tasks by whether or not they contain the given word
def filterTasksByKeyword(data, keyword):
    filtered = []
    for task in data:
        if keyword.lower() in task['Name'].lower():
            filtered.append(task)
    return filtered
# Filters tasks by whether or not they fall between a given range of dates
def filterTasksByDate(data, startDate, endDate):
    filtered = []
    for task in data:
        if startDate <= task['Date'] <= endDate:
            filtered.append(task)
    return filtered


with open('SpotifyData.json', 'r', encoding='utf-8') as spotifyFile:  
    spotifyData = json.load(spotifyFile)
 
def plotSongDataHistogram(dictToPlot):  
    df = pd.DataFrame(list(dictToPlot.items()), columns=['Date', 'Total Time'])
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    plt.figure(figsize=(12, 8))
    plt.bar(df.index, df['Total Time'], color='b', label='Total Time')
    plt.title('Total Time by Date', fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Total Time', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()
def plotSongDataLine(dictToPlot):
    plt.figure(figsize=(12, 8))
    plt.plot(dictToPlot.keys(), dictToPlot.values(), marker='o', linestyle='-', color='b', label='Total Time')
    plt.title('Total Time by Week', fontsize=16)
    plt.xlabel('Week', fontsize=14)
    plt.ylabel('Total Time', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
# Converts data into a dictionary where each day of the year is a key and the total amount of time spent listening to music (in hours) that day are the values 
def songTimeByDay(data):
    timeByDay = generateYearDays(2024)
    for track in data:
        date = track['endTime'][:10]
        if date in timeByDay:
            timeByDay[date] += track['msPlayed'] / 1000 / 60 / 60  # Convert milliseconds to hours
    return timeByDay

# Filters the listening history data by whether or not they fall into a given range of dates (wasn't used because the size of the dataset made it unneccesary)
def filterSongsByDate(data, startDate, endDate):
    filtered = []
    for song in data:
        if startDate <= song['endTime'] <= endDate:
            filtered.append(song)
    return filtered

# Plots the tasks and listening history on the same graph to better see differences and relations
def comparePlots(notionData, spotifyData, num_dates=52):
    # Create a figure
    plt.figure(figsize=(12, 8))

    # Plot Notion data as a bar plot
    plt.bar(notionData.keys(), notionData.values(), color='b', alpha=0.6, label='Notion Tasks')

    # Plot Spotify data as a line plot
    plt.plot(spotifyData.keys(), spotifyData.values(), color='r', alpha=0.6, label='Spotify Listening Time (hours)')

    # Set labels and title
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Count / Total Listening Time', fontsize=14)
    plt.title('Comparison of Notion Tasks and Spotify Listening Time', fontsize=16)

    # Add legends
    plt.legend(loc='upper left')

    # Show grid and layout
    plt.grid(True, linestyle='--', alpha=0.7)

    # Reduce the number of dates on the x-axis
    all_dates = list(notionData.keys())
    selected_dates = all_dates[::max(1, len(all_dates) // num_dates)]
    plt.xticks(selected_dates, rotation=45)

    plt.tight_layout()
    plt.show()

timeByDay = songTimeByDay(spotifyData)
tasksByDay = numTasksByDay(parseTasks(notionData))
comparePlots(tasksByDay, timeByDay)


timebyWeek = convertToWeekly(timeByDay)
tasksByWeek = convertToWeekly(tasksByDay)
comparePlots(tasksByWeek, timebyWeek)

