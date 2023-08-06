Use secrets from [keepass](https://keepass.info/) in your [BundleWrap](http://bundlewrap.org/) repo.

# Installation

```
pip install bundlewrap-keepass
```

# Setup

Create `.bw_keepass.cfg` in your home. It should contain two lines: First
line should contain a path to your keepass file, second line may contain
your password.

If you're not comfortable putting your password into a plain-text file,
you may also use `BW_KEEPASS_PASSWORD` in your environment variables.

You may also set `BW_KEEPASS_FILE` in your environment to overwrite the
location of your keepass file. Please note that if you set the file path
in your environment, you *must* also set the password.

# Usage

All function calls accept lists or strings as their arguments. If you
need to traverse into subdirectories in your keepass file, you have to
use `|` as separator when not using lists.

For example, if you want to access the Password for 'mysite', which is
located inside the directory 'bundlewrap', you can use either one of
these:

```
bwkeepass.password('bundlewrap|mysite')
bwkeepass.password(['bundlewrap', 'mysite'])
```

Example `nodes.py`:

```python
import bwkeepass as keepass

nodes = {
    'somenode': {
        'metadata': {
            'my_secret': keepass.password('my_identifier'),
        },
    },
}
```

Available Fields/Methods are:
- `bwkeepass.password()` for passwords
- `bwkeepass.username()` for usernames
- `bwkeepass.url()` for urls
- `bwkeepass.notes()` for notes

Note: This will insert a proxy object into your metadata, the actual secret is not retrieved until you convert it to a string (e.g. by inserting it in a template or calling str() explicitly).

---

© 2021 [Franziska Kunsmann](mailto:pypi@kunsmann.eu)
