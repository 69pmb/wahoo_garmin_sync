# wahoo_garmin_sync
A tool to sync wahoo bike ride into Garmin Connect

You need to register an app at https://developers.wahooligan.com

Then add the webhook uri http://example.com:5000/webhook (you should setup a reverse https proxy)

The webhook will be called each time a new activity is registered on Wahoo. The .fit file will then be uploaded to Garmin Connect.

Docker compose:
```
    wahoo:
        build: ./wahoo
        restart: always
        environment:
          DESTDIR: /downloads
          GARMIN_LOGIN: somebody@example.com
          GARMIN_PASSWORD: secret
        volumes:
          - /path/to/wahoo/downloads/:/downloads
          - /path/to/wahoo/:/app/
        ports:
            - 5000
```
