
# FastAPI

This project is a web application built using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.9+ based on standard Python type hints. The web application includes several functionalities such as integration with Amazon S3, models relations, background tasks, email sending, and authentication with JSON Web Tokens (JWT).

The models relations include a one-to-many relationship between users and orders, and a many-to-many relationship between users, products and orders. The background tasks include sending emails to users.

The authentication functionality is based on JSON Web Tokens (JWT). Users can create an account, login and generate access_tokens. Authentication is required for certain endpoints such as creating, updating, or deleting orders. The JWT authentication is implemented using the PyJWT library.

## Features

- FastAPI for building the REST API
- Integration with AWS S3 for file storage
- JWT Authentication
- Models with relations between them
- Background tasks for long-running processes
- Email sending functionality
- Handling file and retrieving data
- Custom responses
- More coming soon

## Installation

1. Clone the repository
2. Install the required dependencies by running `pip install -r requirements.txt`
3. Set up environment variables (see below)
4. Start the application by running `uvicorn main:app --reload` or  `docker-compose up --build`

## Environment Variables

The following environment variables are required for the application to function:

- `AWS_ACCESS_KEY_ID`: AWS access key ID for S3 integration
- `AWS_SECRET_ACCESS_KEY`: AWS secret access key for S3 integration
- `AWS_BUCKET_NAME`: AWS S3 bucket name
- `DATABASE_URL`: Database URL
- `EMAIL_USER_NAME`: Email account username for sending emails
- `EMAIL_USER_PASSWORD`: Email account password for sending emails
- `JWT_SECRET_KEY`: Email account username for sending emails
- `JWT_REFRESH_SECRET_KEY`: Email account password for sending emails

## Usage

Once the application is running, the API can be accessed at `http://localhost:8000/docs`.

