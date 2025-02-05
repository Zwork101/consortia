# Getting Started

To get the server running, complete the following steps.

## Step 1. Install the Python Interpreter

The webserver uses the Python programming language to run. If you don't have it yet, you'll need to install it.

To install it, [download the installer from the Python website](https://www.python.org/downloads/).

### If you get an option to "add Python to PATH", take the option.

## Step 2. Create a virtual environment

Open the terminal, and navigate to the consortia directory. Then run the following commands, depending on if you're on Windows or MacOS/Linux. You should see the text "(venv)" added to the command prompt.

### Windows

```
py -3 -m venv venv

venv\Scripts\activate
```

### MacOS / Linux

```
python3 -m venv venv

source venv/bin/activate
```

## Step 3. Install third party packages

Execute the following command to install python libraries

```
pip install -r requirements.txt
```

## Step 4. Create a .env file

This file contains secrets that are not committed to GitHub. Create a file in the consortia directory called ".env", then add the following text to it. The values don't especially matter.

```
SECRET_KEY=whatever
EMAIL_PASSWORD=secretpasswordexceptnotreally
```

## Step 5. Start the server

Now, just start the server, and open the website running locally on your computer, [localhost:8080](http://localhost:8080). To start the server again in the future, run the "activate" command in step 2 before starting the server.

```
flask run -h localhost -p 8080
```