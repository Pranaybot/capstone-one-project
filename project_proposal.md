Project Proposal

Newgen - A Flight Booking System

What goal will your project be designed to achieve?

• Provide Comprehensive flight Comparison: The website should offer a comparison of non-stop one way and round trip 
flights from different airlines
• User-Friendly Interface: Create a user-friendly interface that allows users to easily search for flights and look
at their flight payments and reviews
• Provide other info: Add links to other parts of the website, including travel, special assistance, FAQs, and trip
insurance

What kind of users will visit your app? In other words, what is the demographic of your users?
• The target demographic for our flight recommendation website is open to all people 13 years or older.

Will this be a website? A mobile app? Something else?
• Yes, It will be website and support phone/table view

What data do you plan on using?
• The application will use the API called SerpAPI. This API retrieves information about one way and round trip
flights and allows the user to filter based on additional criteria, such as number of stops and travel class.

What tech stack will you use for your final project?
• Frontend: HTML, JS, CSS, Bootstrap. 
• Backend: Python, Flask, SQLAlchemy, WTForms. 
• Database: PostgreSQL.


Project BreakDown

Setting Up Project Environment:
• Install Flask for the backend.
• Install SQLAlchemy for database management.
• Install WTForms for form handling.
• Install any other necessary libraries or tools.

Create Model and Schema for Users, Flights, Payments, and Reviews:
• Define a User model to store person information.
• Define payment models for one way and round trip flights to keep track of flight payments.
  The models should have a relationship with the User model.
• Define review models for one way and round trip flights to keep track of flight reviews.
  The models should have a relationship with the User model.

Login and Authentication Logic:
• Implement user registration and login functionality using Flask-Login or similar.
• Secure user authentication with hashed passwords using Flask-Bcrypt or similar.

Source Data: Get Familiar with Skyscanner API:
• Understand the SerpAPIAPI documentation for fetching flight details.
• Implement API request handling in Flask to fetch and display flight data on the frontend.

Set Up Frontend Environment:
• Use HTML, CSS, and Bootstrap for the frontend layout.
• Use Jinja templating to render dynamic content from the backend.
• Use JavaScript for any frontend interactivity, such as adding or removing flight reviews 
  or navigating the user to a different page when the person clicks a button

Testing and Debugging:
• Test the application thoroughly to ensure all features work as expected.
• Debug any issues that arise during testing.

Deployment:
• Deploy the application to a hosting service like Heroku or AWS.
• Ensure the application is secure and scalable for potential future updates.

Stretch Goal
• Implement a chatbot for the home page of the web application.

