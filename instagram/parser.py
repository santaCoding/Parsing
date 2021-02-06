from InstagramAPI import InstagramAPI
import time
import sys
import traceback
import pandas as pd
import datetime

class MyInstaCrawler(InstagramAPI):
    def __init__(self, username, password):
        super().__init__(username, password)

    def getTotalFollowers(self, usernameId):
        import datetime
        next_max_id = ''
        followers = []
        while 1:
            try:
                if self.getUserFollowers(usernameId, next_max_id):
                    temp = self.LastJson
                    for item in temp["users"]:
                        followers.append(item)
                    print('Followers: %s ' % len(followers))
                    temp['collected_date'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    if temp.get("big_list") is None:
                        return followers
                    elif temp['big_list'] is False:
                        return followers
                    next_max_id = temp["next_max_id"]
            except:
                print(traceback.format_exc())
                print("Sleeping 10 secs")
                time.sleep(10)
                
usr = str(input('Enter your login: '))
pasw = str(input('Enter your password: '))
ic = MyInstaCrawler(usr, pasw)
ic.login()
arg = str(input('Enter instagram account ID that will be parsed: '))
args = []
args.append(arg)
total_results = []
for arg in args:
    try:
        arg = int(arg)
        results = ic.getTotalUserFeed(arg)
        if results is None:
            print('Some problems with id %s. No results.' % arg)
            continue
        print('Gathered %s media, saving...' % len(results))
        if len(results) != 0:
            username = results[0]['user']['username']
            for r in results:
                try:
                    reduced_r = {}
                    date = datetime.datetime.fromtimestamp(r['taken_at'])
                    date = date.strftime("%Y-%m-%d"'T'"%H:%M:%S"'Z')
                    caption = r['caption']
                    caption_text = ''
                    if caption is not None:
                        caption_text = caption['text']
                    view_count = 0
                    if r['media_type'] == 2:
                        if r.get('view_count'):
                            view_count = int(r['view_count'])
                    reduced_r['created_time'] = date
                    reduced_r['user.username'] = username
                    reduced_r['caption.text'] = caption_text
                    reduced_r['comments.count'] = r['comment_count']
                    reduced_r['link'] = 'https://instagram.com/p/' + r['code']
                    total_results.append(reduced_r)
                except Exception as e:
                    print(e)
            print('Finished for %s, id: %s' % (username, arg))
    except ValueError:
        print("Pass ID as an argument. Couldn't transform to int")
    except:
        print(traceback.format_exc())
df = pd.DataFrame(total_results)
df.to_csv('Database %s.csv' % datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S"))