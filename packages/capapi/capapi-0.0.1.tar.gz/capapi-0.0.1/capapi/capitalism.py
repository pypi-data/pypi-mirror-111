import requests


class get_user:
    
    def __init__(self, user_id: int):
        self.user_id  = user_id

    @property
    def wallet(self):
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=wallet')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']

    @property
    def bank(self):
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bank')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']

    @property
    def bank_max(self):
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bank_max')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']

    @property
    def inventory(self):
        """Returns JSON of the users inventory. To get a value use `get_user(x).inventory['beef']`.
        I will add full inventory support after release."""
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={uself.user_id}&data=inventory')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']

    @property
    def inv(self):
        """Returns JSON of the users inventory. To get a value use `get_user(x).inventory['beef']`.
        I will add full inventory support after release."""
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={uself.user_id}&data=inventory')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']

    @property
    def bitcoin(self):
        """Returns the useres bitcoin"""
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bitcoin')
        if resp.status_code == 200:        
            _json = resp.json()
            return _json['message']

    @property
    def exp(self):
        """Returns the users Experience"""
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=exp')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']

    @property
    def xp(self):
        """Returns the users Experience"""
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=exp')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']

    @property
    def multiplier(self):
        """Returns the users Experience"""
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=multi')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']

    @property
    def multi(self):
        """Returns the users Experience"""
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=multi')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']

    
    @property
    def bank_colour(self):
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bank_color')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']

    @property
    def bank_color(self):
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=bank_color')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']

    @property
    def ads(self):
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=ads')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']

    @property
    def job(self):
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=job')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']

    @property
    def badges(self):
        """Returns JSON of the users badges. To get a value use `get_user(x).badges['RICH']`.
        I will add full inventory support after release."""
        resp = requests.get(f'https://discord.capitalismbot.repl.co/beta/api/v1?user={self.user_id}&data=inventory')
        if resp.status_code == 200:
            _json = resp.json()
            return _json['message']
