# BTC Server [![Build and deploy Docker app to Lightsail](https://github.com/keremnalbant/btc-server/actions/workflows/prod.yml/badge.svg)](https://github.com/keremnalbant/btc-server/actions/workflows/prod.yml)

[See Live](https://app.globalfuturepoland.com)

## Demo Video
https://github.com/keremnalbant/btc-server/assets/43813768/f5e875a9-3e10-439a-be41-c2fb4c3d8488

## System Design and More
[See Whimsical](https://whimsical.com/btc-system-design-MqAKNkaZWDkYBkHSjAyPv1)

## Functionalities
- Real-time notifications and data polling with Websockets (Socket.io)
- Users can continue to make guesses even they close and reopen their browsers, even more server is restarted, unless they clean their ~~cookies~~ cookies are deprecated since S3 with CloudFront distribution does not support cookies, now we use LocalStorage with bearer tokens.
- Loginless persisted data with ~~cookies~~ LocalStorage
- Custom managers/handlers with Singleton Design Pattern
- Strong type-safety achieved via Pydantic
- Modular Design Pattern
- Session/SocketID management to publishing custom messages per user
- High-level usage of asyncio features, fully async code
- Schedule mechanisms
- Coincap API
- MongoDB
- Dockerized
- AWS Services used for deployment, CI/CD with GitHub Actions
- Lightsail Container Service used for distribution and deployment, Domain/DNS management achieved via GoDaddy

### How to setup development environment
    $ git clone
    $ cd btc-server
    $ pip install virtualenv
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ uvicorn main:app --reload
