import requests
from bs4 import BeautifulSoup
import random
import names
from colorama import Fore, Style, init
import threading

from src.utils.utils import log_message, read_file, Useragents, load_proxies, notify_entry

init(autoreset=True)


class Diorerrr:
    """
    Diorerrr class that hold all related variables/methods to entering the Air Dior raffle
    """

    def __init__(self) -> None:
        self._load_personal_data()
        self._validate_size()
        self._setup()

        try:
            try:
                self.proxies = load_proxies("./data/proxies.txt")
            except ValueError:
                self.proxies = load_proxies("../data/proxies.txt")
        except FileNotFoundError:
            log_message("Error", "Proxy file not found.")
            exit()

    def _load_personal_data(self) -> None:
        """
        Loads data from the coofig.json file
        :return:
        """
        # Loading data
        try:
            try:
                self.USERDATA = read_file("./data/config.json")
            except FileNotFoundError:
                self.USERDATA = read_file("../data/config.json")
        except FileNotFoundError:
            log_message("Error", "File config.json not found.")
            exit()
        self.webhook: str = self.USERDATA["Webhook"]
        self.shoe_size: str or int = self.USERDATA["UK Shoe size"]

        personal = self.USERDATA["Personal"]
        self.title: str = personal["Title"]
        self.first_name: str = personal["First name"]
        self.last_name: str = personal["Last name"]
        self.catchall: str = personal["Catchall"]
        self.phone_code: str = personal["Phone code"]

        if '@' in self.catchall:
            self.catchall = self.catchall.replace('@', '')

        self.country_code = self.USERDATA["Country Code of Residence"]

    def _validate_size(self) -> None:
        """
        Validates that the shoe size specified is a valid shoe size
        :return:
        """
        if str(self.shoe_size) == "random":
            return
        try:
            self.shoe_size == int(self.shoe_size)
        except ValueError:
            log_message("Error", "Check your config.json file and make sure your Shoe size is correct. It should be "
                                 "just a number, for example: '6' for UK 6.")
            return

    def _select_instore_location(self, r: requests.Response) -> None:
        """
        Parses and prompts the user to select an instore location where he'll be picking up his W
        :param r: Response object after GET requesting https://capsule.dior.com/en/enter/hi/
        :return:
        """
        #  =================== Selecting the instore pickup location ===================
        print()
        print("------------", Style.BRIGHT + "SELECT PICKUP LOCATION: ", Style.NORMAL + "------------")
        location_options = {1: "Europe & Middle East",
                            2: "North America",
                            3: "Japan",
                            4: "Asia & Australia"}
        for key, val in location_options.items():
            print(Fore.CYAN + f"{key}. - {val}")

        location_select = None
        try:
            location_select = int(input("Select your preferred collection location:\n"))
        except ValueError:
            pass
        while not isinstance(location_select, int):
            print(location_select)
            location_select = input("Please enter a number between 1 and 4.\n")
            try:
                if int(location_select) in range(0, 4):
                    location_select = int(location_select)
                    break
                else:
                    continue
            except ValueError:
                continue
        preferred_location = location_options[location_select]
        print(Fore.GREEN + f"{preferred_location} it is.")

        #  =================== Instore location pt 2 ===================
        soup = BeautifulSoup(r.text, "lxml")
        select_html = soup.find("select", {"id": "locationSelect"})
        # need to get the locationIds
        options = select_html.find("optgroup", {"label": preferred_location})
        print()
        print("------------", Style.BRIGHT + "SELECT PICKUP LOCATION: ", Style.NORMAL + "------------")
        pickup_options = {}
        for i, option in enumerate(options, 1):
            print(Fore.CYAN + f"{i}. - {option.text}")
            pickup_options[i] = option["value"]
        pickup_select = ""
        try:
            pickup_select = int(input("Select your preferred collection location:\n"))
        except ValueError:
            pass
        while not isinstance(pickup_select, int):
            print(pickup_select)
            pickup_select = input(f"Please enter a number between 1 and {len(pickup_options)}.\n")
            try:
                if int(pickup_select) in range(0, len(pickup_options)):
                    pickup_select = int(pickup_select)
                    break
                else:
                    continue
            except ValueError:
                continue
        print(Fore.GREEN + f"{pickup_options[pickup_select]} it is.")
        self.pickup = pickup_options[pickup_select]

    def _setup(self) -> None:
        """
        Sets up all variables for the raffle
        :return:
        """
        self._select_mode()
        if self.mode == 1:
            try:
                try:
                    self.phone_nums = read_file("./data/numbers.txt")
                except ValueError:
                    self.phone_nums = read_file("../data/numbers.txt")
            except FileNotFoundError:
                log_message("Error", "Proxy file not found.")
                exit()
        #  =================== Entering for low or highs ===================
        self.style = str(input("Would you like to enter for the Highs, or the Lows?\n"))
        while 'low' not in self.style.lower().strip() and 'high' not in self.style.lower().strip():
            self.style = str(input("Enter either 'Highs', or 'Lows'...\n"))
        self.style = self.style.lower().strip()
        self.raffle_url = ''
        if 'low' in self.style:
            self.raffle_url = "https://capsule.dior.com/en/enter/low/"
        else:
            self.raffle_url = "https://capsule.dior.com/en/enter/hi/"

        r = None
        try:
            r = requests.get(self.raffle_url, headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "User-Agent": Useragents().get_random_useragent(),
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,cs;q=0.7,de;q=0.6",
                "Cache-Control": "max-age=0",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            })
        except ConnectionError:
            log_message("ERROR", "Connection error. Try again later.")
            exit()

        if r.status_code not in range(200, 210):
            log_message("Error", "Failed to retrieve raffle URL.")
            exit()

        #  =================== Selecting instore location ===================
        self._select_instore_location(r)

    def _jig_info(self) -> None:
        """
        Jigs info based on the user settings in config.json file
        :return:
        """
        if str(self.shoe_size).strip().lower() == "random":
            sizes = [3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14,
                     14.5, 15]
            self.shoe_size = random.choice(sizes)
        if self.title.strip().lower() == "random":
            self.title = random.choice(["Mr.", "Mrs."])
        if self.first_name.strip().lower() == "random":
            self.first_name = names.get_first_name()
        if self.last_name.strip().lower() == "random":
            self.last_name = names.get_last_name()

    def _get_payload(self, useragent: str) -> dict:
        """
        Generates and returns a dictionary object, that will be used as payload for our POST raffle request
        :param useragent: UserAgent string
        :return:
        """
        self.email = f"{self.first_name}.{self.last_name}{random.randint(1, 999)}@{self.catchall}"
        if self.mode == 1:
            self.phone_num = random.choice(self.phone_nums)
        else:
            self.phone_num = f"{self.phone_code} {random.randint(111, 999)}-{random.randint(111, 999)}-{random.randint(111, 999)}"

        return {"style": "high",
                "locationId": "london-selfridges",
                "size": str(self.shoe_size),
                "title": self.title,
                "firstName": self.first_name,
                "lastName": self.last_name,
                "firstNameKanji": "",
                "lastNameKanji": "",
                "firstNameKana": "",
                "lastNameKana": "",
                "email": self.email,
                "tel": self.phone_num,
                "countryOfResidence": self.country_code.upper(),
                "emailOptIn": "1",
                "ack18": "1",
                "ackRules": "1",
                "userAgent": useragent,
                "lang": "en",
                "telCountryCode": self.phone_code.replace('+', '')}

    def _enter(self) -> None:
        """
        Handles everything related to entering (sending the entry request)
        :return:
        """
        self._jig_info()
        useragent = Useragents().get_random_useragent()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": useragent,
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,cs;q=0.7,de;q=0.6",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Origin": "https://capsule.dior.com",
            "Referer": self.raffle_url
        }
        s = requests.Session()
        if self.proxies:
            s.proxies.update(random.choice(self.proxies))
        s.headers.update(headers)

        payload = self._get_payload(useragent)

        p = s.post("https://api.sorchid.com/submit", json=payload)
        if p.status_code in range(200, 210):
            log_message("Success", f"[{p.status_code}] - Successfully entered raffle.")
            if self.webhook.strip():
                notify_entry(self.webhook,
                             f"{self.first_name} {self.last_name}",
                             self.email,
                             self.phone_num,
                             self.pickup,
                             self.mode)
        else:
            log_message("Error", f"[{p.status_code}] - Failed to enter. {p.reason}")

    def _select_mode(self) -> None:
        """
        Handles everything around selecting the entry mode
        :return:
        """
        mode = None
        print("------------", Style.BRIGHT + "MODES: ", Style.NORMAL + "------------")
        print("1.", Style.BRIGHT + Fore.RED + "Y" + Fore.GREEN + "O" + Fore.CYAN + "L" + Fore.MAGENTA + "O")
        print("2. Safe")
        while mode != 1 and mode != 2:
            count = input("Which mode would you like to run?\n")
            try:
                mode = int(count)
            except ValueError:
                print(Fore.RED + "Please enter a number.")
                continue
        if mode == 1:
            print(Style.BRIGHT + Fore.RED + "Y" + Fore.GREEN + "O" + Fore.CYAN + "L" + Fore.MAGENTA + "O"
                  + Fore.WHITE + " mode initalized!")
            print()
            print(Style.BRIGHT + Fore.RED + "W" +
                  Fore.CYAN + "E" +
                  Fore.GREEN + "L" +
                  Fore.YELLOW + "C" +
                  Fore.BLUE + "O" +
                  Fore.MAGENTA + "M" +
                  Fore.RED + "E" +
                  " " +
                  Fore.CYAN + "B" +
                  Fore.GREEN + "R" +
                  Fore.YELLOW + "A" +
                  Fore.BLUE + "V" +
                  Fore.MAGENTA + "E" +
                  " " +
                  Fore.CYAN + "CH" +
                  Fore.GREEN + "A" +
                  Fore.YELLOW + "L" +
                  Fore.BLUE + "L" +
                  Fore.MAGENTA + "E" +
                  Fore.CYAN + "N" +
                  Fore.GREEN + "G" +
                  Fore.YELLOW + "E" +
                  Fore.BLUE + "R" +
                  " " +
                  Fore.MAGENTA + "!" +
                  Fore.GREEN + "!" +
                  Fore.YELLOW + "!" +
                  Fore.BLUE + "!")

        self.mode = mode

    def run(self) -> None:
        """
        Runs the whole thing
        :return:
        """
        more = True
        while more:
            count = input("How many entries?\n")
            try:
                count = int(count)
            except ValueError:
                print(Fore.RED + "Please enter a number.")
                continue
            threads = []
            for i in range(count):
                t = threading.Thread(target=self._enter())
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            again = input("Would you like to run more? (Yes/No)\n")
            if again.lower().startswith('y'):
                continue
            else:
                more = False
