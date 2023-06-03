# FastAPI 

This project is a modern web application built using FastAPI, a high-performance web framework for building APIs with Python 3.9+. It incorporates various functionalities such as integration with Amazon S3, model relations, background tasks, email sending, and JSON Web Token (JWT) authentication. 🚀

## Features 

- **FastAPI**: A powerful framework for building REST APIs
- **AWS S3 Integration**: Seamless integration with Amazon S3 for file storage 📁
- **JWT Authentication**: Secure authentication using JSON Web Tokens 🔒
- **Model Relations**: One-to-many and many-to-many relationships between models 🔄
- **Background Tasks**: Execute long-running processes in the background ⏳
- **Email Sending**: Send emails to users as background tasks 📧
- **File Handling**: Upload and retrieve files 📄
- **Custom Responses**: Customized responses for better user experience ✨

## Installation 

To get started with the project, follow these steps:

1. Clone the repository
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set up the necessary environment variables (see below)
4. Start the application: `uvicorn main:app --reload` or `docker-compose up --build`

## Environment Variables 

Ensure the following environment variables are set:

- **AWS_ACCESS_KEY_ID**: AWS access key ID for S3 integration
- **AWS_SECRET_ACCESS_KEY**: AWS secret access key for S3 integration
- **AWS_BUCKET_NAME**: AWS S3 bucket name
- **DATABASE_URL**: Database URL
- **EMAIL_USER_NAME**: Email account username for sending emails
- **EMAIL_USER_PASSWORD**: Email account password for sending emails
- **JWT_SECRET_KEY**: Secret key for JWT authentication
- **JWT_REFRESH_SECRET_KEY**: Secret key for JWT token refreshing

## Usage 

Once the application is running, you can access the API documentation at `http://localhost:8000/docs` to explore and interact with the endpoints.

Enjoy using the beautifully crafted FastAPI web application! ✨
