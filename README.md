# Car Rental 🚗
Car Rental is a database project designed to manage a car rental service. It enables storing information about vehicles, customers, reservations, and payments, supporting efficient data management. The system offers features such as adding new rentals, generating reports, and monitoring vehicle availability.

## Table of Contents
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Project Structure](#project-structure)
* [Setup](#setup)
* [Screenshots](#screenshots)

## Technologies Used
- Python: Main programming language used for backend development. 
- Flask: A lightweight web framework for building the application's backend. 
- Conda: Used for managing packages and virtual environments. 
- PostgreSQL: Relational database system used for storing and managing data.
- PL/pgSQL: Used for stored procedures, functions, and triggers in PostgreSQL.
- Psycopg2: A PostgreSQL adapter for Python to handle database interactions. 
- Jinja: Template engine for rendering HTML pages dynamically. 
- Tembo: Cloud-based PostgreSQL hosting platform. 
- SQL: For creating and managing the database schema and executing queries.
- JavaScript: Used for displaying dynamic fields when adding new records.
- HTML: For structuring the web pages.
- CSS: For styling and layout of the web pages.


## Features
- Brand and Model Management: Allows storing and managing information about car brands and models, including names and associations between them. 
- Car Inventory: Manages detailed information about each car, such as registration numbers, production years, and availability. 
- Customer Management: Stores customer information, including names, contact details, and unique phone numbers. 
- Employee Roles: Manages employee roles with specific permissions and salary information, ensuring proper access control. 
- Rental Management: Supports adding new rentals, linking customers with cars and employees, and validating rental dates. 
- Order Management: Allows customers to place orders for specific car models with start and end dates, and tracks the status of orders (successful, failed, or pending).
- Pricing System: Manages rental pricing based on car classes, ensuring accurate cost calculations for different vehicle categories. 
- Payment Processing: Records payments for rentals and links them to corresponding transactions, ensuring all payments are properly tracked. 
- Reporting and Analysis: Enables generating reports on car availability, popular models, and financial performance.
- Data Validation and Integrity: Ensures data accuracy through constraints such as unique keys, foreign keys, and checks on data formats and logical date orders. 

## Setup
The project requirements and dependencies are listed in the requirements.txt file, which is located in the root directory of the project.

## Project structure
Car-Rental-Databases-Project/
├── static/                  # Static files (images, CSS, JS)
├── templates/               # HTML templates for the frontend
├── .gitignore               # Git ignore file for sensitive and unnecessary files
├── BD_Dokumentacja.pdf      # Project documentation (in Polish)
├── README.md                # Main project documentation
├── app.py                   # Main backend logic (Flask)
├── baza.sql                 # SQL schema for the database
├── requirements.txt         # Python dependencies


1. Clone repository
 ```bash 
   git clone https://github.com/ziraaell/Car-Rental-Databases-Project.git
```

2. Navigate to the project directiory:
 ```bash 
  cd Car-Rental-Databases-Project
```

3. Create and activate a virtual environment using Anaconda (optional but recommended):
```bash 
  conda create -n rental_env
  conda activate rental_env
```

4. Install the required libraries:
```bash 
  pip install -r requirements.txt
```

5. Create the database using the 'baza.sql' file:
   - Ensure you have an active PostgreSQL instance. This can be hosted locally, on Tembo, or any other PostgreSQL hosting service.
   - Run the following command to create the database structure and insert initial data:


     ```bash 
     psql -h [hostname] -U [username] -W -d [database_name] < baza.sql
     ```

6. Configure the .env file with database settings:
   - Create a .env file in the root directory and add:


     ```bash 
     DATABASE_URL=postgresql://[username]:[password]@[hostname]:[port]/[database_name]
     ```
        
7. Run the application locally:
   ```bash 
      flask run
    ```
   
  The application will be awailable at: http://127.0.0.1:5000

## Screenshots
### Car List Display
List of cars available for rent, displaying information such as model, brand, license plate number, and class. 

<img width="1264" alt="image" src="https://github.com/user-attachments/assets/17c27a2a-5fb3-4415-afcc-8c76630c47a0" />

### Adding record
Form for adding a new car, including fields for license plate number, year, and model selection.

<img width="1264" alt="image" src="https://github.com/user-attachments/assets/d4cacb25-71b6-4702-b4af-60ebdf5b9e74" />

### Reports Display - Car Availability
Search for available cars by selecting a start and end date. 

<img width="1264" alt="image" src="https://github.com/user-attachments/assets/6fd06c54-de13-4e06-9e14-a1a506b888fe" />

## Available Cars Summary
Displays the total number of available cars and a breakdown by brand. 

<img width="1264" alt="image" src="https://github.com/user-attachments/assets/ccf0c95e-3e18-41f2-92c2-075573a0d067" />
