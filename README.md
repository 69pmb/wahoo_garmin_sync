# Wahoo Garmin Sync

A tool to sync Wahoo bike rides into _Garmin Connect_.

## Principle
This application will be triggered by the [Wahoo API](https://cloud-api.wahooligan.com/#webhooks) each time a new activity is registered on its platform.  
The webhook will then upload the `.fit` file to _Garmin Connect_.

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
  - Replace the placeholders _GARMIN_LOGIN_ and _GARMIN_PASSWORD_ in the `docker-compose.yml` file with your _Garmin Connect_ login credentials.  
  - Then run the following command:  
    `docker compose up --build -d`  
  - Open a browser and and navigate to http://localhost:42195 or https://your_website_url.com   
    You should see a simple _ok_ message.

## Test & Debug

### Logs

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

### Bruno

The Bruno collection contains:
- **Garmin** request to upload manually a file to _Garmin Connect_  
  - Fill the _token_ value with the _access_token_ value.  
    Can be found by running:  
    ```
    docker exec -it wahoo sh
    cat ~/.garth/oauth2_token.json
    ```
  - Choose the `.fit` file to upload
- **Webhook** request to call the deployed `/webhook` endpoint  
  - Filename can be found by listing workouts with the [Wahoo API](https://cloud-api.wahooligan.com/#get-all-workouts)
  - To receive a token:
    ```
    curl https://api.wahooligan.com/oauth/authorize?client_id=<client_id>&redirect_uri=https://your_website_url.com&scope=email%20power_zones_read%20workouts_read%20plans_read%20routes_read%20offline_data%20user_read&response_type=code -H "Content-Type: application/json"
    ```
    You will be redirected to your application with this url, holding a code:  
    ```
    https://your_website_url.com/?code=<code>
    ```
    Use it to the run:  
    ```
    curl -X POST https://api.wahooligan.com/oauth/token?client_secret=your_client_secret&code=<code>&redirect_uri=https://your_website_url.com&grant_type=authorization_code&client_id=<client_id> -H "Content-Type: application/json"
    ```
    Response:
    ```json
    {"access_token":"<access_token>","token_type":"Bearer","expires_in":7199,"refresh_token":"<refresh_token>","scope":"email power_zones_read workouts_read plans_read routes_read offline_data user_read","created_at":1736182705,"user_id":4112422}
    ```
    Use the _access_token_ value (it expires after 2 hours)
