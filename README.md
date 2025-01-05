# Spotify-Usage-Analytics
## Description
Sabanci University DSA210 Introduction to Data Science Course Fall 2024-2025 Term Project.

This project will be an analysis of my Spotify usage depending on the amount of school work I have.

## Motivation
While think about what do analyze for my project the music streaming service Spotify came to mind. This is because it is the only app that I use to listen to music and I almost exclusively listen to music to pass the time on my way to school. I do not stay in the dorms and going to my university takes me almost 2 hours one way. So, if I am busy with school work I often choose to not go to school to study on my own time as it gives me at least an extra 4 hours to do what I need. This lead me to the hypothesis that if I look at my Spotify usage, I can determine the periods of time where I was extra busy with school work. 

## The Plan
I plan on taking data from Spotify via their API and looking at how much music I listen to on any given day. Then I can compare this data with the data that I got from my task list on Notion to see if my hypothesis is true. If I listended to less music on a given day, that will most likely mean I did not go to school to focus on an assignment or exam. 

## Data Source
I will have two different sources of data:
1. Data exported from Spotify.
2. Data taken from my task list on the Notion app.

There are APIs for both Spotify and Notion so that will most likely be how I export my data but I might just be able to copy the data from Notion by hand.

In addition to the data from my task list, I might choose to use the academic calender for my university for a more general understanding.

## Getting the Data
### Spotify
I first tried to use the spotify API to get my listening history but quickly realised that I could only access the last 50 songs I listened to. This would not be enough as I wanted an entire years worth of listening data. 

After doing some more research, I figured out that I could download my data from Spotify's website which would give me all the data I needed so that is what I did.

The listening history was located in the "StreamingHistory_music_0.json" file so I took that file and wrote a python script to read and parse that data.

### Notion 
Notion also allows users to download their data so that is what I did.

I took the cvs file that had my task list data, used a cvs to json converter online to convert the data into json format since I find that easier to work with.

## Parsing the data
### Spotify Listening History:
I needed 2 things from my Spotify listening history:
1. The date of when I played a song
2. How long I listened to the song 

The date was already in the format that I wanted to I didn't change it.

The time was in miliseconds so I converted it to hours to make it easier to understand.

### Notion Task List:
I needed 2 things from the Notion task list:
1. Name of the task
2. When the task is due

The name is not strictly necessary, but I still wanted to if I decided to do more detailed analysis.

But the date needed some work as it wasn't as consistent as I needed it to be.

Here are some examples of the different date formats:
* March 22, 2024
* January 3, 2024 2:57 PM
* March 11, 2024 23:59 (GMT+3)
* May 11, 2024 15:00 (GMT+3) → 16:30

I converted the dates into the same format as Spotify to keep things consistent
