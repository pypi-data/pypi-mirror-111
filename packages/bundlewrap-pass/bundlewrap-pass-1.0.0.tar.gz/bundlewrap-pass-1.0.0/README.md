Use secrets from [pass](https://www.passwordstore.org/) in your [BundleWrap](http://bundlewrap.org/) repo.

# Installation

```
pip install bundlewrap-pass
```

# Setup

There's no setup needed. Please note bundlewrap-pass will override your
`PASSWORD_STORE_DIR` to the content of `BW_PASS_DIR`, which in turn will
default to `~/.password-store`. Keep this in mind if you want to use
a custom path to your passwordstore repo.

# usage

bundlewrap-pass will use the first line of `pass` output to get its
`password` attribute. You can also retrieve any other saved attributes,
as long as your pass entries conform to the format which browserpass uses:

```
my_super_secure_password
custom_attribute: foo
another_attr: bar
```

You can then retrieve those attributes using the `attr` method of
bundlewrap-pass.

Example `nodes.py`:

```python
import bwpass

nodes = {
    'somenode': {
        'metadata': {
            'my_secret': bwpass.password('my_identifier'),
            'my_custom_attr': bwpass.attr('my_identifier', 'custom_attribute'),
        },
    },
}
```

Note: This will insert a proxy object into your metadata, the actual secret is not retrieved until you convert it to a string (e.g. by inserting it in a template or calling str() explicitly).

---

© 2021 [Franziska Kunsmann](mailto:pypi@kunsmann.eu)
