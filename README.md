# BTC Server [![Build and deploy Docker app to Lightsail](https://github.com/keremnalbant/btc-server/actions/workflows/prod.yml/badge.svg)](https://github.com/keremnalbant/btc-server/actions/workflows/prod.yml)

[See Live](https://app.globalfuturepoland.com)

## Demo Video
https://github.com/keremnalbant/btc-server/assets/43813768/f5e875a9-3e10-439a-be41-c2fb4c3d8488

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
