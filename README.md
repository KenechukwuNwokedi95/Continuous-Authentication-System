# Continuous-Authentication-System

# Introduction

**Continuous Authentication System**  was created for continual authentication using Keystroke and mouse scroll to aid a continuous authentication system. This system will be leveraging a pre-trained machine learning model to determine the different users on a platform through their interactive keystroke and mouse scroll with a system. The ML model is built on a secondary Keystroke Mouse data with features such as Dwell average, Flight average, Trajectory average etc.


# How it Works ?
We collected user keystrokes as the user enter his/her details on the registration page then keystrokes is pass to the pretrained model which will bw used to predict if its the same user typing on the messaging page and the authentication interval time is every minute, this is why we called it continuous authentication.

<br/>

## What Problem it Solves ?
It potentially solve in personification and can serve as additional security to a platform
# Tech Stack

- [HTML](https://www.w3schools.com/html/) - The front-end development language used for creating extension.

- [CSS](https://www.w3schools.com/css/) - The  front-end development language used for creating extension.

- [Python](https://www.python.org/) - The Programing Language used to parse features from a website and for training/testing of the ML model.
- [JavaScript](https://www.javascript.com/) - The scripting language used for creating the extension and sending  requests to the served Ml model.

- [scikit-learn](https://scikit-learn.org/stable/) -
  The library used for training ML models.
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) - This is server side that host the platform and I used localhost.
<br/>

# Usage

## Directory Structure

```
.
|-- LICENSE
|-- README.md
|-- Server
|   |-- svm(4)_model(1).pkl
|   |-- rf_model.pkl
|   |-- gbm_model.pkl
|   |-- ensemble.pkl
|-- static
|   |-- style.css
|   `-- style2.css
|-- Templates
|   |-- chat.html
|   |-- register.html
|-- user_data
|-- requirements.txt
`-- app.py
```


## Backend - Ml Model




