## Microservices & Cloud Computing (CSC 5201) - Healthcare Management System - Final Project

### Project Overview:
A microservices-based application for managing healthcare data and services. The application encompasses various modules, including patient management, appointment scheduling, and medical records management, all designed using a microservices architecture with REST APIs for communication.

### Overall App Design: 
1. GUI Service: Provides the user interface for interaction with the system, including views for patient management, appointment scheduling, and medical records.
2. Medical Records Service: Manages the creation, modification, and retrieval of medical records.
3. Patient Management Service: Handles patient data management and integrates a machine learning model for risk prediction
4. Appointment Scheduler Service: Manages scheduling of appointments and coordinates times between patients and healthcare providers.


Platform used to deploy the app is DigitalOcean Droplet and Docker Compose is utilized to manage the containerization of services, allowing for easy deployment and scaling.


### To run the project:
**Prerequisites**

a) Log into mongodb and create your own project and cluster.

b) Create a Database called ***healthcare***

c) Create three collections in the database: ***appointment-scheduler***, ***medical-records***, and ***patients***

d) Get your connection string: click on Database -> Connect (in the created cluster) -> Drivers -> Click Python in dropdown -> copy the connection string visible

e) After cloning the repository, enter your connection string in the `docker-compose.yml` file (for the specific app version described below you want to run) and for all of the `app.py` files in each microservice.

**App Versions**

While the functionality mostly remains the same, below are the descriptions for each folder in this repository:
1. `/local-healthcare-manager`: Runs the healthcare management system locally. after switching into the directory, run `docker compose up --build -d` to get the application started. Navigate to localhost:5000 and it should work as expected!
2. `/d-ocean-healthcare-manager`: Runs the application on a digital ocean droplet. To do this, log into to DigitalOcean and create a droplet. Install Docker<sup>1</sup> on the DigitalOcean Droplet. After doing this, copy the ipv4 of the Droplet as displayed in the DigitalOcean UI. Navigate to your console and `ssh` into the droplet by typing `ssh root@<ipv4-address>`. Create a folder called `healthcare` in the droplet. Use `scp -r <local-repo-folder-location/d-ocean-healthcare-manager> ~/healthcare` in a new window (on your local machine) to copy over the local files onto the Digital Ocean droplet. After switching into the directory, run `docker compose up --build -d` in the Droplet connection window to build the application. The application should then be running at ipv4-address:5000 .
3. `/ml-do-healthcare-manager`: Contains additional data & training Scripts for Patient Risk prediction ML model - has the training dataset and scripts necessary to train and serialize the ML model used in patient management. To run this, repeat the steps above for `/d-ocean-healthcare-manager` and it should run.


### Use Case Screenshots:
**Homepage**
![Screenshot (757)](https://github.com/sumedhars/healthcare-management-project/assets/93266225/e5e80e39-6970-4c3d-a541-fbc6339b3292)

**Sample Documents stored in MongoDB & Database-Collection structure**
![Screenshot (772)](https://github.com/sumedhars/healthcare-management-project/assets/93266225/e3718ccb-10b7-45ac-89db-af25f229648f)



### Author
Sumedha Sanjeev

sanjeevs@msoe.edu


### References:
1. https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04
   (When following the tutorial, make sure to add `docker-compose` in addition to `docker-ce`).
