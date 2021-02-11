# Spellchecker API

## Getting Started

There are two ways to configure your environment for this python app:
1. Virtual Environment
1. Docker Container

Both methods should allow you to curl/postman against `localhost:31337/spellcheck/{word}`

## Virtual Environment
1. Install your favorite virtual environment to avoid affecting your main python environment
`pip install virtualenv`
1. create virtual environment
`virtualenv spellcheck`
1. activate virtual envionment:
`source spellcheck/bin/activate`
1. Install python dependencies
`pip install -r requirements.txt`
1. Run the application
`python spellcheck.py`

## Docker Container
1. Build the docker container
`docker build -t spellchecker .`
1. Run the docker image
`docker run -d -p 31337:31337 spellchecker`
