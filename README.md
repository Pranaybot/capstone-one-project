# Newgen - A Flight Booking System

***

## Summary - Project Description

***

Newgen is a flight booking application. It allows users to book nonstop
one-way and round trip flights. While the application does not retrieve
payment details from the user's payment method, it serves as a first step 
to achieving this goal and much more. The user can look at payments they
have made and the reviews for them. In addition, users can modify or delete
any review they have created. Finally, the application incorporates a chatbot
built from the Botpress website to answer questions users may have.

## Tech Stack

***

### Frontend

HTML, JS, CSS, Bootstrap

### Backend

Python, Flask, SQLAlchemy, WTForms, PostgreSQL

## Features

***

### Secure User Sign-in / Form Validation

User sign-in routes are protected using bcrypt hashed passwords and forms for
one-way trip payments, one-way trip reviews, round trip payments, and round trip reviews are
validated securely through WTForms

### Responsive Layout

The content of the application shrinks or enlarges to fit the size of the screen regardless of 
whether the application is viewed on a smartphone, tablet, or a computer.

### Cache control

After every request to a route, the flight booking system clears cache information 
to control storage of user data.

### Interactive footer and travel nav tab links

Users can click on these links to see other information pertaining to the website,
whether it deals with trip insurance, FAQs, or airport rules. While the information
presented for the application is not real, it acts as a first step to making the 
application usable and unique.

### Backend

1. The Flask application connects to PostgreSQL using a PostgreSQL shell.
Users can connect to the airline-app database from this shell and run the
app.py file with `flask run` command to create the tables inside the PostgreSQL shell.
2. To run PostgreSQL shell, make sure the PostgreSQL server runs on port 5432
and use `psql airline-app` command to connect to the `airline-app` database.
3. Backend runs on localhost:5000.

### Frontend

1. As mentioned above, you use `flask run` command to start the flight booking system
application.
   
## Future Development

***

1. Allow users to change password / have a forgotten password system in place.
2. Allow users to delete their own accounts.
3. Implement automatic light/dark theme toggle for application based on the time
of day and season.
4. Write or include scripts that process details from the payment method the user
chooses to book the flight(s).
5. Allow users to book flights regardless of the number of stops or other parameters
that may or may not delay flights.
6. Notify users if there are any price drops for flights and allow them to save
destinations they are interested in.