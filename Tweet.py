import json
from dateutil.parser import parse
from pytz import timezone
import re
import sys
import io
import codecs

class Tweet:
    user_id = None
    tw = None
    local_media_path = None

    def __init__(self, twitter_data_path, twitter_user_id):
        self.user_id = twitter_user_id
        with codecs.open(twitter_data_path + '/data/tweets.js', 'r' , 'utf-8', 'ignore') as f:
            data = f.read()
        self.tw = json.loads(data[data.find('['):])
        self.local_media_path = twitter_data_path + '/data/tweets_media/'

    def call(self):
        # self.__tweets_list()
        pass

    def call_with_pictures(self):
        tl = self.__tweets_list(exclude_retweet=True)
        return self.__tweets_with_pictures(tl)
        
    '''
    return list(dict)
    
    dict.keys
    text: tweet_text
    created_at: tweet_datetime
    url: tweet url
    retweet: retweet count
    fav: fav counts
    media: pictures
    '''
    def __tweets_list(self, exclude_retweet = False):
        tweets_list = []

        for t in self.tw:
            d = {
                'text': self.__tweet_text(t),
                'created_at': self.__tweet_datetime(t),
                'url': self.__tweet_url(t),
                'retweet': self.__retweet_count(t),
                'fav': self.__fav_count(t),
                'media': self.__media_local_urls(t),
            }
            if exclude_retweet and self.is_retweet_by_me(t):
                pass
            else:
                tweets_list.append(d)

        return tweets_list


    '''
    return list(list)
    list[text, created_at, url, retweet, fav, media]
    '''
    def __tweets_with_pictures(self, tweets_list):
        media_list = []
        
        # python の for は順番を制限しないので厳密な記載ではないが、手元で動かした感じはまあ動いてそう
        sorted_tw_list = sorted(tweets_list, key=lambda x:x['created_at'], reverse=True)
        
        for t in sorted_tw_list:
            media_size = len(t['media'])
            if media_size == 0:
                pass
            elif media_size == 1:
                tmp = [
                    t['text'],
                    t['created_at'],
                    t['url'],
                    t['retweet'],
                    t['fav'],
                    t['media'][0]
                ]
                media_list.append(tmp)
            else:
                for m in t['media']:
                    tmp = [
                        t['text'],
                        t['created_at'],
                        t['url'],
                        t['retweet'],
                        t['fav'],
                        m
                    ]
                    media_list.append(tmp)
        # sorted_tw_list = sorted(tweets_list, key=lambda x:x['fav'], reverse=True)
        
        return media_list

    def __tweet_text(self, t):
        s = t['tweet']['full_text']
        e = t['tweet']['entities']
        if 'urls' in e:
            for u in e['urls']:
                if 'expanded_url' in u:
                    s = s.replace(u['url'], u['expanded_url'])
        s = s.replace("\n", " ")
        s = s.replace("\r", " ")
        return s

    def __tweet_url(self, t):
        return "https://twitter.com/" + self.user_id + "/status/" + t['tweet']['id']

    def __tweet_datetime(self,t):
        return parse(t['tweet']['created_at']).astimezone(timezone('Asia/Tokyo')).strftime("%Y-%m-%d %H:%M:%S")

    def __retweet_count(self, t):
        return int(t['tweet']['retweet_count'])

    def __fav_count(self, t):
        return int(t['tweet']['favorite_count'])

    def __media_local_urls(self, t):
        if not 'extended_entities' in t['tweet']:
            return []
        if not 'media' in t['tweet']['extended_entities']:
            return []
        if len(t['tweet']['extended_entities']['media']) < 1:
            return []
        ms = []
        id_str = t['tweet']['id_str']
        for m in t['tweet']['extended_entities']['media']:
            tmp = m['media_url']
            tmp = tmp.replace('http://pbs.twimg.com/media/', '')
            tmp = self.local_media_path + id_str + '-' + tmp
            ms.append(tmp)
        return ms

    def is_retweet_by_me(self, t):
        """
        文字列sが「RT @」から始まるかどうかを判定する == そのツイートがリツイートしたものかを判定する
        「RT @」から始まる場合はTrueを、そうでない場合はFalseを返す。
        """
        return t['tweet']['full_text'].startswith("RT @")

