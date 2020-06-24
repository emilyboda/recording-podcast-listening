Here is the information you can get about one episode from Pocket Casts' Listening History API.

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

The webplayer also does not give us this information:
<p align="center">
<img src="https://github.com/emilyboda/recording-podcast-listening/blob/master/webplayer%20listening%20history%20screenshot.PNG" width="900"><img 
</p>
   
Thankfully, the array that is returned by the API _is_ in chronological order. Using this order, and by pulling this listening history every hour of the day, I can determine which hour of the day I finished listening to an episode. However, if I finish a 2.5 hour long episode at 1:13 pm, my data will tell me that I listened to 2.5 hours of episodes at 2:00 pm.

While I could correct this by telling my script that I listened to 0.5 hours at 12:00 pm, 1 hr at 1:00 pm, and 1 hr at 2:00 pm, but this is still not very accurate.

I prefer to record the data every hour of the day, and then display my data on a graph by the day.
