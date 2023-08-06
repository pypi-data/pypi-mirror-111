![PREFS logo](https://github.com/Patitotective/PREFS/blob/main/Images/logo1.png?raw=true)

![Python Version](https://img.shields.io/pypi/pyversions/prefs)
[![PYPI](https://img.shields.io/pypi/v/prefs)](https://pypi.org/project/prefs/)
[![Downloads](https://pepy.tech/badge/prefs)](https://pepy.tech/project/prefs)
![Stars](https://img.shields.io/github/stars/patitotective/prefs)

## Why?

**PREFS's purpose is to facilitate the process of store and manage user preferences, simple but useful library.**

## Installation:

On windows:
`pip install PREFS`

On MacOS and Linux:
`pip3 install PREFS`

### Syntax:

PREFS library has inside a class also called PREFS, you have to create an instance of this class to call all functions. Each new instance is a new prefs file:
This class has one required parameter, which is a dictionary with the default preferences, default means the preferences that all users will have at first time.

```Python
UserPrefs = PREFS.PREFS(prefs = {"theme": "light", "lang": "en"})
```

The main methods are:

-   `ReadPrefs()`: Returns a dictionary with your prefs.

-   `WritePrefs()`: Requires two arguments, first the name of the pref that you want to change (if pref exists) or create if it doesn't, and second argument is the value that you want to asign to the pref.

-   `ConvertToJson()`: Converts the prefs file to a json one (with the same filename)

Methods outside PREFS class:

-   `ReadJsonFile()`: Requires the filename to read the json file.
-   `GetStats()`: Returns and prints the PREFS library stats using pypistats (https://pypi.org/project/pypistats/).

## Documentation

PREFS documentation can be found at https://github.com/Patitotective/PREFS/wiki with more examples and information.

## Links

-   Github page: https://github.com/Patitotective/PREFS
-   Pypi page: https://pypi.org/project/PREFS/

-   Contact me:
    -   Discord: **patitotective#0127**
    -   Email: **cristobalriaga@gmail.com**
