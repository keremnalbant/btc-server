# BTC Server

## System Design and More
[See Whimsical](https://whimsical.com/btc-system-design-MqAKNkaZWDkYBkHSjAyPv1)

### How to setup development environment
    $ git clone
    $ cd btc-server
    $ pip install virtualenv
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ uvicorn main:app --reload
