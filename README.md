# SFS-Threat-Intel

Warning: This is an unfinished product and will likely not be worked on in the near future due to the product being cancelled. Some features mentioned in this may not be fully implemented or available. Some noticeable features that are missing are weather checking, traffic alerts, and social media checking. 

Warnining: This code needs a complete refactor. The code works, but this is by no means readable. You have been warned. 

This code is licensed under Licensed under Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0). Reference license file for use of this code.

This code is a Python-based threat intelligence program that scans the internet for any trending positive/negative media and/or dangerous security events relating to the Scottsdale Fashion Square and the Scottsdale area as a whole. The current information this program collects includes but currently not limited too online news articles, social media posts from Instagram, Facebook, and Twitter, traffic alerts for Scottsdale, and the current forecast (including any severe weather alerts). After results are finished, it will send it to a specified email recipient. As of this writing, only the articles function and send_emails function works, and all other functionality does not. 

# USING THIS CODE

To use this code, you'll need to modify the code. For one, I removed my personal email and the receiver email. You'll need to specify a sender email (along with a password) and a receiver (you'll need to modify the code to select multiple receivers). Also, you'll need to modify the queries section and the keywords section. The queries section is basically what you put into the google search bar. Right now, it is targeting only the Scottsdale mall. You'll need to modify it to your needs. Also, you'll need to modify for keywords. Right now, it is only focused on security events relevant to the mall. You'll need to modify it to your needs. 

