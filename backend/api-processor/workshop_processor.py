#!/bin/python
# author SOMRC-ork8s
# date 2/5/18

import requests
import json
import yaml
from dateutil import parser
from datetime import datetime
from operator import itemgetter

response = requests.get('https://education.cadre.virginia.edu/api/workshop')

workshop_data_utf = response.json()

workshop_str = json.dumps(workshop_data_utf)

workshop_data = yaml.safe_load(workshop_str)

# ['workshops'][x] contains the title
# ['workshops'][x]['instructor']['display_name'] contains the instructor name
# ['workshops'][x]['sessions'][y]['date_time'] contains the date

# Fetch a list of all dates for all sessions
# Order them by date in ascending order
# Limit the results to top five

trimmed_workshop_list = []
date_today = datetime.now()
date_today - date_today.replace(tzinfo=None)

for workshop in workshop_data['workshops']:
    if(len(workshop['sessions']) > 0):
        id = workshop['id']
        title_str = workshop['title']
        display_name_str = workshop['instructor']['display_name']
        session_date = parser.parse(workshop['sessions'][0]['date_time'])
        session_date = session_date.replace(tzinfo=None)
        workshop_dict = {
            'id': id,
            'title_str': title_str,
            'display_name_str': display_name_str,
            'session_date': session_date
        }
        trimmed_workshop_list.append(workshop_dict)

sorted_workshop_list = sorted(trimmed_workshop_list, key=itemgetter('session_date'))

present_and_future_workshops_list = [workshop for workshop in sorted_workshop_list if workshop['session_date'] >= date_today]

present_and_future_workshops_list_top_five = present_and_future_workshops_list[:5]

for workshop in present_and_future_workshops_list_top_five:
    workshop['session_date'] = workshop['session_date'].strftime('%m/%d/%Y')

workshops_json_format = json.dumps(present_and_future_workshops_list_top_five)

print(workshops_json_format)
