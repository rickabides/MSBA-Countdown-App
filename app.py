from flask import Flask, render_template
from datetime import datetime
import os
import pytz

app = Flask(__name__)

# Environment variables or default values for start and end times
start_time_str = os.getenv('START_TIME', '2023-08-22 12:00:00')
end_time_str = os.getenv('END_TIME', '2024-08-10 17:00:00')

# Set pacific time
pacific_tz = pytz.timezone('America/Los_Angeles')

# Convert start and end times to datetime objects and localize them to Pacific time
start_time = pacific_tz.localize(datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S'))
end_time = pacific_tz.localize(datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S'))

class_dates = ['2024-05-13', '2024-05-15', '2024-05-18', '2024-05-20', '2024-05-22', '2024-05-28', '2024-05-29', '2024-06-01','2024-06-03', '2024-06-05',
              '2024-06-08', '2024-06-10', '2024-06-12', '2024-06-17', '2024-06-20', '2024-06-22', '2024-06-24', '2024-06-26', '2024-06-29',
              '2024-07-08', '2024-07-10', '2024-07-13', '2024-07-15', '2024-07-17', '2024-07-22', '2024-07-24', '2024-07-27', '2024-07-29',
              '2024-07-31', '2024-08-05', '2024-08-07', '2024-08-10']

# Countdown timer and index route. Pin to pacific time
@app.route('/')
def countdown():
    now = datetime.now(pacific_tz)
    special_congrats_time = pacific_tz.localize(datetime(2024, 8, 10, 17, 1, 0))

    # Check if the current time has reached the special congrats time
    if now >= special_congrats_time:
        return render_template('congrats.html')

    total_seconds = int((end_time - now).total_seconds())
    
    # Ensure the countdown doesn't go negative
    if total_seconds < 0:
        total_seconds = 0

    remaining_days = total_seconds // 86400
    remaining_hours = (total_seconds % 86400) // 3600
    remaining_minutes = (total_seconds % 3600) // 60
    remaining_seconds = total_seconds % 60

    return render_template('countdown.html',
                           days=remaining_days,
                           hours=remaining_hours,
                           minutes=remaining_minutes,
                           seconds=remaining_seconds)


# Return one page or another based on date
@app.route('/dowehaveclass')
def do_we_have_class():
    today = os.getenv('TODAY', datetime.now(pacific_tz).strftime('%Y-%m-%d'))
    if today in class_dates:
        return render_template('wehaveclass.html')
    else:
        return render_template('noclass.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
