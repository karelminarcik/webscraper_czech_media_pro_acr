#!/bin/bash

# Instalace Google Chrome
echo "Installing Google Chrome..."
curl -sSLo google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get update && apt-get install -y ./google-chrome.deb
rm google-chrome.deb

# Instalace ChromeDriver
echo "Installing ChromeDriver..."
CHROME_VERSION=$(google-chrome --version | awk '{print $3}')
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
curl -sSLo chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip chromedriver.zip -d /usr/local/bin/
rm chromedriver.zip
chmod +x /usr/local/bin/chromedriver

echo "✅ Chrome & ChromeDriver installed!"
