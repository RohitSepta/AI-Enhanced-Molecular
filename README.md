
# VectorDB project

By below given steps, you should be able to successfully set up and run the TEST_TASK project.

## Prerequisites

Python 3.10.13: Ensure you have Python 3.10.13 installed on your system. You can verify this by opening your terminal or command prompt and running

```bash
python --version
```

If you don't have Python 3.10.13 or need to install it, download the appropriate installer from the official Python website: https://www.python.org/downloads/windows/ for Windows and https://docs.python-guide.org/starting/install3/linux/ for Linux and macOS.


## Setting Up the Environment

1). Navigate to the project directory: Open your terminal or command prompt and navigate to the directory containing the TEST_TASK project files. You can use the cd command to change directories. For example:

```bash
cd TEST_TASK
```

2).Activate the virtual environment: This step ensures that the project uses its own isolated set of dependencies, preventing conflicts with other Python environments on your system. Run the following command to activate the virtual environment:

```bash
source env/bin/activate
```

Note:- Virtual environment already created in project, you have to only activate it.


## Installing Dependencies

1). Install required packages: The project uses dependencies specified in the requirements.txt file. Run the following command to install them using pip, the Python package installer:

```bash
pip install -r requirements.txt
```

## Running the Application

1). Start the development server: With the virtual environment activated and dependencies installed, run the following command to start the Flask development server:

```bash
flask run --debug
```

The server will typically start on http://127.0.0.1:5000/ (localhost, port 5000) by default. You can access the application in your web browser by visiting this URL.
