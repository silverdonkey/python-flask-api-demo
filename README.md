# Playground for REST API Demo with Python and Flask
## Features

- Implements a simple Flask Microservice
- Endpoints: 
    - Home: /
    - Products: /products
    - Auth Products: /auth/products (Authentication Token required)
    - Authentication: /auth (generate auth token for secured endpoints) 

## Build and Run
1. From the project directory call the prep.sh script to set up the virtual env and install dependencies: 

    ./prep.sh



2. To start the `public` microservice (without authentication), spin up the Flask development server, which will start running at `http://localhost:5000` and then make a HTTP GET request  `http://localhost:5000/products` from your browser or use the provided Postman collection.


        # activate the virtual env
        source .venv/bin/activate
        # start the service
        flask --app services/products run


3. To start the `secured` microservice (with authentication required), spin up the Flask development server, which will start running at `http://localhost:5000`and then make a HTTP GET request `http://localhost:5000/auth/products` from your browser or use the provided Postman collection. An Authorization header must be set accordingly, since it is a secured endpoint.

        flask --app services/auth/products run
        # OR
        python services/auth/products.py


In order to generate an authorization token, make a POST request to the `http://localhost:5000/auth` with credentials admin/admin or user/user. There is also a Postman request prepared. 

A note about the AuthN/AuthZ implemented here: JSON Web Tokens (JWTs) are used. 

## Containerize the Microservice
Build the conteiner with Docker: 

        docker build -t flask-microservice:1.0.0 .

Run the container (in the background), exposing ports 5000, 5001: 

        docker run -d --name flask-microservice -p 5000:5000 -p 5001:5001 flask-microservice:1.0.0

This command will start a Docker container running the microservice and expose port 5000 on the container to port 5000 on the host machine, allowing you to make HTTP requests from your web browser or Postman using the URL http://localhost:5000.

To start the public microservice from whithin the running container  on port 5001 execute the command: 

        docker exec -e PORT=5001 -it flask-microservice sh -c "python services/products.py"


## Post-actions
Do not forget to deactivate the virtual env when you've finished. Just run 'deactivate' from the command line: 

        deactivate