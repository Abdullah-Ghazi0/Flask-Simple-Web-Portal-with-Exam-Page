import requests
import random
def memer():
    url = "https://www.reddit.com/r/ProgrammerHumor/top.json?limit=5&t=day"

    headers = {
        "User-Agent": "NewFlaskapp/2.0"
    }
    response = requests.get(url, headers=headers)

    data = response.json()
    memes = []

    for post in data["data"]["children"]:
        post_data = post["data"]

        if post_data["post_hint"] == "image":
            meme_data = {"title": post_data["title"], "image": post_data["url"] }

            memes.append(meme_data)


    meme = random.choice(memes) if memes else None
    return meme
