# Planetary API

List of known planets so far discovered

## Getting Started

1. Clone or Pull the repo
2. To use the **email** functionality you will need to create .env file and add the following environment variables

        MAIL_USERNAME=your_email_address
        MAIL_PASSWORD=your_email_password
        MAIL_PORT=your_email_provider_smtp_port
        MAIL_SERVER=your_email_smpt_address

3. To be able to use JWT for content management add the following enviroment variable to .env
        
        SECRET_KEY=your_secret_key

4. Run the following shell command

        ./build_docker.sh && ./run_docker.sh

5. Open you browser and visit localhost:5000 or execute the following shell command to verify the app is running

        curl localhost:5000

You should received the message *Hello World*

**NOTE:** if you are using Windows, consider executing point 4 using git bash

### You may follow this instructions if you like to set up your own Flask and Python environment
https://stackabuse.com/dockerizing-python-applications/

### Docker CLI (which is done by the .sh scripts provided)

1. Build the image with

        docker build -t [img_name]
Default image name *flask-web-app*

2. To run the image

        docker run --name [app_name] -v $PWD/src:/www/src -p 5000:5000 [img_name]
Add a **-d** to run in the background

Default app_name *flaskapp*

3. Start the image

        docker -i start [app_name]
The **-i** indicates for interactive mode if needed for debugging

4. Stop the image

        docker stop [app_name]

### Prerequisites

Just having Docker, because is more fun that way

## How does it work

### The following routes are available (to be updated)

```
  GET /planets
  PUT /add_planet
  DELETE /delete_planet/<planet_id>
```
### Example from GET /planets
``` json
  [
  {
    "distance": 100000000.0,
    "home_star": "Golden Orb of Day",
    "mass": 1.08e+25,
    "planet_id": 1,
    "planet_name": "Aiur",
    "planet_type": "Class M",
    "radius": 6636.0
  },
  {
    "distance": 67240000.0,
    "home_star": "Sol",
    "mass": 4.867e+24,
    "planet_id": 2,
    "planet_name": "Venus",
    "planet_type": "Class K",
    "radius": 3760.0
  }
]
```

## Running the tests

In progress

## Deployment

In progress

## Enhancement
1. Refactory
2. Create modules
3. Single responsitility implementation
4. Update routes
5. Middleware for content management

## Built With

* [Python3](https://docs.python.org/3/) - Programming Language
* [Docker](https://www.docker.com/products/docker-desktop) - Container
* [Flask](https://palletsprojects.com/p/flask/) - Web Framework
* [SQLAlchemy](https://www.sqlalchemy.org/) - SQL Toolkit and ORM
* [JWT](https://jwt.io/) - Used to generate, check, validate user identity and content management

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

This project is based on the course [Building RESTful APIs with Flask](https://www.linkedin.com/learning/building-restful-apis-with-flask/conclusion-3?autoplay=true&u=2169170) with customizations and modifications done by [Henry Valbuena](https://github.com/henryvalbuena). That's me :smile:

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
