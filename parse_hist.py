import json
import os
import datetime
import math

history_file_path = "/home/pi/pocket-casts-hist/history/"
graph_choice = 'hours' # do you want to view the metrics by date or by hour and date? choose 'hours' or 'days'

def debug_episode(uuid, history):
    for date in history:
        for episode in date['episodes']:
            if episode['uuid'] == uuid:
                print(date['date/time string'])
                print(json.dumps(episode, indent=3))

def get_history_from_files(path):
    ## IMPORT ALL FILES FROM /history
    history = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            with open(path+filename,'r') as f:
                eps = json.load(f)
                dt_str = filename[0:len(filename)-5]
                eps['date/time string'] = dt_str
                eps['date/time object'] = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
                history.append(eps)
    history = sorted(history, key = lambda episode: episode['date/time object'])
    """
    EXAMPLE
    history =   [
                    {
                       "date/time string": "2020-06-24 12:00",
                       "date/time string": datetime.datetime(2020,6,24,12,0,0),
                       "total": 100, #num of eps
                       "episodes":
                            [
                                {
                                   "uuid": "163966d2-043f-4118-b934-e1bd2f8545be",
                                   "url": "https://dts.podtrac.com/redirect.mp3/whyy-od.streamguys1.com/thewhy/20200615THEWHY.mp3",
                                   "published": "2020-06-15T19:30:01Z",
                                   "duration": 1199,
                                   "fileType": "audio/mp3",
                                   "title": "Reckoning with Frank Rizzo\u2019s legacy",
                                   "size": "19186271",
                                   "playingStatus": 3,
                                   "playedUpTo": 1199,
                                   "starred": false,
                                   "podcastUuid": "72f77760-b3a6-0136-7b93-27f978dac4db",
                                   "podcastTitle": "The Why: Philly Explained",
                                   "episodeType": "full",
                                   "episodeSeason": 0,
                                   "episodeNumber": 0,
                                   "isDeleted": true,
                                   
                                },
                                {
                                    same as above
                                }
                            ]
                    },
                    {
                        the next date/time goes here
                    }
                ]
    """
    return history
    
def get_unique_uuids(history):
    """
        This is a complicated section. The idea is that history is set up 
        with the dates goes from oldest to newest and that the episode
        order within each date/time is set up from most recently listened
        to listened a long time ago.
        
        Using this order, we can assume that, going through the arrays/dicts
        from 0 to len(), the first time an episode's uuid shows up will be 
        the last time you listened to that episode. However, if you start
        an episode, pause it, listen to some other episodes, and then go back
        and listen to some more of that episode, this will no longer be true.
        
        To get around this, I set the played date as the first time I see the
        uuid. Then, every subsequent time I check to see if the playedUpTo time
        has increased. If it has, it means you've played more of the podcast and
        I replace that 'played date' with the new date.
        
        This will probably fall apart if you are the kind of person who
        re-listens to podcasts frequently and you'd like to record both listens.
        I think the only way around this would be to say something like "if the
        old played date is greater than X days ago, add this episode like it's
        a new episode". But I don't feel like defining X and I'm happy with
        where I'm at right now.
    """
    
    uuids = {}
    for date in history:
        for episode in date['episodes']:
            if episode['uuid'] not in uuids:
                uuids[episode['uuid']] ={'data':episode,'title':episode['title'],'played date':date['date/time string'], 'all dates':[date['date/time string']]}
            else:
                if uuids[episode['uuid']]['data']['playedUpTo'] == episode['playedUpTo']:
                    uuids[episode['uuid']]['all dates'].append(date['date/time string'])
                else:
                    uuids[episode['uuid']]['played date'] = date['date/time string']
                    uuids[episode['uuid']]['data'] = episode
                    uuids[episode['uuid']]['all dates'].append(date['date/time string'])
    """
    EXAMPLE
    a dictonary, one entry for each episode uuid
    uuids = {
                "jfdslkjfsk3348549994":  # this is the episode's uuid
                    {
                        "data": {full episode object from history},
                        "title": "Reckoning with Frank Rizzo\u2019s legacy",
                        "played date": "2020-06-24 12:00", # this is hopefully the date/time hour string you finished the podcast
                        "all dates": ["2020-06-24 12:00", "2020-06-24 11:00"] # this is all the date/time hour strings the episode shows up on, just for debuggnig purposes
                    },
                "32jio32okj4i3ojk342":  # new episodes uuid
                    { same as above, but for a new episode}
            }
    """
    return uuids

def get_dates_from_files(path):
    # this returns all the filenames in /hist as datetime objects so we can use it for our plotting later
    x_dates = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            x_dates.append(datetime.datetime.strptime(filename,"%Y-%m-%d %H:%M.json"))
    x_dates = sorted(x_dates)
    return x_dates

