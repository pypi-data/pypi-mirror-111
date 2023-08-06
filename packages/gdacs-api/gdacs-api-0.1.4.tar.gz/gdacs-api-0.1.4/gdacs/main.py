from api import GDACSAPIReader

client = GDACSAPIReader()

# get latest events
# latest_events = client.latest_events(event_type="EQ", historical="24h", limit=1000)
# print(latest_events)

# get single event
# event = client.get_event(event_type='TC', event_id='1000132', episode_id='8')
event = client.get_event(event_type='DR', event_id='1012428', episode_id='9', source_format='geojson', cap_file=False)
# event = client.get_event(event_type='DR', event_id='1012428', source_format='geojson')
print(event)