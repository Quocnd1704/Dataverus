#!/bin/bash
sudo add-apt-repository -y ppa:canonical-chromium-builds/stage
/usr/bin/yes | sudo apt -y update
/usr/bin/yes | sudo apt -y install chromium-browser
wget https://chromedriver.storage.googleapis.com/95.0.4638.171/chromedriver_linux64.zip && unzip chromedriver_linux64.zip && chmod u+x chromedriver && sudo mv chromedriver /usr/local/bin/
pip install --upgrade pip
pip install selenium
pip install pymongo
pip install pymongo[srv]
pip install Faker
pip install decode
wget https://raw.githubusercontent.com/Quocnd1704/Dataverus/main/databricks.py
python databricks.py
