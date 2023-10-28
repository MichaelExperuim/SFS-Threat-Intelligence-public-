import os  # For checking if file exists
import random  # For generating random numbers
import re  # For regular expressions
import sys  # For exiting program and printing error messages
import time  # For sleeping
import traceback  # For printing stack trace when exception occurs
from datetime import datetime, timedelta  # For date range
from urllib.parse import urlparse  # For parsing URLs
import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML
from googlesearch import search  # For searching Google
from textblob import TextBlob  # For sentiment analysis
import smtplib  # For sending emails
from email.mime.multipart import MIMEMultipart  # For sending emails
from email.mime.text import MIMEText  # For sending emails
from email.mime.application import MIMEApplication  # For sending emails

all_articles = []
def get_news_articles(queries):
    print("Beginning search...")
    phrases = ["bomb", "robbery", "theft", "burglary", "riot", "protest", "shooting", "crime", "incident", "police", "officer-involved", "accident", "evacuation", "fire", "cyberattack", "cyber", "scam", "security",
    'sexual assault', 'stabbing', 'sex assault', 'sexual conduct', 'kidnapping', 'kidnapped', 'rape', 'cop', 'protestors', 'protestor']
    
    # Create a dictionary for each article
    article = {
        'title': '',
        'date' : '',
        'title-sentiment': '',
        'title-polarity-score': '',
        'url': '',
        'found-phrases': '',
        'phrase-output': '',
        'article-sentiment': '', 
        'article-polarity-score': '',
    }
    
    start_time = time.time()
    print(" The current time is: ", datetime.now().strftime("%H:%M:%S"))
    
    # Load already sent URLs from file if it exists
    
    # Define the headers with the User-Agent. Used to mimic a browser and prevent Google from blocking the request
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    if os.path.isfile("duplicate_urls.txt"):
        print("duplicate_urls.txt exists. Loading...")
        with open("duplicate_urls.txt", "r") as f:
            existing_urls = f.read().splitlines()
    else:
        print("Duplicates file does not exist. Creating...")
        with open("duplicate_urls.txt", "w") as f:
            f.write("")
        existing_urls = []
    
    for query in queries:
        start_time = time.time()
        print(" ")
        print("Start time: ", datetime.now().strftime("%H:%M:%S"))
        print(f"Searching for {query} in Google... ")
        
        # Create a new URL set for each query
        url_set = set()
        
        # Search for news articles using the Google Search API, put every query into double quotes to search for the exact phrase
        # Might want to modify date range be longer than 3 days
        # Modify the date range here. Default is 7 days ago to today. 
        days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')       
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Search result. Max attempts is 5, max unique articles is 10. Program will stop searching if either of these conditions are met and move on to the next query
        max_search_attempts = 5
        max_unique_articles = 10
        #limit = 0
        search_attempt = 0
        unique_articles = 0
        num_results = 10 # Number of results starts at 10 and increases by 10 each time until max unique articles is reached

        while unique_articles < max_unique_articles and search_attempt < max_search_attempts: 
            
            # If unique_articles is not empty, set the max unique articles to the number of unique articles found so far. If it is empty, do not declare unique_articles
            print("Unique articles: ", unique_articles)
            if unique_articles > 0:
                unique_articles = urls_found
            else:
                print("Unique articles is empty. Continuing...")
            search_attempt += 1 # Increment search attempt
            
            print("Searching for articles from " + days_ago + " to " + today + " with attempt #" + str(search_attempt) + " of " + str(max_search_attempts) + " attempts and " + str(num_results) + " results... ") 
            urls_found = 0  # initialize count of unique URLs found in this search attempt
            
            # Can modify by date, domain, language, types of content
            #for url in search(query + ' after:' + days_ago, tld='com', lang='en', num=num_results, start=0, stop=num_results, pause=10.0):
            for url in search("News articles about " + query, tld='com', lang='en', num=num_results, start=0, stop=num_results, pause=10.0):
                if 'http' in url:
                    # Check if the URL is already in the duplicate_urls.txt file, if it is, mark it as a duplicate and skip it
                    if url in existing_urls:
                        print(url + " already exists in duplicate_urls.txt. Skipping...")
                        time.sleep(3)
                        continue
                    # If the URL is not in the duplicate_urls.txt file, add it to the duplicate_urls.txt file and the URL set
                    else:
                        url_set.add(url)
                        time.sleep(3)
                        print(url + " added to duplicate_urls.txt and URL set.")
                        urls_found += 1  # increment count of unique URLs found in this search attempt
                if urls_found >= max_unique_articles:  # If the max unique articles is reached, stop searching and display the number of unique articles found
                    print("Total unique articles found: " + str(len(url_set)) + ". Terminating search...")
                    print(" ")
                    break
            if unique_articles < max_unique_articles:
                if urls_found == 0 and len(url_set) == 0:  # If no unique URLs found in this search attempt, try again with more results
                    print("No unique articles found. Moving on to next query...")
                    print(" ")
                    break
                elif urls_found < max_unique_articles:  # If some unique URLs found but not enough, try again with same amount of results
                    print("Only found " + str(urls_found) + " unique articles out of " + str(max_unique_articles) + " required. Trying again with increased results...")
                    num_results += 10
                    print("Results increased to " + str(num_results) + "\n")
                    # += 10
                    #print("Limit increased to " + str(limit) + "\n ")
                    print("Number of unique articles found: " + str(len(url_set)) + "\n")
                    unique_articles = len(url_set)
                    print(url_set)
                    print("Sleeping for 10 seconds...")
                    time.sleep(10)
                else:  # If max unique articles reached, stop searching
                    print("Found " + str(urls_found) + " unique articles. Moving on to next query...")
                    print(" ")
                    break

            else:  # If max unique articles reached, stop searching
                print("Max unique articles reached. Moving on to next query...")
                print("Total unique articles found: " + str(len(unique_articles)) + "\n ")
                print(" ")
                break

        print("Number of unique URLs found: ", len(url_set))
        print(" ")
        articles = []
        if url_set == set():
            print("No articles found for this query. Skipping...")
            continue
        else:
            print("Current URL set: ")
            print(url_set)
            print(" ")
        
        print("Searching for articles...")
        for url in url_set:
            try:
                print(url)
                # Check if the URL is already in the duplicate_urls.txt file. If it is, skip it
                if url in existing_urls:
                    print(url + " already exists in duplicate_urls.txt. Skipping...")
                    continue
                # Parse the URL and get the article title and text, store it in soup to use later
                print("Trying to find article at: ", url)
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                #response = requests.get(url, headers=headers, timeout=10)
                
                # Getting too many HTTP 429 errors, this is the code to fix it. Sleeps for 30 min if it receives 429 error. Any other error
                # will be treated as a non-news article, given one more chance, and then skipped.
                retry_delay = 1800 # 30 minutes
                while True:
                    try:
                        response = requests.get(url, headers=headers, timeout=10)
                        response.raise_for_status()  # Raise an exception if the response has an error status code
                        # Print the error code if the response has an error status code
                        if response.status_code != 200:
                            print("HTTP Error", response.status_code)
                            break  # Skip the URL if the request is not successful
                        else:
                            print("HTTP 200 OK")
                            break  # Exit the loop if the request is successful
                    except requests.HTTPError as e:
                        if e.response.status_code == 429:
                            print("Too Many Requests - Sleeping for", retry_delay, "seconds")
                            time.sleep(60)  # Sleep for 1 minute
                            retry_delay += 300  # Increase the retry delay by 5 minutes for subsequent 429 errors
                        else:
                            print("HTTP Error", e.response.status_code, "- Moving to next URL...")
                            break
                    except requests.RequestException:
                        print("Request exception occurred. Broken URL or non-news article. Skipping...")
                        break # SKip the URL if there is a request exception             
                # Check if its xml or html. If its xml, parse it with xml, otherwise, assume html
                if response.headers.get('Content-Type', '') == 'application/xml':
                    print("Parsing as XML...")
                    try:
                        soup = BeautifulSoup(response.text, 'xml')
                    except:
                        print("Error parsing XML. Skipping...")
                        # Display the error message
                        print("Error message: ", sys.exc_info()[0])
                else:
                    print("Parsing as HTML...")
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                try:
                    title_element = soup.find('title')
                    if title_element:
                        title = title_element.get_text().strip()
                        if title == "":
                            print("Error finding title. Renaming...")
                            title = "Error finding title"
                    else:
                        print("Title element not found. Skipping...")
                        title = "Error finding title"
                except Exception as e:
                    print("Error finding title:", e)
                    title = "Error finding title"

                if 'title' not in article or article['title'] == "":
                    try:
                        article['title'] = soup.find('h1').get_text() # Most titles are h1 tags so this is a backup in case the title is not found in the title tag
                    except:
                        print("Error finding title. Renaming..")
                        title = "Error finding title"
                        article['title'] = title
                    # If this doesn't work, then the article title will be "Error finding title"
                found_phrases = []
                
                # Check if any of the keywords are located in the article content, otherwise skip this article
                # Split the article content into a list of words and check if the phrases are in 
                article_text = soup.get_text().lower() # Get the text of the article and convert to lowercase 
                article_words = set(article_text.split())  # Convert the article text to words and create a set
                
                # Find the date of the article. Convert them to a consistent format
                date_patterns = [
                    r'\d{4}-\d{2}-\d{2}',         # YYYY-MM-DD
                    r'\d{2}/\d{2}/\d{4}',         # MM/DD/YYYY
                    r'\d{2}-\d{2}-\d{4}',         # DD-MM-YYYY
                    r'\d{1,2}/\d{1,2}/\d{2}',      # M/D/YY or MM/DD/YY
                    r'\d{1,2}-\d{1,2}-\d{2}',      # D-M-YY or DD-MM-YY
                    r'\d{1,2}\s\w+\s\d{4}',        # D MonthName YYYY (e.g., 1 January 2022)
                    r'\w+\s\d{1,2},\s\d{4}',       # MonthName D, YYYY (e.g., January 1, 2022)
                    r'\d{1,2}\s\w+\.\s\d{4}',      # D MonthAbbreviation. YYYY (e.g., 1 Jan. 2022)
                    # Add more patterns as needed
                ]
                # Stadardize the date format with the following format: YYYY-MM-DD. Will be used to sort later.
                article_date = None
                for pattern in date_patterns:
                    match = re.search(pattern, article_text)
                    if match:
                        article_date = match.group()
                        break

                if article_date:
                    # Convert the extracted date to a consistent format
                    date_formats = [
                        "%Y-%m-%d",                  # YYYY-MM-DD
                        "%m/%d/%Y",                  # MM/DD/YYYY
                        "%d-%m-%Y",                  # DD-MM-YYYY
                        # Add more formats as needed
                    ]
                    
                    parsed_date = None
                    for date_format in date_formats:
                        try:
                            parsed_date = datetime.strptime(article_date, date_format)
                            break
                        except ValueError:
                            continue

                    if parsed_date:
                        formatted_date = parsed_date.strftime("%Y-%m-%d")  # Format the date as YYYY-MM-DD
                        article['date'] = formatted_date
                    else:
                        print("Invalid date format:", article_date)
                        # Keep the original date format if it is not in a recognized format
                        article['date'] = article_date
                else:
                    print("No date found.")
                    # If no date is found, then set it as No date found
                    article['date'] = "No date found"
                
                keywords = ["scottsdale mall", "sfs", "scottsdale fashion square", "fashion square", "scottsdale mall", "mall", "scottsdale fashion", "scottsdale", "fashion", "square", "scottsdalefashionsquare"]
                if not any(keyword in article_words or keyword in title for keyword in keywords):                    
                    print("No mention of the mall found in article or title. Skipping and adding to duplicates_url.txt...")
                    print(" ")
                    # Add the URL to the duplicate_urls.txt file
                    with open("duplicate_urls.txt", "a") as f:
                        f.write(url + "\n")
                    continue
                for phrase in phrases:
                    if phrase in soup.get_text():
                        found_phrases.append(phrase)
                        article['found-phrases'] = found_phrases # Add the found phrases to the article dictionary for that article
                print("Article found!")
                print("Title: ", title)
                article['title'] = title
                print("Date: ", article_date)
                print("URL: ", url)
                article['url'] = url
                
                if found_phrases:
                    print("Beginning phrase extraction and cleaning...")
                    phrase_outputs = []  # List to store the outputs of each phrase

                    # Iterate over each phrase in the found_phrases list
                    for phrase in found_phrases:
                        output = ''  # Variable to store the output for the current phrase

                        # Split the text into sentences using regular expressions (period, question mark, exclamation mark)
                        for sentence in re.split(r'[\.\?!]', soup.get_text()):
                            # Check if the current sentence contains the phrase as a whole word
                            if re.search(r"\b" + re.escape(phrase) + r"\b", sentence, re.IGNORECASE):
                                # Find the start and end indices of the phrase within the sentence
                                start_index = sentence.lower().index(phrase.lower())
                                end_index = start_index + len(phrase)

                                # Extract the substring around the phrase with the specified character limit
                                extracted_output = sentence[max(start_index - 75, 0):end_index + 75].strip()

                                # Add elipses to the beginning and end of the output if the phrase is not at the beginning or end of the sentence
                                if start_index > 0:
                                    extracted_output = "..." + extracted_output
                                if end_index < len(sentence):
                                    extracted_output += "..."

                                output += extracted_output + " "  # Add a space instead of a new line

                        # Add the cleaned output for the current phrase to the phrase_outputs list
                        phrase_outputs.append(output.strip())  # Strip the leading and trailing spaces

                    # Remove both the phrase and the phrase output from the found phrases list if the output is empty
                    found_phrases = [phrase for phrase, output in zip(found_phrases, phrase_outputs) if output != '']
                    phrase_outputs = [output for output in phrase_outputs if output != '']

                    print("Updated found phrases:", found_phrases)
                    article['found-phrases'] = found_phrases

                    # Remove excessive whitespace from the output and join lines with a space instead of a new line
                    cleaned_outputs = []
                    for output in phrase_outputs:
                        cleaned_lines = [line.strip() for line in output.splitlines() if line.strip() != '']
                        cleaned_output = ' '.join(cleaned_lines).strip()  # Join lines with a space instead of a new line

                        # Limit the output to 150 characters with ellipses (...) at the beginning and end if it exceeds the limit
                        if len(cleaned_output) > 250:
                            cleaned_output = "..." + cleaned_output[-247:]  # Keep the last 247 characters
                            cleaned_output = cleaned_output[:250] + "..."  # Keep the first 250 characters

                        cleaned_outputs.append(cleaned_output)

                    print("Phrase cleaning complete.")

                    article['phrase-output'] = cleaned_outputs
                    print("-----------------------------------")
                    # Print the new phrases and their corresponding outputs in an easy-to-read format
                    print("Cleaned outputs with corresponding phrases:")
                    for phrase, output in zip(found_phrases, cleaned_outputs):
                        print(f"{phrase}: {output} (Character Count: {len(output)})")
                        print("-----------------------------------")
                    print("End of phrase outputs. Moving to sentiment analysis...\n")
                # Skip the phrase extraction and cleaning if no phrases are found but still add the articles
                else:
                    print("Article does not possess a phrase. Skipping phrase extraction and cleaning...")
                    print("Continuing to sentiment analysis...\n")
                    with open("duplicate_urls.txt", "a") as f:
                        f.write(url + "\n")
                    article['found-phrases'] = "No phrases found"
                    article['phrase-output'] = "No phrase output found"
                    
                # Sentiment analysis section -------------------------
                # Sentiment analysis of title
                title_sentiment = TextBlob(title).sentiment.polarity
                print("Title: ", title)
                #Less than -0.1 is negative, greater than 0.1 is positive, between -0.1 and 0.1 is informational/neutral.
                if title_sentiment < -0.1:
                    print("Negative title found!")
                    print("Sentiment polarity: ", title_sentiment)
                    # Print the article title 
                    print(title)
                    article['title-sentiment'] = 'negative'
                elif -0.1 <= title_sentiment <= 0.1:
                    print("Neutral/Informational title found!")
                    print("Sentiment polarity: ", title_sentiment)
                    # Print the article title 
                    print(title)
                    article['title-sentiment'] = 'neutral'
                else:
                    print("Positive title found!")
                    print("Sentiment polarity: ", title_sentiment)
                    # Print the article title 
                    print(title)
                    article['title-sentiment'] = 'positive'
                article['title-polarity-score'] = title_sentiment # Add the polarity score to the article dictionary for that article

                # Sentiment analysis of text
                article_text = soup.get_text()
                article_sentiment = TextBlob(article_text).sentiment.polarity

                if article_sentiment < -0.1:
                    print("Negative article text found!")
                    print("Sentiment polarity: ", article_sentiment)
                    article['article-sentiment'] = 'negative'
                elif -0.1 <= article_sentiment <= 0.1:
                    print("Neutral/Informational article text found!")
                    print("Sentiment polarity: ", article_sentiment)
                    article['article-sentiment'] = 'neutral'
                else:
                    print("Positive article text found!")
                    print("Sentiment polarity: ", article_sentiment)
                    article['article-sentiment'] = 'positive'
                article['article-polarity-score'] = article_sentiment
                
                
                # Prints what is appended to the articles list
                articles.append(article)
                # Print the article appended to articles
                print("The following article was appended to articles:")
                # Iterate every article, and all of the dictionary values in an easy-to-read format
                counter = 0
                for article in articles:
                    counter += 1
                    print("Article number: ", counter)
                    print("Title: ", article['title'])
                    print("Date: ", article['date'])
                    print("URL: ", article['url'])
                    print("Found phrases: ", article['found-phrases'])
                    #print("Phrase output: ", article['phrase-output'])
                    print("Title sentiment: ", article['title-sentiment'])
                    print("Title polarity score: ", article['title-polarity-score'])
                    print("Article sentiment: ", article['article-sentiment'])
                    print("Article polarity score: ", article['article-polarity-score'])
                    print("-----------------------------------")
                print("End of articles list. Moving to all_articles list...\n")
                print("###################################")
                
                all_articles.append(dict(article))                    
                print("The following is all of the current articles in all_articles:")
                # Iterate every article, and all of the dictionary values in an easy-to-read format
                counter = 0
                for article in all_articles:
                    counter += 1
                    print("Article number: ", counter)
                    print("Title: ", article['title'])
                    print("Date: ", article['date'])
                    print("URL: ", article['url'])
                    print("Found phrases: ", article['found-phrases'])
                    #print("Phrase output: ", article['phrase-output'])
                    print("Title sentiment: ", article['title-sentiment'])
                    print("Title polarity score: ", article['title-polarity-score'])
                    print("Article sentiment: ", article['article-sentiment'])
                    print("Article polarity score: ", article['article-polarity-score'])
                    print("-----------------------------------")
                print("End of all_articles list. Moving to duplicate_urls.txt...\n")
                print("###################################")
                
                # Check if the article is already in the duplicate_urls.txt file. If it is, skip it. If not, add it to the file
                if url in existing_urls:
                    print(url + " already exists in duplicate_urls.txt. Skipping...")
                else:
                    print("Adding URL to duplicate_urls.txt...")
                    with open("duplicate_urls.txt", "a") as f:
                        f.write(url + "\n")
            except requests.exceptions.Timeout:
                print("Request timed out. Possible anti-bot detection. Skipping")
                # Write the article URL to the duplicate_urls.txt file
                with open("duplicate_urls.txt", "a") as f:
                    f.write(url + "\n")
            except:
                print("Error occurred. Skipping...")
                # Write the article URL to the duplicate_urls.txt file
                with open("duplicate_urls.txt", "a") as f:
                    f.write(url + "\n")
                # Print the error message
                print("Error: ", sys.exc_info()[0])
                # Print the full traceback
                print(traceback.format_exc())
                print(" ")        
            # Sleep for 10 seconds to prevent Google from blocking the request
            print("Sleeping for 10 seconds...")
            print("")
            time.sleep(10)    
            
            
        if len(articles) == 0:
            print(f"No new articles found for {query}")
        else:
            print(f"Articles for {query}:")
            for article in articles:
                print("Article title: " + article['title'])
                print("Title sentiment: " + article['title-sentiment'])
                print("Title sentiment score: " + str(article['title-polarity-score']))
                print("URL: " + article['url'])
                print("Article date: " + article['date'])
                print("Article sentiment: " + article['article-sentiment'])
                print("Article sentiment score: " + str(article['article-polarity-score']))
                
                
                # Print the found phrases and their corresponding outputs
                found_phrases = article['found-phrases']
                phrase_outputs = article['phrase-output']
                for i in range(len(found_phrases)):
                    print("Found phrase:", found_phrases[i])
                    print("Phrase output:", phrase_outputs[i])
                
                print("----------------------------------------")
                articles = [] # Reset the articles list
                
        elapsed_time = time.time() - start_time
        print(f"Query finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Elapsed time: {elapsed_time:.2f} seconds.")
        print("----------------------------------------")
        print("Sleeping for 10 seconds...")
        time.sleep(10)
        
        # Specify the output file
        output_file = "articles.txt"
        counter = 0

        # Check if the output file exists
        if os.path.isfile(output_file):
            mode = "w"  # Change to a if you want to append to the file instead of overwriting it
        else:
            mode = "w"  # Write mode if the file doesn't exist

        # Open the file in the specified mode
        with open(output_file, mode) as file:
            # Write the header and current date and time
            file.write("All articles found:\n")
            file.write("Date: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")

            # Check if there are any articles
            if len(all_articles) == 0:
                file.write("No new articles found.\n")
            else:
                # Sort the articles by date
                sorted_articles = sorted(all_articles, key=lambda x: x['date'] if x['date'] != 'No date found' else '9999-99-99')           
                positive_articles = []
                negative_articles = []

                # Initialize a set to store the URLs of printed articles, used to remove duplicates
                printed_urls = set()

                for article in sorted_articles:
                    url = article['url']
                    if url not in printed_urls:  # Check if the article has already been printed
                        if article['article-sentiment'] == 'positive':
                            positive_articles.append(article)
                        elif article['article-sentiment'] == 'negative':
                            negative_articles.append(article)

                        printed_urls.add(url)  # Add the URL to the set of printed URLs

                # Sort positive articles by date
                positive_articles = sorted(positive_articles, key=lambda x: x['date'], reverse=True)
                # Sort negative articles by date
                negative_articles = sorted(negative_articles, key=lambda x: x['date'], reverse=True)
                if len(negative_articles) > 0:
                    file.write("----------------------------------------\n")
                    file.write("Negative Articles:\n")
                    file.write("----------------------------------------\n")
                    for article in negative_articles:
                        counter += 1
                        file.write("Article number: " + str(counter) + "\n")
                        file.write("Article title: " + article['title'] + "\n")
                        if article['date'] is None or article['date'] == '9999-99-99':       
                            file.write("Article date: No date found\n")
                        else:
                            file.write("Article date: " + article['date'] + "\n")
                        file.write("URL: " + article['url'] + "\n")
                        file.write("Title sentiment: " + article['title-sentiment'] + "\n")
                        file.write("Title sentiment score: " + str(article['title-polarity-score']) + "\n")
                        file.write("Article sentiment: " + article['article-sentiment'] + "\n")
                        file.write("Article sentiment score: " + str(article['article-polarity-score']) + "\n")

                        found_phrases = article['found-phrases']
                        phrase_outputs = article['phrase-output']

                        """
                        if found_phrases:
                            file.write("Found phrases and their corresponding outputs:\n")
                            for phrase, output in zip(found_phrases, phrase_outputs):
                                file.write("Found phrase: " + phrase + "\n")
                                file.write("Phrase output: " + output + "\n")
                                file.write("\n")  # Add a new line between each phrase and its output
                        """
                        file.write("----------------------------------------\n")
                        
                        # Add the url to the duplicate printed urls 
                        printed_urls.add(url)
                        
                        # Print article details
                        print("Article number:", counter)
                        print("Article title:", article['title'])
                        print("Article date:", article['date'])
                        print("URL:", article['url'])
                        print("Title sentiment:", article['title-sentiment'])
                        print("Title sentiment score:", article['title-polarity-score'])
                        print("Article sentiment:", article['article-sentiment'])
                        print("Article sentiment score:", article['article-polarity-score'])
                        
                        """
                        if found_phrases:
                            print("Found phrases and their corresponding outputs:")
                            for phrase, output in zip(found_phrases, phrase_outputs):
                                print("Found phrase:", phrase)
                                print("Phrase output:", output)
                                print()
                        """

                if len(positive_articles) > 0:
                    file.write("Positive Articles:\n")
                    file.write("----------------------------------------\n")
                    for article in positive_articles:
                        counter += 1
                        file.write("Article number: " + str(counter) + "\n")
                        file.write("Article title: " + article['title'] + "\n")
                        if article['date'] is None or article['date'] == '9999-99-99':       
                            file.write("Article date: No date found\n")
                        else:
                            file.write("Article date: " + article['date'] + "\n")
                        file.write("URL: " + article['url'] + "\n")
                        file.write("Title sentiment: " + article['title-sentiment'] + "\n")
                        file.write("Title sentiment score: " + str(article['title-polarity-score']) + "\n")
                        file.write("Article sentiment: " + article['article-sentiment'] + "\n")
                        file.write("Article sentiment score: " + str(article['article-polarity-score']) + "\n")

                        found_phrases = article['found-phrases']
                        phrase_outputs = article['phrase-output']

                        """
                        if found_phrases:
                            file.write("Found phrases and their corresponding outputs:\n")
                            for phrase, output in zip(found_phrases, phrase_outputs):
                                file.write("Found phrase: " + phrase + "\n")
                                file.write("Phrase output: " + output + "\n")
                                file.write("\n")  # Add a new line between each phrase and its output
                        """
                        file.write("----------------------------------------\n")
                        
                        # Print article details
                        print("Article number:", counter)
                        print("Article title:", article['title'])
                        print("Article date:", article['date'])
                        print("URL:", article['url'])
                        print("Title sentiment:", article['title-sentiment'])
                        print("Title sentiment score:", article['title-polarity-score'])
                        print("Article sentiment:", article['article-sentiment'])
                        print("Article sentiment score:", article['article-polarity-score'])
                        
                        """
                        if found_phrases:
                            print("Found phrases and their corresponding outputs:")
                            for phrase, output in zip(found_phrases, phrase_outputs):
                                print("Found phrase:", phrase)
                                print("Phrase output:", output)
                                print("")
                        """
                        printed_urls.add(url)  # Add the URL to the set of printed URLs

        print("Finished searching for articles.\n")

        print("Output has been written to the file:", output_file)
        
