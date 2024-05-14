Welcome to the UMBC Financial Wellness Assistant!

Steps to deploy on a development server
1.	Download and install MongoDB onto the host machine at https://www.mongodb.com/.
2.	Extract the source code at https://github.com/reberly1/Capstone-SFWA.
3.	Ensure that the system environment has the dependencies, so they match the requirements provided in requirements.txt using the command: pip install -r requirements.txt
4.	Ensure that the system has the most recent installation of the python programming language at https://www.python.org/.
5.	Change the "HOST" constant variable in scraper.py and database.py to match the connection string for your MongoDB database.
6.	Run the following commands in the terminal to activate the server from your machine (note this is for testing purposes, for true deployment knowledge of the host system architecture and policies of the organization will be required for broader deployments).  
a.	Cd website (To Naviate to the website folder of the project)  
b.	Python ./scraper.py (Scrapes an updated version of the opportunities from academic works)  
c.	Flask run (Activates a development server to run the application)  

File Naviation:
There are three primary sections within this application (Calculator Suite, Milestone Tracker, and Scholarships/Profiles)

Calculator Suite Code:
1. Lines 36-213 of app.py for flask route handling
2. functions.py for calculations
3. Relevant HTML Files found in templates:  
   a. layout  
   b. guided  
   c. guided_estimates  
   d. guided_terms 
   d. guided_loans  
   e. report  
   f. unguided  

Milestone Tracker: 
1. Lines 214-665 in app.py for flask route handling
2. functions.py for calculations
3. database.py for saving logs via profile
4. Relevant HTML Files found in templates:  
   a. layout 
   b. loan_log 
   c. log  
   d. milestone  
   e. repay_log  

Scholarships/Profiles:
1. Lines 666-824 of app.py for flask route handling
2. database.py for saving/loading profiles and scholarships
3. scraper.py for extracting scholarships
4. Relevant HTML Files found in templates:  
   a. layout  
   b. login  
   c. profile  
   d. reg_admin  
   e. register_menu  
   f. register   
   g. scholarships  
