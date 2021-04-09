# automatic-test-ui
Automatic Test UI Tool using LinkChecker(https://github.com/linkchecker/linkchecker) and Selenium

## Installation

1. Install packages
`pip install -r requirements.txt`
2. Download Browser Driver  
detail guide at: https://selenium-python.readthedocs.io/installation.html#drivers

Install Driver for chrome 89 for linux  
`curl -O https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip && unzip chromedriver_linux64.zip && sudo cp chromedriver /usr/local/bin`
## USAGE
- `python3 main.py -h` for helps  
- `python3 main.py your-url`  
- find result at result/check_result.csv

## Run with selenium plugins
Common to check a html componet on all html page. The result of plugin check included in "**warning**" column in csv file and console.  
Current, Have only one plugins for **sample purpose**, see ModalCheck in selenium_plugins/
- `python3 main.py your-url -p ModalCheck`
