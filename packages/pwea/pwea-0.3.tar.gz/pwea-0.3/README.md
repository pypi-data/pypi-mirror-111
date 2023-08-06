# Pwea 

Pwea is a simple weather tool written in Python, utilizing the [Weather API](https://www.weatherapi.com/) to source current weather information.

Pwea uses the [requests](https://docs.python-requests.org/en/master/) and [rich](https://github.com/willmcgugan/rich) libraries to retrieve and display weather data.

# How it works

Pass a desired location to `pwea` to retrieve the current weather information. For forecast information, add `-t forecast` or `--type forecast`. For imperial measurements, use `-u imperial` or `--unit imperial`

Use it like this:

`pwea springfield MA`

![springfield](current.gif)

![springfield](forecast.gif)

# Installation

You can install pwea from PyPi, or build it from source.

## Pypi

`pip install pwea`

## Building from source

Clone the repository:

`git clone https://gitlab.com/jeffreybarfield/pwea.git`

Install using `setuptools`:

`python3 setup.py install`

# Credit

I created this tool to educate myself on the Rich library. I was originally inspired by the [pwy](https://github.com/clieg/pwy) project.

# License

Copyright © 2021 Jeff Barfield.

