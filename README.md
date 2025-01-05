# Wahoo Garmin Sync

A tool to sync Wahoo bike rides into Garmin Connect.

## Principle
This application will be triggered by the Wahoo API each time a new activity is registered on its platform.  
The webhook will then upload the `.fit` file to Garmin Connect.

## Register your application

1. You need to register an app at [Wahoo Developer Portal](https://developers.wahooligan.com)  
1. With scope:  
`email power_zones_read workouts_read plans_read routes_read offline_data user_read`
1. Choose _Sandbox_ (it will be approved more quickly) and enable Webhook.
1. With Webhook URI to:  
`https://your_website_url.com/webhook`  
*This application should be accessible behind this domain.*

## Build & Run the Docker image

Inside the `wahoo_garmin_sync` directory:  
  - Replace the placeholders _GARMIN_LOGIN_ and _GARMIN_PASSWORD_ in the `docker-compose.yml` file with your Garmin Connect login credentials.  
  - Then run the following command:  
    `docker compose up --build -d`  
  - Open a browser and and navigate to http://localhost:42195 or https://your_website_url.com   
    You should see a simple _ok_ message.

---

When the application is triggered by the Wahoo webhook, the logs (viewable with `docker logs wahoo`) should look like this:  
```
Received post
Workout url: https://cdn.wahooligan.com/wahoo-cloud/production/uploads/workout_file/file/jxre2UP3Lx_o6wF-8tdArw/2025-01-06-171681-ELEMNT_ROAM_F23E-852-0.fit
Filename: 2025-01-06-171681-ELEMNT_ROAM_F23E-852-0.fit
192.168.1.23 - - [06/Jan/2025 18:19:52] "POST /webhook HTTP/1.1" 200 -
File saved
Connected to _Garmin Connect_
{'detailedImportResult': {'uploadId': 302033637404, 'uploadUuid': {'uuid': 'eafa3083-3c1a-4529-bd59-f298f06418e4'}, 'owner': 166921955, 'fileSize': 85828, 'processingTime': 564, 'creationDate': '2025-01-06 18:19:56.336 GMT', 'ipAddress': None, 'fileName': '2025-01-06-171681-ELEMNT_ROAM_F23E-852-0.fit', 'report': None, 'successes': [], 'failures': []}}
Workout successfully uploaded
```
