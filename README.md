# Requirements
JSON API that allows the following:
- Create a random short link for arbitrary URLs, e.g., bit.ly/2FhfhXh
- The same URL should always generate the same random shortlink
- Allow creating custom short links to arbitrary URLs, e.g., bit.ly/my-custom-link
- Provide a route for returning stats in a given short link, including:
- When the short link was created
- How many times the short link has been visited total
- A histogram of number of visits to the short link per day
- Of course, the server itself should handle redirecting short links to the URLs it creates

# Data Storage
Store mapping of short_url:long_url in NoSQL K/V store. In my mind DynamoDB makes sense as it uses consistent hashing and we can use the short_url as the partion key, and unlike redis we can store it to disk which should be cheaper. We can front it with a cache for high read traffic.

Store stats in redis since they're relatively small and redis has nice incr commands which can help with concurrent requests simultaneously needing to update that value. Can have an expiry of 90 days, which we could lower if it's taking too much space and product allows it. Otherwise we'd probably need to use a different store.

# Tech
I used FastAPI so that it could easily autogenerate api docs, and it seemed capable of producing a simple json api. 

I used redis to store stats, and dynamodblocal to simulate a dynamodb server in aws. The project runs in docker containers.

# Running this for yourself
You should just be able to run 
`docker-compose up`

You can put `http://localhost/docs` in your browser to see the OpenAPI-generated interface (or if you prefer redoc, `http://localhost/redoc`)

Caveat: I wasn't able to get dymamodb to persist, so it will get wiped out when restarting docker compose. I think there is some sort of permissions issue where the `data/` dir gets created as root and it needs to be owned by the `dynamodblocal` user.

# Next Steps
- Fix dynamodblocal persistence
- Better testability; right now it's easiest accessed/tested through the docs page
- API request/response could be more readable; right now it's just kind of dumping all possible data in the response. Would like it to hide more data
- Separate stats endpoint
- Redirects on the GET /short_url/id
- Retention window on histogram data
