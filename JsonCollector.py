import requests
import time
import pickle

def save_obj(obj, filename):
    with open(filename + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(filename):
    with open(filename + '.pkl', 'rb') as f:
        return pickle.load(f)


class JsonCollector:
    def __init__(self, mintime, subreddit):
        self.url = "https://api.pushshift.io/reddit/search/submission/"
        self.subreddit = subreddit

        # the Unix times we have already searched. We searching from mintime to current,
        # updating each time we do it.
        self.min = mintime

        #contains dictionary keyed on postid, with value=json block
        self.data = {}


    def fetch_json(self, lower, upper):
        r = requests.get(
            self.url,
            params={
                "subreddit": self.subreddit,
                "before": upper,
                "after": lower,
                "size": 500
            }
        )
        assert r.status_code == 200
        return r.json()["data"]

    # Find posts starting at the subreddit's start, up to the current time
    def read_forward(self):
        jsonlist = self.fetch_json(self.min, int(time.time()))

        if jsonlist:
            # save the data
            for i in range(len(jsonlist)):
                self.data[jsonlist[i]["id"]] = jsonlist[i]
            self.min = jsonlist[-1]["created_utc"]
        return jsonlist

    def populate(self):
        while self.read_forward():
            display(len(self.data.keys()))
            # The pushshift api limit is apparently 3Hz.
            time.sleep(0.5)