def send_email():
    # Send results via email
    sender_email = ''
    sender_password = ''
    recipient_email = ''
    file_name = 'articles.txt'
    file_path = os.path.join(os.getcwd(), file_name)

    # Set up the email server
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587  # Port for outlook

    # Create a multipart message object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'SFS-Threat-Intelligence Report - ' + datetime.now().strftime("%m/%d/%Y")

    # Read the contents of articles.txt and set it as the email body
    with open(file_path, 'r') as file:
        body = file.read()

    # Attach articles.txt to the email
    with open(file_path, 'rb') as file:
        attachment = MIMEApplication(file.read(), Name=file_name)
    attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
    message.attach(attachment)

    # Set the email body
    message.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the email server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())

        print("Email sent successfully.")
        return True

    except Exception as e:
        print("An error occurred while sending the email:", str(e))
        return False
    
def get_weather():
    


# Measure the performance of the script
start_time = time.time()
print(" The current time is: ", datetime.now().strftime("%H:%M:%S"))

# List of queries to search for in google API

queries = ['Scottsdale Fashion Square', 'Scottsdale Fashion Square Mall', 'Scottsdale Fashion Square officer-involved shooting', 'Scottsdale Fashion Square scam', 
'Scottsdale Fashion Square crime', 'Scottsdale Fashion Square arrest', 'Scottsdale Fashion Square incident', 'Scottsdale Fashion Square accident',
'Scottsdale Fashion Square protest', 'Scottsdale Fashion Square riot', 'Scottsdale Fashion Square bomb threat', 'Scottsdale Fashion Square shooting', 
'Scottsdale Fashion Square arrest']

get_news_articles(queries)

end_time = time.time()
total_time = end_time - start_time

# Convert the total time to hours, minutes, and seconds
hours = int(total_time // 3600)
minutes = int((total_time % 3600) // 60)
seconds = total_time % 60
print(f"Total time: {hours} hours, {minutes} minutes, {seconds:.2f} seconds")

max_attempts = 3  # Maximum number of attempts to send the email
attempts = 0  # Number of attempts to send the email

while attempts < max_attempts:
    if send_email():
        print("Email sent successfully.")
        break
    else:
        attempts += 1
        print("Failed to send email. Attempt", attempts, "of", max_attempts)
        
    if attempts == max_attempts:
        print("Failed to send email after", attempts, "attempts.")

print("Finished...")
