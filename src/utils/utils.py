import datetime
import json
import os
import random
import requests
from colorama import Fore, init
from discord_webhook import DiscordWebhook, DiscordEmbed
from typing import Union


init(autoreset=True)


# ---------------------------------------- Icons ---------------------------------------- #
class Icons:
    def __init__(self):
        self.DIOR = "https://cdn-vsh.prague.eu/object/617/44070910-1961871467200842-4640565116532686848-n.jpg"
        self.RTUNA = "https://avatars3.githubusercontent.com/u/38296319?s=460&u=ab0b4436b70c53941ac69aeba5ca21c5f1ed5379&v=4"


# ---------------------------------------- Colors ---------------------------------------- #
class Colors:
    def __init__(self):
        self.YELLOW = 0xFFFF00
        self.RED = 0xFF0000
        self.PURPLE = 0xAB79F2

        self.BONZAY = 0xAB79F2


# ---------------------------------------- Useragents ---------------------------------------- #
class Useragents:
    def __init__(self):
        self.mobile = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone12,1;FBMD/iPhone;FBSN/iOS;FBSV/13.3;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/Sprint]",
            "Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G570Y Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900 Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-N910F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 8.0.0;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/605.1",
            "Mozilla/5.0 (Android 8.0.0; Mobile; rv:61.0) Gecko/61.0 Firefox/68.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/23.0 Mobile/16B92 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPod Touch; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 9; AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36 OPR/55.2.2719",
            "Mozilla/5.0 (Windows Mobile 10; Android 8.0.0; Microsoft; Lumia 950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36 Edge/80.0.361.62",
        ]
        self.desktop = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/74.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/74.0",
            "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/74.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.62",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edge/44.18363.8131",
        ]

    def get_random_useragent(self, mobile: Union[bool, None] = None) -> str:
        """Gets a random useragent

        Arguments:
            mobile {bool} -- if true, returns a mobile useragent; if false, returns a desktop useragent; if unspecified, returns a random one.

        Returns:
            str -- Useragent string
        """
        if mobile is None:
            return random.choice(self.mobile + self.desktop)
        if mobile:
            return random.choice(self.mobile)
        else:
            return random.choice(self.desktop)


# ************************************************** FUNCTIONS ************************************************** #

# ---------------------------------------- Fundemental Functions ---------------------------------------- #
def get_time() -> str:
    """
    Simple function that returns a string containing info about current time and location.

    Returns:
        now {str}   - String in the format of '[time]'
    """
    now = str(datetime.datetime.now().time())
    # now = now[:-3] #[14:49:05.525]
    now = now[:-7]  # only want 3 decimal places
    return f"[{now}]"


def load_proxies(filename: str) -> Union[list, None]:
    """
    Reads proxies from a file and parses them to be ready to use with Python `requests` library

    Args:
        filename {str}                       - Name of the file (.txt) where are the proxies located
    Returns:
        formatted_proxy_list {list [dict]}  - List of dictionaries, that are formatted and ready-to-use with Python
        None                                - on Error

    Notes:
        *can be read from a file and split by a separator (usually new line)
    """

    with open(filename, "r") as f:
        file_contents = f.read()
        file_contents = file_contents.split("\n")
    formatted_proxy_list = []
    try:
        try:
            # Userpass
            for i in range(0, len(file_contents)):
                if ":" in file_contents[i]:
                    tmp = file_contents[i]
                    tmp = tmp.split(":")
                    proxies = {
                        "http": "http://" + tmp[2] + ":" + tmp[3] + "@" + tmp[0] + ":" + tmp[1] + "/",
                        "https": "http://" + tmp[2] + ":" + tmp[3] + "@" + tmp[0] + ":" + tmp[1] + "/",
                    }
                    formatted_proxy_list.append(proxies)
        except:
            # IP auth
            for n in range(0, len(file_contents)):
                if ":" in file_contents[n]:
                    temp = file_contents[n]
                    proxies = {"http": "http://" + temp, "https": "http://" + temp}
                    formatted_proxy_list.append(proxies)
    except:
        return None
    return formatted_proxy_list


def log_message(status: str, message: str, location: str = None, ) -> None:
    """
    A function to handle logging

    Args:
        status {str}    - Level of the logger - how problematic the message is, see Notes for special meanings
        message {str}   - Log message

    Returns:
        None

    Notes:
        Statuses with special meaning:
            - debug
            - info
            - warning
            - error
            - critical
    """
    if location:
        status = f"[{status.upper()}] ({location.upper()})"
    else:
        status = f"[{status.upper()}]"
    if status.lower().strip() == 'success':
        print(Fore.GREEN + f"{get_time()} {status} -> {message}")
    elif status.lower().strip() == 'error':
        print(Fore.RED + f"{get_time()} {status} -> {message}")
    else:
        print(f"{get_time()} {status} -> {message}")


# ---------------------------------------- File operating Functions ---------------------------------------- #
def read_file(filename: str) -> Union[str, dict, None]:
    """Reads from a file

    Args:
        filename: Name of the file

    Returns:
        dict: if the file is json
        str:  if the file is txt
        None: on error
    """
    try:
        file_type = filename.split(".")[-1]
        if file_type == "json":
            if os.stat(filename).st_size == 0:
                return {}
            with open(filename, "r") as f:
                j = json.load(f)
            return j

        elif file_type == "txt":
            with open(filename, "r") as f:
                return f.read()
        else:
            return None
    except Exception as e:
        raise e


def test_proxy(url: str, proxy: dict, headers: dict) -> bool:
    """
    A simple proxy tester to make sure a proxy is working (can see) on a website.

    Args:
        url     - URL where you want to test the proxy
        proxy   - Proxy that you want to test
        headers - Headers that you want to test with the proxy

    Returns:
        True or False
    """
    test = requests.get(url=url, headers=headers, proxies=proxy)
    if test.status_code in (302, 200):
        return True
    else:
        return False


def notify_entry(webhook_url: str, name: str, email: str, phonenum: str or int, location: str, mode: int) -> None:
    """
    Notifies a successful raffle entry.

    :param mode: Mode used for entering
    :param webhook_url: Url of a discord webhook
    :param name: Name that was used to enter the raffle
    :param email: Email that was used to enter the raffle
    :param phonenum: Phone number that was used to enter the raffle
    :param location: Location that was used to enter the raffle
    :return:
    """
    i = Icons()
    c = Colors()
    # ---------- Initializing time ---------- #
    now = str(datetime.datetime.utcnow().time())[:-5]

    # ---------- Initializing webhook ---------- #
    hook = DiscordWebhook(url=webhook_url, username="Dior Raffle bot", avatar_url=i.DIOR, )

    # ---------- Initializing embed ---------- #
    embed = DiscordEmbed(
        title="Dior raffle successfully entered! 🥳",
        url="https://github.com/rtunazzz/DiorRaffleBot",
        color=c.BONZAY,
    )
    if mode == 1:
        mode = '**YOLO**'
    else:
        mode = 'Safe'
    embed.add_embed_field(name="Mode", value=mode)
    embed.add_embed_field(name="Name", value=name)
    embed.add_embed_field(name="Email", value=f"||{email}||", inline=False)
    embed.add_embed_field(name="Phone Number", value=f"||{phonenum}||", inline=False)
    embed.add_embed_field(name="Location", value=location)

    # ---------- Setting author ---------- #
    embed.set_footer(text="@rtunazzz on Twitter", icon_url=i.RTUNA)

    hook.add_embed(embed)
    return hook.execute()
