import random, sys
from checkid import *
from fake_useragent import UserAgent
from selenium.common.exceptions import TimeoutException
ua = UserAgent()

def save_id(id):
    try:
        with open("ids.txt", "a+") as f:
            f.write(str(id)+"\n")
        print(f"Saved ID : {id}")
    except Exception as e:
        print(f"Could not save ID : {e}")

def gen_id(profile="modern"):
    if profile == "retro":
        return random.randint(1, 9999) * 10
    elif profile == "classic":
        return random.randint(10000, 99999) * 10
    elif profile == "modern":
        return random.randint(100000, 350000) * 10
    else:
        raise ValueError("Profile must be one of those : 'retro', 'classic' or 'modern'.")

profiles = ['retro', 'classic', 'modern']
#check_urls = ["https://store.steampowered.com/app/<appid>/", "https://steamdb.info/app/<appid>/"]

def proc():
    appid = gen_id(random.choice(profiles))
    print(f"Testing AppID : {appid}")
    try:
        # isvalid = check_id(random.choice([f"https://store.steampowered.com/app/{appid}/", f"https://steamdb.info/app/{appid}/"]))
        isvalid = check_id(f"https://store.steampowered.com/app/{appid}/")
    except TimeoutException as e:
        print(f"Timeout reached : {e}")
        isvalid = False
    # isvalid = check_id(random.choice(["https://store.steampowered.com/app/{appid}/", "https://steamdb.info/app/{appid}/"]), appid)
    if isvalid == True:
        print(f"Valid AppID found! ID : {str(appid)}. Saving it now...")
        save_id(appid)
        return
    else:
        print("AppID invalid, continuing...")
        return

def main():
    print("Will start generating after your confirmation.\nPress CTRL + C to stop the generation proccess.")
    input("PRESS ENTER TO START...")
    while True:
        try:
            proc()
            timeout = random.uniform(1.5645745, 8.94245)
            print(f"Entering cooldown to prevent WAF trigger... (Timeout in seconds : {timeout}.)")
            time.sleep(timeout)
        except KeyboardInterrupt:
            print("Ctrl + C recieved, stopping now!")
            break
    print("\nSuccessfully stopped generating.")
    input("Press enter to exit...")
    sys.exit()

if __name__ == "__main__":
    main()

"""
I don't think I'll need this in fact.
steam_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "store.steampowered.com",
    "Priority": "u=0, i",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": ua.random
}
steamdb_headers = {}"""