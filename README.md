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
