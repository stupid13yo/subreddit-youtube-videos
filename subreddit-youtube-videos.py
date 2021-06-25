import sys
import time
import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Check command-line arguments
if len(sys.argv) != 2:
    print('Usage: python3 script.py subreddit [before]')

subreddit = sys.argv[1]
try:
    initial_before = sys.argv[2]
except IndexError:
    initial_before = int(time.time())

# Settings
YOUTUBE_DOMAINS = ['youtu.be', 'youtube.com']

# Run script
print(f'Writing YouTube video urls to {subreddit}.txt')

# New requests session
s = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
s.mount('https://', HTTPAdapter(max_retries=retries))

for domain in YOUTUBE_DOMAINS:
    before = initial_before
    
    while True:
        url = f'https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&domain={domain}&size=500&before={before}&fields=id,url,created_utc'
        print(url)
        res = s.get(url)
        
        try:
            data = res.json()['data']
        except:
            print(res.status_code)
            print(res.text)
            exit()

        if len(data) < 1:
            break # no more posts
        
        urls = []

        for post in data:
            urls.append(post['url'])
            before = post['created_utc']
        
        with open(f'{subreddit}.txt', 'a+') as f:
            f.write('\n'.join(urls) + '\n')
        
        urls = None
        
        time.sleep(5)
