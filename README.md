# API Cars

## Overview

This project is a Django REST Framework API designed to provide a robust and scalable backend service for managing user data and resources. It leverages the power of Django and DRF to offer a range of CRUD (Create, Read, Update, Delete) operations, along with advanced features such as role-based access control and token-based authentication.

Key features include:

- Role-based access control for secure endpoint connections.
- Integration with PostgreSQL for a reliable and performant database solution.
- Utilization of SimpleJWT for handling JSON Web Tokens for secure authentication.


## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python  3.9 or later.
- You have installed Django  3.2 or later.
- You have installed Django REST Framework  3.12 or later.
- You have installed PostgreSQL  13 or later.
- You have installed SimpleJWT.

## Installation

To install Your Project Name, follow these steps:

1. Clone the repository:
   ``sh git clone https://github.com/incelcure/incelcure.git``

2. Create a virtual environment and activate it:
  ``sh python3 -m venv env source env/bin/activate``
   
3. Install the required dependencies:
   ``sh pip install -r requirements.txt``

4. Set up the PostgreSQL database:
   ``sh # Ensure you have PostgreSQL installed and running # Then create a database for your project createdb cars``

5. Apply migrations:
  ``sh python manage.py migrate``

## Configuration

Configure your `.env` file with the necessary settings including database credentials and JWT secret key.

## Usage

To run Cars API, follow these steps:

1. Start the development server:
   ``sh python manage.py runserver``

2. Access the API at:
    [http://localhost:8000/](http://localhost:8000/)

3. To authenticate, obtain a token by sending a POST request to `/api/login/` with your username and password. Use this token in the `Authorization` header for subsequent requests.

4. To make superuser use
    ``sh python manage.py createsuperuser``

5. To register some user, use admin panel:
    [http://localhost:8000/admin/](http://localhost:8000/admin/) with ur superuser data

## Testing

To run tests, use the following command:
     ``sh python manage.py test``

## Authors

-[incelcure](https://github.com/inclecure)

## Acknowledgments

- Special thanks to Amis Techno for the opportunity to realize my potential in weak programming
