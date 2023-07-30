# imports
from discord_webhook import DiscordWebhook
import json
import time
from datetime import datetime


def main():
    # load config
    with open("config.json", 'r') as f:
        config = json.load(f)
    
    prev_time = 0
    while True:
        # create webhook
        webhook = hook(config)
        r = webhook.execute()
        print(r)
        # wait for next backup
        time.sleep(int(config["interval"]) * 3600)

    
def hook(config):
    #https://pypi.org/project/discord-webhook/
    # create webhook
    webhook = DiscordWebhook(url=config["webhook"], username="Backup")

    # length check for discord limitation
    if len(config["files"]) > 10:
        raise ValueError("Too many files to backup. Max is 10.")
    
    # add files to webhook
    for file in config["files"]:
        with open(file, "rb") as f:
            webhook.add_file(file=f.read(), filename=get_name(file))

    return webhook

def get_name(path):
    cur_time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = path.split("\\")[-1]
    return f"{cur_time}_{filename}"

if __name__ == "__main__":
    main()
    #debug()