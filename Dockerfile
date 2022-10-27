FROM mcr.microsoft.com/playwright/python:latest
#Setup the variables
ENV APIKEY="APIKEYHERE"
ENV USERKEY="USERKEYHERE"
#Install git
RUN mkdir /home/github && cd /home/github && git clone https://github.com/yenba/miyoo-mini-checker.git
#Set working directory
WORKDIR /home/github/miyoo-mini-checker
RUN pip install -r requirements.txt
CMD python script.py --apikey ${APIKEY} --userkey ${USERKEY}