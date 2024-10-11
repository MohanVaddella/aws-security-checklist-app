# AWS Security Checklist App

## Overview

The AWS Security Checklist App is a web application designed to provide users with a checklist of best practices for securing AWS infrastructure. Users can view, update, and search through the checklist, ensuring compliance with AWS security standards.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Key Components](#key-components)
- [Tests](#tests)

## Technologies Used

- **Flask**: A Python-based web framework for building the backend API and handling HTTP requests.
- **Pandas**: For reading, manipulating, and updating the security checklist data stored in an Excel file (`security-controls.xlsx`).
- **HTML/CSS/JavaScript**: Frontend structure and styling, including interactive behavior with custom styles and client-side logic.
- **Bootstrap**: Used for responsive design and enhancing the UI.
- **Flask Testing**: For writing unit tests to ensure proper functionality of the application.

## Project Structure

```bash
aws-security-checklist-app/
├── __init__.py                 
├── app.py                    
├── models.py                   
├── routes.py                   
├── requirements.txt            
├── security-controls.xlsx       
├── templates/                  
│   ├── base.html               
│   ├── checklist.html          
│   ├── index.html              
│   └── update-checklist.html   
├── static/                     
│   ├── css/
│   │   └── styles.css          
│   ├── images/
│   │   └── logo.jpeg           
│   └── js/
│       └── main.js             
├── tests/                      
│   └── test_app.py             
└── README.md                   
```

## Setup Instructions

To set up the project locally, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/MohanVaddella/aws-security-checklist-app.git
   cd aws-security-checklist-app
   ```
2. **Install Dependencies**:

   - Ensure you have Python installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Run the Flask App**:

   ```bash
   export FLASK_APP=app.py
   flask run --port 5001
   ```

   This will start the Flask app on port 5001. You can access the application in your web browser by navigating to:
   http://localhost:5001

2. **Accessing the Homepage**:

   The homepage will display the AWS Security Checklist, and you can interact with it to view or update specific controls.

## Key Components

- **Backend**:

  - The **Flask app** defines the core routes (`routes.py`) to serve different pages and handle requests. `app.py` initializes the app and manages the overall flow.
  - **Pandas** is used to handle reading and writing to the `security-controls.xlsx` file, which stores the security checklist data.

- **Frontend**:

  - **HTML** templates in the `templates/` directory render the checklist and homepage.
  - **CSS** files in `static/css/` handle styling, and **JavaScript** in `static/js/` manages client-side behavior such as form submissions and dynamic updates.

## Tests

The application includes unit tests to verify the functionality of the core features. These tests are located in the `tests/` directory.

- To run tests:

  ```bash
  python -m unittest discover tests
  ```

