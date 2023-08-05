# yaml-util
It will help to read yaml file

## Installation
```pip install yaml-utils```

## How to use it?
```python
from yaml_utils import get_parent_key_and_value

dict1 = [{'id': {'home_welcome_lbl': 'username'}},
         {'id': {'test.test1': 'test1', 'test.test2': 'test2', 'test.test3': 'test3', 'test.test4': 'test4'},
          'xpath': {'test.test5': 'test5', 'test.test6': 'test6', 'test.test7': 'test7', 'test.test8': 'test8'}},
         {'id': {'login_username_txt': 'username2', 'login_password_txt': 'password'}}]

loc, val = get_parent_key_and_value(dict1, "home_welcome_lbl")
print(loc,val)

# Output:
# id username
```

## License
MIT License

Copyright (c) 2021 Muralidharan Rajendran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.