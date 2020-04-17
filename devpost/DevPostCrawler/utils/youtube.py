# -*- coding: utf-8 -*-

import json
import os
import os.path
import re
import time

import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"

DEVELOPER_KEY = "AI...mw"  # TODO: Change me!


def fetch_video_id(url):
    yt_embed_regex = r"v\=(.*)"
    fa = re.findall(yt_embed_regex, url)
    print(fa)
    if len(fa) > 0:
        return fa[0]
    else:
        return None


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def save_json(filename, dict_video):
    json_str = json.dumps(dict_video)
    f = open(filename, 'w')
    f.write(json_str + '\n')
    f.close()
    print(f"Saved {filename}")


def main():
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    df = pd.read_json('../../projects.jl', lines=True).drop(['storyHTML'], axis=1)

    for video_url in df['video']:
        try:
            if video_url:
                video_id = fetch_video_id(video_url)
                if video_id:
                    filename = f'../../out/yt/{video_id}.json'
                    if not os.path.isfile(filename):
                        print(f"Going to fetch video information for {video_url}...")
                        request = youtube.videos().list(
                            part="snippet,contentDetails,statistics",
                            id=video_id
                        )
                        response = request.execute()
                        if response['items'] and len(response['items']) > 0:
                            save_json(filename, response['items'][0])
                        time.sleep(0.55)  # FIXME: might not be necessary
                    else:
                        print(f"Already have download {filename}, skipped")
        except:
            print(f"Problem with {video_url}")


if __name__ == "__main__":
    main()
