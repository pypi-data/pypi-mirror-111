Discord API Wrapper for Python

Installation:
**Linux:** `pip3 install -U daw`
**Windows:** `pip install -U daw`

Requirements:
- `Python 3.x`

**Examples**

```py
from daw.api import *

daw = DAW(token="token", bot_token="optional") #Initalize the wrapper

print(daw.get_current_user_data()) #Prints user data as json```

