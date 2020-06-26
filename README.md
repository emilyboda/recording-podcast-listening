# Recording your podcast listening using Pocket Casts' Listening History feature
1. Copy get_history.py to your files
2. Add your pocket casts token and history filepath to get_history.py.
3. Follow the instructions [here](https://developers.google.com/sheets/api/quickstart/python) to get your credentials.json and token.pickle files.
4. Copy the credentials.json and token.pickle files to your files.
5. Add your google spreadsheet id to parse_history.py.
6. Set get_history.py to run every hour (or whatever frequency you wish to measure your podcast listening)
7. Use parse_hist.py to parse the history once you have a few days recorded

# Note on the integrity of the data gathered
Since Pocket Casts' Listening History feature does not expose the actual date or time you listened to an episode, I am using the date and time that your script runs to guess the date that you listened. If your script fails to run, you will only know that you listened to the episode at some point after the last time you recorded and before the next time you recorded. No way around this. Because of this, I use the library "Notify" to alert myself if my script fails so I can (hopefully) fix it within the day.

# TO DO
* create an authorization script that can run on a failed status_code
* add export to csv option
* add notify and notify set-up instructions

# TO DO: Authorization Problem
I originally created these files using Google App Script. I had no trouble converting get_history to Python, but my authorization file is giving me errors.
I've included my [original Google App Script authorization file](docs/authorization.js) for reference.
My [Python authorization file](docs/authorization.py) attempts to do the same thing, but returns a 500 Internal Server Error.

# What information is revealed by the Pocket Casts Listening History API
Here is all the information that is returned by the Pocket Casts' Listening History API about one episode you listened to.

```
{
   "uuid": "e1473ac4-c23a-4076-bef2-394851f6c656",
   "url": "https://anchor.fm/s/18480338/podcast/play/15507406/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fproduction%2F2020-5-21%2F84160236-44100-2-4d2e178fed4ea.mp3",
   "published": "2020-06-22T05:00:00Z",
   "duration": 4775,
   "fileType": "audio/mp3",
   "title": "Fans Bring the Weapons - Extreme Championship Wrestling",
   "size": "152807471",
   "playingStatus": 2,
   "playedUpTo": 2113,
   "starred": false,
   "podcastUuid": "7395c3c0-5277-0138-97a4-0acc26574db2",
   "podcastTitle": "Legends of Philadelphia",
   "episodeType": "full",
   "episodeSeason": 1,
   "episodeNumber": 13,
   "isDeleted": false
}
```

Note that this does not include the date or time that you listened to the podcast, only the date and time that it was published.

The webplayer also does not give us this information, so I think it safe to assume that this information is not available anywhere.
<p align="center">
<img src="https://github.com/emilyboda/recording-podcast-listening/blob/master/images/webplayer%20listening%20history%20screenshot.PNG" width="900"><img 
</p>

# So how does my script determine what day a podcast was listened to?
Thankfully, the array that is returned by the API _is_ in chronological order. Using this order, and by pulling this listening history every hour of the day, I can determine which hour of the day I finished listening to an episode. However, if I finish a 2.5 hour long episode at 1:13 pm, my script will tell me that I listened to 2.5 hours of episodes at 2:00 pm.

While I could correct this by telling my script that I listened to 0.5 hours at 12:00 pm, 1 hr at 1:00 pm, and 1 hr at 2:00 pm, but this is still not very accurate. I prefer to record the data every hour of the day, and then display my data on a graph by the day.

# Determining Re-Listening
It's also important to note that if I listen to a episode twice, it will purge the old listen and replace it with the new one. 

When a podcast moves in the list from one data recording to another, it's almost always going to be a continuation of the old listen. In fact, almost every time you listen to an episode that's over an hour your data recordings will show a continued listen. Because it's so common, I've built the script to always assume that you're continuing your listening session when it sees data like this. 

I currently decided to let re-listens overwrite old listens because the risk of messing up all the continuing listens is too great. However, I have some ideas of how I would factor in re-listens.

### Days since last listen
```
if days_since_last_listen < X:
  you're continuing to listen to this episode
elif days_since_last_listen > X:
  I'm going to assume you finished listening last time and you're listening to the episode again now
```

### If the playedUpTo number goes _down_ instead of up
This could fail in two ways: 
* if you decided to go back a minute or two during your listening session at the top of the hour (when your script was taking recordings)
* if the podcast is less than an hour long, you might finish the episode before the hourly data recording can catch that your playedUpTo value was less

## Testing Re-Listening vs. Continued Listening
I've added an [example history array](https://github.com/emilyboda/recording-podcast-listening/blob/master/examples/continued_listening_example.json) that you can use to test whether your code properly senses re-listening.

It shows that the episode "uuid":3 was 50% done on Jan 1st and then it moved up to 100% done on the date of the next recording, Jan 2nd. The episode "uuid":2 was played to 100% on Jan 1st, and then it was re-listened on Jan 3rd and played to 100% again. The only way that I can tell it was re-listened to is that it moved in the order.
