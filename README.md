# AIRMED - doctor appointment application

*Developed and designed as part of Milestone Project 3: Python and Data Centric Development*

[Please view the live project here](#)

## Table of Contents

<details>

  <summary>Click to expand table of contents</summary>

1. [Overview](#overview)
2. [User Experience UX](#user-experience-ux)
    - [User Stories](#user-stories)
        - [Visitor Stories](#visitor-stories)
    - [Strategy](#strategy)
    - [Scope](#scope)
    - [Structure](#structure)
    - [Skeleton](#skeleton)
    - [Design](#design)
    - [Color Scheme](#color-scheme)
    - [Fonts](#fonts)
    - [Imagery](#imagery)
    - [Logo](#logo)
    - [Icons](#icons)
3. [Features](#features)
    - [Existing Features](#existing-features)
    - [Future Implementation](#future-implementation)
4. [Technologies](#technologies)
5. [Testing](#testing)
6. [Deployment](#deployment)
    - [GitHub pages](#github-pages)
    - [Forking the Repository](#forking-the-repository)
    - [Local Deployment](#local-deployment)
7. [Credits](#credits)
    - [Code](#code)
    - [Media](#media)
    - [Content](#content)
8. [Acknowledgements](#acknowledgements)
9. [Disclaimer](#disclaimer)

</details>

# Overview

The project was created as a **Milestone Project 3** as a part of **Diploma in Full Stack Software Development** with **Code Institute**. The project is developed using Python, JavaScript, HTML, CSS, and Materialize framework.

# User Experience (UX)

## User Stories

### Visitor Stories

## Strategy

### Project Goals

- Attractive and good quality UI design

- The main function of doctor appointment app is to make the app accessible for each and every potential user who is potential patient.

## Scope

## Structure

## Skeleton

## Design

### Color Scheme

Delicate and soothing color palette will be chosen for medical app. Users should feel calm and comforted when opening AIRMED app, knowing that they have come to the right place to address their healthcare needs, questions, and any concerns.

- Celadon Blue (#247ba0)
- White (#FFFFFF)
- Green Sheen (#70C1B3)
- Turqouise Green (#b2dbbf)
- Mango Tango (#f68c48)

Mainly cold colors will be selected throughout the app in order to establish an overall sense of tranquility that is necessary to help users concentrate on the more important app features.

White will be primarily used as the background because it represents reverence, purity, and innocence. This association calms people and influences their brain activity in a very positive way. Blue color symbolizes a sense of calm, peace harmony, trust and knowledge. Celadon Blue will be used to promote a tranquil environment for the users. Green is  associated with health, good luck, youth, vigor, generosity, and fertility. A variaty of orange color (Mango Tango) will be used sparingly as button highlighters.

### Fonts

- Two fonts will be used throughout the project, **Roboto** and **Montserrat**. Both will be used with ``sans-serif`` font as a fallback.
**Montserrat** will be used for the main headings and **Roboto** will be used for the hero text, paragraph sections and the footer.

- These fonts pair very well together and make the website appear both prestigious and contemporary. They make a good combination of tradition and modernity.

- Fonts were imported from [Google Fonts](https://fonts.google.com/).

### Imagery

### Logo

- I used [Canva](https://www.canva.com/) to design the custom logo. 

### Icons

Icons should be obvious and very intuitive so that users can easily understand what a particular icon represents. Also, a detailed heading will be used for each icon to describe top specialities the Airmed clinic offers. 

# Features

AIRMED doctor application will be built to be fully responsive mobile-first. This will be primarily achieved by utilizing the Materialize's grid system.

## Existing Features

## Future Implementation

## Languages

- [HTML5](https://en.wikipedia.org/wiki/HTML5) was used to complete the structure of the website.
- [CSS3](https://en.wikipedia.org/wiki/CSS) was used to style the website.
- [Python](#)
- [JavaScript](https://en.wikipedia.org/wiki/JavaScript) was used to make webpage interactive.

## Frameworks, Libraries and Programs

## Validation
- [W3C Markup Validation Service](https://validator.w3.org/) was used for Markup validation.
- [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) was used for CSS code validation.
- [JSHint](https://jshint.com/) was used for JavaScript code validation.


# Testing

Testing process was written in a separate file. 
Please click [here](testing.md) for the testing process.

# Deployment

## Clone the GitHub Repository

## Database Deployment

## Version Control

[Git](https://git-scm.com/) as a local repository and [GitHub](https://github.com/) as a remote repository were used for this project. Detailed elaboration please find below:

1. Create a remote repository in GitHub by clicking **"New repository"** on the main page<br>

2. Use **Code Institute Template**, put the repository name and click Create Repository making sure to select public<br>

3. Open the repository with [Gitpod](https://www.gitpod.io/). By using Code Institue Template, initialisation including initial commit is done so no need to do `git init` command when open IDE, or to use `git push -u origin main` command for my first commit. `gitignore` file, which is very important for the project including some confidential information, is created with Code Institute template so not necessary to create it.<br>

## Deploy to Heroku

The website of this project requires back-end technologies such as server, application, and database so the website is deployed in [Heroku](https://www.heroku.com/), which is a cloud platform with a service supporting several programming languages, because GitHub can only host a static website

Before deploying the website to Heroku, there are three important steps to follow to make the application work in Heroku correctly.

1. Create `requirements.txt` file that contains the names of packages being used in Python. It is important to update the file if other packages or modules are installed during the project.
2. Create `Procfile` that contains the name of the application file so that Heroku knows what to run.
3. Push them into GitHub.

Once above steps have been followed the website can be deployed. Please find the steps of the deployment in Heroku:

1. Create an account in Heroku

2. Click **New** & **Create new app** to create a new app

3. Put an app name, which must be unique, choose a region and click create app

4. Go to **Deploy** section and click **Connect to GithHub**

5. Search for the repository by the repository name and connect it

6. Before clicking Enable Automatic Deploys, hidden variables such as IP address, PORT, SECRET_KEY, MONGO_URI and MONGO_DATABASE need to be recorded in Heroku. Go to **Settings**, click **Reveal Config Vars** and fill out necessary keys and values.

7. Once all the hidden variables are recorded, then click **Enable Automatic Deploys** and click **Deploy Branch** (Main should be selected unless you want other branches to be deployed).

8. When the app is deployed by Heroku correctly, there is a confirmation message and you can access the app.

**Note**<br>
*It is important NOT to set `debug=True` when deploying the website. As this is a project for my study, I keep `debug=True` even after the deployment but only while the app is being built and make sure to change it to `debug=False` before the submission*.

### Connecting to Mongodb
From the CLI:



`mongo "mongodb<url connection string>" --username root`

## Deployment Platform

#### Creating a Heroku app


# Credits

## Code

## Media

### Images

### Icons

## Content

Below websites were used for a general layout inspiration:

The text was adapted from:

# Acknowledgements

- My mentor, Mr. Spencer Barriball, for the helpful feedback and guidance.
- [Code Institute](https://codeinstitute.net/) for all course materials and ongoing support.
- Fellow Code Institute students for their feedback and suggestions.
- My family and friends for testing and useful feedback.

# Disclaimer

The information provided on this website is for educational purposes only.