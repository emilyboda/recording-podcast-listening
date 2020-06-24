# Recording your podcast listening using Pocket Casts' Listening History feature
1. Copy get_history.py to your files
2. Add your token and filepath to get_history.py
3. Set get_history.py to run every hour (or whatever frequency you wish to measure your podcast listening)
4. Use parse_hist.py to parse the history once you have a few days recorded

# Note on the integrity of the data gathered
Since Pocket Casts' Listening History feature does not expose the actual date or time you listened to an episode, I am using the date and time that your script runs to guess the date that you listened. If your script fails to run, you will only know that you listened to the episode at some point after the last time you recorded and before the next time you recorded. No way around this. Because of this, I use the library "Notify" to alert myself if my script fails so I can (hopefully) fix it within the day.

# TO DO
* create an authorization script that can run on a failed status_code
