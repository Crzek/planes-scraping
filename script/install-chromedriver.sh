CHROME_VERSION=”google-chrome-stable”
CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0–9]+)(\.[0–9]+){3}.*/\1/")
#.    Please note that the steps mentioned below now can be 
#.    replaced with Web driver manager which do the the download
#.    and setup of driver
CHROME_DRIVER_VERSION=$(wget — no-verbose -O — “https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}");
echo “Using chromedriver version: “$CHROME_DRIVER_VERSION
wget — no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
rm -rf /opt/selenium/chromedriver
unzip /tmp/chromedriver_linux64.zip -d /opt/selenium
rm /tmp/chromedriver_linux64.zip
mv /opt/selenium/chromedriver /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION
chmod 755 /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION
ln -fs /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION /usr/bin/chromedriver