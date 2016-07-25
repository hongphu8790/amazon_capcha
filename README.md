#amazon_capcha
##Environment
Ubuntu 16.04

Python 2.7

##Requires
sudo apt-get -y install tesseract-ocr

sudo -H pip install Pillow pytesseract

##Installation and Usage
git clone https://github.com/wangchuande/amazon_capcha.git

cd amazon_capcha

python download_capcha.py

##About
the program will download the capcha into the amazonpicture directory

the image name is recoginzed result

open the picture and verify the result
