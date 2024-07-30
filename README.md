# Newgen - A Flight Booking System


## Summary - Project Description


Newgen is a flight booking application. It allows users to book nonstop
one-way and round trip flights. While the application does not retrieve
payment details from the user's payment method, it serves as a first step 
to achieving this goal and much more. The user can look at payments they
have made and the reviews for them. In addition, users can modify or delete
any review they have created. Finally, the application incorporates a chatbot
built from the Botpress website to answer questions users may have.

You can view the deployed application here: https://capstone-one-4nvd.onrender.com

## Tech Stack


### Frontend

HTML, JS, CSS, Bootstrap

### Backend

Python, Flask, SQLAlchemy, WTForms, PostgreSQL

## Features

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

### The interactive footer and travel nav tab links

Users can click on these links to see other information pertaining to the website,
whether it deals with trip insurance, FAQs, or airport rules. While the information
presented for the application is not real, it acts as a first step to making the 
application usable and unique.

### Interactive Botpress chatbot

People using the site can interact with the chatbot from Botpress. It answers basic questions about how and where images
are stored for the project, creating an account and logging in, and information about the site's mission.

## Project setup and build

### A) Python installation
1. If you don't have Python installed, go to this link, https://www.python.org/, click on Downloads.
Next, click on the yellow download button under 'Download the latest version for {}' where the '{}' 
represents the name of your operating system. For example, if you use Windows, it would show 'Download
the latest version for Windows'.
2. Locate the downloaded Python installer file from your Downloads folder and double-click on it to run
the installation process. Once you see the Installer's welcome screen, click on the 'Install Now' option.
3. Check that the installation directory chosen is correct and click 'Install' to start the installation
process.
4. Once the installation is complete, you can check the version of Python by typing the following command 
in your command prompt: `python --version`
   
### B) PyCharm IDE setup
1. Go to official JetBrains website for PyCharm by typing "JetBrains PyCharm download" in the search bar in
Google. Click on the first link. Once you are on the site, select the free Community Edition, or the paid 
Professional Edition.
2. Choose the installer based on your operating system:
   a) If you are a Windows user, download the .exe installer and run it. Once it's done, you can create a desktop
      shortcut and associate .py files with PyCharm during the installation.
   b) If you are a macOS user, download the .dmg disk image. Once it is finished, open the image and drag it 
      to your Applications folder.
   c) If you are a Linux user, you can download the .tar.gz archive and follow the instructions on the JetBrains
      website to unpack and run it
3. Once the PyCharm IDE has installed, launch the application from your computer. Then, choose to create a new
   project or open an existing one.
4. If you create a new project for the first time, PyCharm will prompt you to select a Python interpreter. 
   Otherwise, go to File > Settings (Windows/Linux) or PyCharm > Preferences (macOS), navigate to Project: {} > 
   Python interpreter where the '{}' represents your project name. For instance, if your project is called 
   'MyFirstProject', you would go to Project: MyFirstProject > Python interpreter.
5. From here, select the existing Python installation or click the gear icon to configure a new one.

### C) PostgreSQL setup
1. Visit the official PostgreSQL download page: https://www.postgresql.org/download/
2. Select your operating system:
   a) If you have windows, choose between the interactive installer by EDB (recommended for most users), or 
   the zip archive (for advanced users).
   b) If you have macOS, choose between the Postgres.app or the Homebrew installers. You can also download the 
      EDB macOS installer.
   c) If you have Linux, select from any of the distributions like Ubuntu or Debian suggested. It is recommended
      that you use your distribution's package manager as it simplifies installation and updates.
3. Download the installer. Once it is finished, click on the application and follow the on-screen instructions, 
   which might involve choosing installation paths, setting passwords, and configuring ports.
4. Once it is installed, open a terminal or command prompt and type psql. If it launches successfully, 
   you're good to go!
   
### D) Postgres.app configuration
1. If you have a Postgres.app on your macOS, you can create your database, tables, and connect your database
   to your application using psql. You can look at the instructions for doing so here: https://postgresapp.com/.
2. If you are using a normal PostgreSQL installer, check this link: https://www.digitalocean.com/community/
   tutorials/how-to-use-a-postgresql-database-in-a-flask-application.
3. You will also need to create a .env file by going to the `app` folder on the project, right-click `app` to
   create a new file, enter the file name as `.env` and enter values for these keys: 'FLIGHT_API_KEY', 
   'FLIGHT_API_SECRET', 'SQLALCHEMY_DATABASE_URI', 'SQLALCHEMY_TRACK_MODIFICATIONS', 'SQLALCHEMY_ECHO', 
   'DEBUG_TB_INTERCEPT_REDIRECTS', 'SECRET_KEY', and 'CURR_USER_KEY'.
   a) In your `.env` file, you should have values for these keys: SQLALCHEMY_TRACK_MODIFICATIONS=False,
   SQLALCHEMY_ECHO=False, DEBUG_TB_INTERCEPT_REDIRECTS=True.
   b) For keys, 'SECRET_KEY' and 'CURR_USER_KEY', you can create any values you want, but it is 
   recommended you make the values more complex, yet easy to remember. Make sure to put quotation marks
   around the values.
   c) For the key, 'SQLALCHEMY_DATABASE_URI', set it to `postgresql:///name_of_postges.app_database` if you
   are using Postgres.app. Otherwise, check the link described in step 2 for assistance. Make sure the values
   are surrounded by normal quotation marks.
   d) For the second key, use this format, `b'flight_api_secret_value'` where you assign a complex and readable
   value. Do this after you acquire the value for the 'FLIGHT_API_KEY'. In order to register for the api, go to
   the SerpAPI link: https://serpapi.com/.
      i.) If you don't have a SerpAPI account, create an account first.
      ii.) Once you have signed up, save your API key to the 'FLIGHT_API_KEY' variable in the `.env` file.
      iii.) Finally, choose the "google_flights" engine parameter under SerpAPI engine.
   
