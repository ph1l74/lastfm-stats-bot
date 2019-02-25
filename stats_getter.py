import requests
import config


def get_top_artist(user_name, period):

        request_string = 'http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=' + user_name \
         + '&period=' + period + '&api_key=' + config.lastfm_api_key + '&format=json'
        req = requests.get(request_string)
        req_jsonified = req.json()
        result = []

        for aritst in req_jsonified['topartists']['artist']:
                result.append({'artist_name': aritst['name'],
                                'play_count': aritst['playcount'],
                                'image_URL': aritst['image'][1]['#text']})

        return result[:10]
