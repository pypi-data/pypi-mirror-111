# Semya

A module to shorten the time to setup a new python package. This is just an opinionated
way to deal with setting up a project for pip installation, running tests, and
bootstrapping setup.

## Example setup

```
from semya import Semya

seed = Semya(package_name="gytrash", project_url="https://github.com/trejas/gytrash")

seed.sew()
```