### E) Other steps
1. Before you start your project, you need to create a bot. To get started, sign up for a free Botpress Cloud
account using this link: https://botpress.com/.
2. Log in using your new account, click "Create Bot" and choose a name for your chatbot.
3. Follow the first ten minutes of the Botpress video to get started on building the conversation flow for the
chatbot using this link: https://www.youtube.com/watch?v=8rZU51GjvlE&t=999s. Create the flow such that the chatbot
can respond to users' questions about the Newgen site, such as how to login and signup or figuring out which 
footer clicks are usable. Allow the chatbot to respond to a question differently. For example, a user may say
they can't log in or that they are having login issues, and the chatbot should respond with an answer, such as "The login
button can be found by clicking on the 'Login' button on the home page and selecting the 'Login' button on the 
login/signup page".
4. Once you are done, publish the chatbot by clicking on the 'Publish' button. 
5. Go back to the home page, select your chatbot, click on 'Integrations', and check the 'Enable Integration' 
   and 'Using new' switch buttons.
6. Scroll down to 'Embed code' and right-click around the window showing the script soruces.
7. In your 'index.html' file located under the file path, '/app/blueprints/index/templates', insert the script sources
   you copied from Botpress into the script block: {% block script %}{% endblock %}. Make sure you have defer after
   the src attribute for each script.
   
### F) Project build
1. From the github repository, go to Code and copy the HTTPS github repository url to your clipboard.
2. In your command prompt, find or create an empty directory and run `git clone git_repo_url_link` to
clone the repository to your local machine. If you don't have `git` installed, follow the instructions 
on this website: https://github.com/git-guides/install-git.
3. On your command prompt, go to the directory with your `git` repo using a command like `cd folder_with_repo`
from macOS to make sure you can access the project content. 
4. Launch PyCharm from your computer, click on 'Open project', and select the folder with the git 
repository.
5. Inside your IDE, open a new command prompt window, navigate to your `git` repo and run `pip install -r 
requirements.txt`. Make sure you are in your root directory while you do this. Once PyCharm finishes
downloading the required libraries, you can run the app in the command prompt using the command, `flask run`
or select the green run button in app.py located next to the line where it shows: `if __name__ == __main__:`
6. If you decide to use a `venv` folder to run your application, run the commands `python -m venv venv` to 
create the `venv` folder and `source venv/bin/activate` to use your `venv` environment for your application.
Like the previous step, make sure you are in your root directory.
7. To deactivate your `venv` environment, type `deactivate` in your command prompt.

## Tips and Troubleshooting

1. If you have a python version less than 3.0 or above, use the `python` command. Otherwise, use `python3`.
For python versions less than 3.0, use `pip` or `pip2`. Otherwise, use `pip` or `pip3`. 
2. While you are installing Python, try checking the box next to “Add Python 3.x or 2.x to PATH” before proceeding with 
   the installation. This will ensure that Python is added to your system’s PATH variable, making it easier to run 
   Python from the command prompt.
3. When you are installing Python, you can customize the installations by selecting 'Customize installation'.
4. Before you configure the PyCharm interpreter, make sure Python is installed first.
5. If you can't use the `psql` command, try typing the command as shown exactly or try the full path to the psql 
   executable (e.g., /usr/local/bin/psql on some Linux systems) to see if it launches.
6. If you are experiencing issues with your chatbot, try inserting the chatbot scripts from Botpress into your 
   'index.html'. Since Botpress gets updated regularly, it is a good idea to have scripts with the newest Botpress
   version.
7. When you use the round trip and sign-in forms on the home page or in the flights page, you can consult SerpAPI's 
Google Flights API documentation here for reference: https://serpapi.com/google-flights-api
8. You can check the data types of the values when you fill out some forms or try io insert data into the tables
by going over the forms and models sub-folders in the main folder.
9. If you get a TypeError warning when you run the tests, you can ignore it. When you use the web application,
everything will work normally.
10. If you create a review for a payment, and you want to edit it, you may get an error saying the value for the
timestamp is invalid. In that case, use the format, '%Y-%m-%d %H:%M:%S', to enter the timestamp value. Also, if
you want to edit the timestamp value whe you created the review, simply remove the decimal part of it.

## Running Tests

To run the tests from the repository, make sure you are in your project directory and enter the command, 
`python3 -m unittest`or `python -m unittest` if you have a version of python less than 3.0.

## Future Development

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
