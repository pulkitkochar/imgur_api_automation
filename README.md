## Pre-requisites ## 

Install python3

Install virtualenv (pip/pip3 install virtualenv)


## Virtual Env Activate ##

inside this directory, run following commands:

virtualenv automation-env -p python3.6.5

source automation-env/bin/activate

pip install -r requirements.txt


## Driver Installation ## (Not needed for api testing)
For Firefox:
brew install geckodriver

For Chrome:
brew cask install chromedriver



## How to Run ##
behave                                             ----- to run all tests without initialising browser

behave -D BROWSER=chrome -D HEADLESS=False         ----- to run all tests in chrome driver in browser mode 

behave -D BROWSER=firefox                          ----- to run all tests in firefox driver 

behave -w                                          ----- to create test data to test all flows manually

behave -i abc.feature                              ----- to run a specific feature file

behave -n "user login"                             ----- to run a specific scenario

PS: -D is used to pass command line arguments

