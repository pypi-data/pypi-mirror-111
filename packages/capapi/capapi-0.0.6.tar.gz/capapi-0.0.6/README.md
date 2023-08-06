# CapAPI
### Short for "Capitalism API for Python"

This is a simple, free-to-use, API wrapper for the [Capitalism Bots API](https://discord.capitalismbot.repl.co/beta/api/v1)

Source Code: https://github.com/drapespy/CapAPI

### Examples

```py
from capapi import get_user

user = get_user(583745403598405632)

print(user.wallet)
```