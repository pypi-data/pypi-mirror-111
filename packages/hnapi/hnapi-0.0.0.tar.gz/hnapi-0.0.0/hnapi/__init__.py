import requests

class hackernews:
    def __init__(self, user_agent):
        self.headers = {'User-agent': user_agent}

    def get(self, endpoint):
        url = f'https://hacker-news.firebaseio.com/v0/{endpoint}.json'
        r = requests.get(url,headers=self.headers)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception(r.json()['error'])

    def item(self,item_id):
        return self.get('item/'+str(item_id))

    def user(self, username):
        return self.get('user/'+username)

    def max_item(self):
        return self.get('maxitem')
    
    def get_stories(self,kind=None):
        kinds = ['new','top','best','ask','show','job']
        if kind in kinds:
            return self.get(kind+'stories')
        else:
            raise Exception('Bad `kind` argument')

    def changed_items(self):
        return self.get('updates')['items']

    def changed_profiles(self):
        return self.get('updates')['profiles']
