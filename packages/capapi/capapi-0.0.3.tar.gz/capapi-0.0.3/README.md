# CapAPI
### Short for "Capitalism API for Python"

This is a simple, free-to-use, API wrapper for the [Capitalism Bots API](https://discord.capitalismbot.repl.co/beta/api/v1)

There isnt much, so read the source code lmao.

### Examples

```py
from capi import get_user

user = get_user(583745403598405632)

print(user.wallet)
```