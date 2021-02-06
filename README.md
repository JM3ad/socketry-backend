# socketry-backend
Playing about with flask sockets

## Dev
* `docker-compose up`

## Test
* `docker-compose -f docker-compose-test.yml up`

## Deployment
* Manually, build & run with:
  * `docker build --target prod -t prod .`
  * `docker run -e PORT=5000 -p 5000:5000 prod`
* Deploys automatically to heroku on push to main