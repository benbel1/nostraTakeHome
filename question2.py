import json

with open('payload.json') as data:
    payload=json.load(data)

#Calculating Metrics by their definition
ttfb = payload["response_start"] - payload["navigation_start"]

dom_content_loaded_time = payload["dom_content_loaded_event_end"] - payload["navigation_start"]

page_load_time = payload["load_event_end"] - payload["navigation_start"]

# Print the results
print(f"Time to First Byte (TTFB): {ttfb} ms")
print(f"DOM Content Loaded Time: {dom_content_loaded_time} ms")
print(f"Page Load Time: {page_load_time} ms")