def get_unique_dates(uuids):
    # this takes the previous dict that was a compliation of all the unique episode information
    # it will return a dict that is a compliation of all the eps you've listened to per each hour timestamp
    dates = {}
    for episode in uuids:
        if uuids[episode]['played date'] not in dates:
            dates[uuids[episode]['played date']] = {'episodes':{episode:uuids[episode]['data']}}
        else:
            if episode not in dates[uuids[episode]['played date']]['episodes']:
                dates[uuids[episode]['played date']]['episodes'][episode] = uuids[episode]['data']
    x_dates = get_dates_from_files(history_file_path)
    first_date = x_dates[0].strftime('%Y-%m-%d %H:%M')
    del dates[first_date]
    """
    EXAMPLE
    a dictonary, one entry for each hour timestamp
    dates = {
                "2020-06-23 23:00":  
                    {
                        'episodes':
                            {
                                "jfdslkjfsk3348549994":{full episode object from history},
                                "243fdslkjfsk33454322cs994":{full episode object from history}
                            }
                    }
                "2020-06-24 00:00":  
                    {
                        'episodes':
                            {
                                "rfewdslkjfs5435432219994":{full episode object from history},
                                "ssdfgdsfsk34322cs994":{full episode object from history}
                            }
                    }
            }
    """
    return dates


def get_date_metrics(dates, hd):
    metrics = {}
    if hd == "hours":
        for d in dates:
            dur = 0
            for ep in dates[d]['episodes']:
                dur = dur + dates[d]['episodes'][ep]['playedUpTo']
            dobj = datetime.datetime.strptime(d, "%Y-%m-%d %H:%M")
            metrics[dobj] = {'num of episodes':len(dates[d]['episodes']), 'duration':dur, 'date object':datetime.datetime.strptime(d,"%Y-%m-%d %H:%M")}
    elif hd == "days":
        for d in dates:
            dur = 0
            for ep in dates[d]['episodes']:
                dur = dur + dates[d]['episodes'][ep]['playedUpTo']
            dobj = datetime.datetime.strptime(datetime.datetime.strptime(d, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d"),"%Y-%m-%d")
            if dobj not in metrics:
                metrics[dobj] = {'num of episodes':len(dates[d]['episodes']), 'duration':dur, 'date object':dobj}
            else:
                metrics[dobj]['num of episodes'] = metrics[dobj]['num of episodes'] + len(dates[d]['episodes'])
                metrics[dobj]['duration'] = metrics[dobj]['duration'] + dur
    """
    EXAMPLE
    the status of each timestamp. hd will choose if you want to return the data in hourly timestamps, or in daily timestamps
    metrics = {
                "2020-06-23":  
                    {
                        'num of episodes': 33,
                        'duration': 6435646 # in minutes
                    }
                "2020-06-24":  
                    {
                        'num of episodes': 4,
                        'duration': 4333 # in minutes
                    }
            }
    """
    return metrics

def format_for_graph(metrics, hd):
    # this will return three arrays that you can plot the data with
    y_num = []
    y_dur = []
    if hd == 'hours':
        x_dates = get_dates_from_files(history_file_path)
        for x in x_dates:
            try:
                y_num.append(metrics[x]['num of episodes'])
                y_dur.append(round(metrics[x]['duration']/60,1))
            except:
                y_num.append(0)
                y_dur.append(0)
    elif hd == "days":
        x_dates = []
        for d in metrics:
            x_dates.append(d)
        x_dates = sorted(x_dates)
        for x in x_dates:
            y_num.append(metrics[x]['num of episodes'])
            y_dur.append(round(metrics[x]['duration']/60,1))
    return x_dates, y_num, y_dur

history = get_history_from_files(history_file_path)
uuids = get_unique_uuids(history)
print('total episodes found:', len(uuids))
dates = get_unique_dates(uuids)

metrics = get_date_metrics(dates,graph_choice)
x_dates, y_num, y_dur = format_for_graph(metrics, graph_choice)

print('')
print('listening metrics:')

print('date/time stamp      ','\t','# eps','\t','dur(mins)')
for x in range(len(x_dates)):
    print(x_dates[x],'\t',y_num[x],'\t',y_dur[x])

print('')
print('IMPORTANT NOTE:')
print('Due to a quirk with how podcast listening is recorded, this script is unable')
print('to determine which episodes were listened to during the first hour of recording.')
"""
NOTES

"playingStatus":
3: archived
2: unfinished

"podcastUuid": unique id for podcasts
"uuid": unique id for episode
"""
