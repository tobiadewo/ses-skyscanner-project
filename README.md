# Skyscanner Project

This repository contains a Flask-based flight searching website that I made in 2021.

This project works by taking user input to make API calls to Skyscanner, a travel agency. The information gained from these API calls are displayed graphically on a webpage created using HTML and CSS. This application also utilizes an SQL database to store information on countries supported by Skyscanner's API, their ISO 3166-1 alpha-2 country codes, and their currencies.

The Skyscanner API has been deprecated since the creation of this project, and so it no longer functions, but I plan to find a suitable replacement API in the near future.

## How to run
1) Clone this repository.
```
git clone https://github.com/tobiadewo/ses-skyscanner-project
```
2) Inside your cloned repository, create and activate a virtual environment.
```
py -3 -m venv .venv
.venv\Scripts\activate
```
3) Download the required packages.
```
pip3 install -r requirements.txt
```
4) Retrieve an API key and use it to set the *key* variable in `config.py`.
5) Run the application.
```
flask run
```

## Screenshots
![image](https://github.com/user-attachments/assets/90df660a-973b-462d-ba32-0edede37874d)
