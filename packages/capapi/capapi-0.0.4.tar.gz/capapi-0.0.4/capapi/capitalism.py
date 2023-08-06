import requests


class Ratelimit(Exception):
    pass

def get_user(user_id):
    return User(user_id)

class User:
    
    def __init__(self, user_id: int):
        self.user_id  = user_id

    @property
    def wallet(self):
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=wallet")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def bank(self):
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bank")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def bank_max(self):
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bank_max")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def inventory(self):
        """Returns JSON of the users inventory. To get a value use `get_user(x).inventory["beef"]`.
        I will add full inventory support after release."""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=inventory")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def inv(self):
        """Returns JSON of the users inventory. To get a value use `get_user(x).inventory["beef"]`.
        I will add full inventory support after release."""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=inventory")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def bitcoin(self):
        """Returns the useres bitcoin"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bitcoin")
        if resp.status_code == 200:        
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def exp(self):
        """Returns the users Experience"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=exp")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def xp(self):
        """Returns the users Experience"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=exp")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def multiplier(self):
        """Returns the users Experience"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=multi")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def multi(self):
        """Returns the users Experience"""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=multi")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")
    
    @property
    def bank_colour(self):
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bank_color")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def bank_color(self):
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bank_color")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def ads(self):
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=ads")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def job(self):
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=job")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")

    @property
    def badges(self):
        """Returns JSON of the users badges. To get a value use `get_user(x).badges["RICH"]`.
        I will add full badge support later."""
        resp = requests.get(f"https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=badges")
        if resp.status_code == 200:
            _json = resp.json()
            return _json["message"]
        if resp.status_code == 529:
            raise Ratelimit("You fucking retard, you have to pay $1 for more API calls during this minute")


    # Has Stuff
    def has_item(self, item:str):
        inventory = self.inventory
        try:
            result = inventory[str(item)]
            if result > 0:
                return True
            else:
                return False
        except:
            return False

    def has_badge(self, item:str):
        badges = self.badges
        try:
            result = badges[str(item)]
            if result > 0:
                return True
            else:
                return False
        except:
            return False

    def is_admin(self):
        return self.has_badge("admin")

print(get_user(763854419484999722).is_admin())