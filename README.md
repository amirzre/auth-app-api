<h1 align="center"> Authentication App </h1> <br>

<h3 align="center">
  An authentication and user registration system. Built with Python/Django Rest Framework.
</h3>

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Workflow Explanation](#workflow-explanation)
- [API Endpoints](#api-endpoints)
  - [Login](#login)
  - [Refresh Token](#refresh-token)
  - [Verify Token](#verify-token)
  - [Send OTP Code](#send-otp-code)
  - [Register](#register)
  - [Profile](#profile)
- [Project Setup](#project-setup)

## Introduction

This project is an authentication and user registration system designed for a web or mobile application. The system allows users to log in if they are already registered or to sign up if they are new users. It integrates phone number-based authentication, ensuring that users receive a verification code to validate their identity before creating an account. The flow ensures a seamless experience by guiding users through the necessary steps based on their registration status.


## Features

A few of futher on this app:

- Separating the business logic layer
- Separation of test and production environments
- Customized user authentication
- Authorization for endpoints
- Throttling for user requests
- Use Redis cache
- Unit test for all app
- Github workflow
- Document project with swagger
- Dockerized project

## Workflow Explanation

This workflow ensures that both new and returning users can access the application securely and efficiently, with minimal friction in the authentication process.


```mermaid
flowchart TD
    A[1. enter phone number] --> B{2. registered user?}
    B -- Yes --> C[3. enter password and login]
    B -- No --> D[4. get verification code]
    D --> E[5. enter personal details and password]
    E --> F[6. register user and login]
```

1. **Enter Phone Number:**
   - The user begins the process by entering their phone number. This step is crucial as it determines whether the user is already registered or needs to go through the registration process.

2. **Registered User?**
   - The system checks whether the entered phone number is associated with an existing account.
   - If the user is registered, they are prompted to enter their password to log in.
   - If the user is not registered, the system proceeds to the next step to begin the registration process.

3. **Enter Password and Login:**
   - For registered users, they are prompted to enter their password. If the password is correct, they are successfully logged into the system.

4. **Get Verification Code:**
   - For new users, the system sends a verification code to the provided phone number. This step ensures that the phone number is valid and belongs to the user.

5. **Enter First Name, Last Name, Email, and Password:**
   - Once the user has verified their phone number using the code, they proceed to enter their personal details: first name, last name, email address, and a password of their choice. This information is essential for creating a new user account.

6. **Register User and Login:**
   - After entering all the required information, the system registers the user by creating a new account with the provided details. The user is then logged in, allowing them to start using the application.



## API Endpoints 
API endpoints facilitate the communication between clients and servers. We will design the APIs REST-style. A URL shortener primary needs two API endpoints. 

### Login

**Endpoint:** `/api/auth/jwt/login/`

**Method:** `POST`

**Description:**
This endpoint allows users to log in by providing their phone number and password. Upon successful authentication, it returns access and refresh tokens.

**Request Body:**
```json
{
    "phone": "string",
    "password": "string"
}
```

**Response:**
```json
{
  "access": "string",
  "refresh": "string"
}
```

**Example Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/jwt/login/ \
-H "Content-Type: application/json" \
-d '{"phone": "09123456789", "password": "test@123"}'
```

**Example Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
    "refresh": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..."
}
```

### Refresh Token

**Endpoint:** `/api/auth/jwt/refresh/`

**Method:** `POST`

**Description:**
This endpoint is used to refresh the access token. By providing a valid refresh token, users can obtain a new access token.

**Request Body:**
```json
{
    "refresh": "string"
}
```

**Response:**
```json
{
  "access": "string",
  "refresh": "string"
}
```

**Example Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/jwt/refresh/ \
-H "Content-Type: application/json" \
-d '{"refresh": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..."}'
```

**Example Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
    "refresh": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..."
}
```

### Verify Token

**Endpoint:** `/api/auth/jwt/verify/`

**Method:** `POST`

**Description:**
This endpoint is used to verify the validity of a JWT token. If the token is valid, the response will be empty. If the token is invalid or expired, an error message will be returned.

**Request Body:**
```json
{
    "refresh": "string"
}
```

**Response:**
```json
{}
```

**Example Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/jwt/verify/ \
-H "Content-Type: application/json" \
-d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..."}'
```

**Example Response:**
```json
{}
```

### Send OTP Code

**Endpoint:** `/api/users/send-otp/`

**Method:** `POST`

**Description:**
This endpoint is used to send a One-Time Password (OTP) via SMS to the user's phone number. The OTP can be used for verifying the user's phone number during registration processes.

**Request Body:**
```json
{
    "phone": "string"
}
```

**Response:**
```json
{
    "otp_code": "string"
}
```

**Example Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/users/send-otp/ \
-H "Content-Type: application/json" \
-d '{"phone": "09123456789"}'
```

**Example Response:**
```json
{
    "otp_code": "123456"
}
```

### Register

**Endpoint:** `/api/users/register/`

**Method:** `POST`

**Description:**
This endpoint is used to register a new user in the system. The user must provide their phone number, password, OTP code received via SMS, and personal details such as first name, last name, and email. Upon successful registration, the user's information is returned.

**Request Body:**
```json
{
    "phone": "string",
    "password": "string",
    "otp_code": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "user@example.com"
}
```

**Response:**
```json
{
    "phone": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "user@example.com"
}
```

**Example Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
-H "Content-Type: application/json" \
-d '{
    "phone": "09123456789",
    "password": "test@123",
    "otp_code": "123456",
    "first_name": "user",
    "last_name": "test",
    "email": "user.test@example.com"
}'
```

**Example Response:**
```json
{
    "phone": "09123456789",
    "first_name": "user",
    "last_name": "test",
    "email": "user.test@example.com"
}
```

### Profile

**Endpoint:** `/api/users/profile/`

**Method:** `GET`

**Description:**
This endpoint is used to retrieve the authenticated user's profile information. The response includes the user's first name, last name, and email address. Note that the user must be authenticated (e.g., by providing a valid JWT token) to receive a response from this endpoint.


**Response:**
```json
{
    "first_name": "string",
    "last_name": "string",
    "email": "user@example.com"
}
```

**Example Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/users/profile/ \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Example Response:**
```json
{
    "first_name": "user",
    "last_name": "test",
    "email": "user.test@example.com"
}
```

## Project Setup

1. go inside the project
```
cd /path/project/
```

2. setup venv
```
python3 -m venv venv
source venv/bin/activate
```

3. install Dependencies
```
pip install -r requirements.txt
```

4. create your env
```
cp .env.example .env
```

5. spin off docker compose
```
docker compose -f docker-compose.dev.yml up -d
```

6. create tables
```
python manage.py migrate
```

7. run the project
```
python manage.py runserver
```

8. run tests
```
pytest
```
