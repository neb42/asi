# asi

The service is being hosted on my raspberry pi so I apologise if it seems a bit slow. If it goes down for any reason drop me an email.

The code was written using flask and flask-restful, and the requests library for communicating with github. 

## Usage
http://bmcalindin-asi.ddns.net/user/\<username\>/repo/

### Optional GET Parameters
* limit - integer - the maximum number of repos to show
* orderby - the field to sort the results by

## Deployment
Fabric was used for the deployment

1. Github repo is checked out to /rootdir/releases/commit_timestamp
2. Bootstrap script is ran to setup virtualenv and install packages
3. The checkout is symlinked to /rootdir/releases/current
4. Apache is restarted

### Improvements

* The checkouts and bootstrap should be done in parallel on all servers. Once that is done all servers should be switched and restarted in parallel in ensure that they are kept in sync as much as possible.
* Normally part of my deployment code would remove old versions, keeping something like the 5 most recent deployments. I just forgot to do this.

## Tests

I've added some unit tests for the repo controller. Obviously this could have a lot more tests, this was just an example. As well as more unit tests I
would probably add some end-to-end integration tests that communicate with github. The tests are ran with:

./scripts/test

## General Improvements

* I messed up the apache config a bit. Normally I would keep the default config and add one line to include /rootdir/releases/current/conf/app_server.conf. This would contain a virtual host with everything relevant to this deployment.
* My server isn't setup properly at all. I took this as more of a coding/deployment challenge rather than an infrastructure challenge.
* More tests
* I'm less experienced with flask than django so perhaps some of the create app boiler plate isn't perfect
* Logging isn't setup properly
