# FastAPI JWT Authentication System

A secure and minimal authentication system using FastAPI and JSON Web Tokens (JWT). This project includes:

- User registration
- Login with password hashing
- Access and Refresh token generation
- Token-based protected routes
- Token refresh endpoint

## Features

- FastAPI-based REST API
- JWT Access and Refresh Tokens using `python-jose`
- Secure password hashing using `passlib`
- OAuth2-compatible login flow
- Token expiration handling
- Protected routes using dependency injection
- Refresh token support via HTTP headers
