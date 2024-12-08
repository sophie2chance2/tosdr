import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import re
# load environment variables
from dotenv import load_dotenv
load_dotenv()

def get_services(num_pages=None):
    # page 1
    url = "https://api.tosdr.org/service/v2/?page=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['parameters']['services']) # load data into df
        page = data['parameters']['_page']['current'] + 1 # get the next page number
        print("Page 1 complete")
        last_page_available = data['parameters']['_page']['end'] # get the last page number so we can compare later
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")

    # loop through the pages
    if num_pages:
        last_page = min(num_pages, last_page_available)
        print(f"Retrieving {last_page} from {last_page_available} available pages")
    else:
        last_page = last_page_available

    while page <= last_page:
        url = f"https://api.tosdr.org/service/v2/?page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            df = pd.concat([df, pd.DataFrame(data['parameters']['services'])])
            print(f"Page {page} of {last_page} complete")
            page = data['parameters']['_page']['current'] + 1
            time.sleep(2) # prevent rate limiting

        else:
            print(f"Failed to retrieve data. Status Code: {response.status_code}")
            break

    df.reset_index(drop=True, inplace=True)

    return df

def pull_quoteText(discussion_url):
    highlight = None
    paraphrase = None
    # Make the request to the discussion URL
    response = requests.get(discussion_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # blockquote = soup.find('blockquote')
        blockquote = soup.find('div', class_='col-sm-10 col-sm-offset-1 p30 bgw')
        # paraphrase = soup.find('h4', class_='lighter fl')

        if blockquote is None:
            print(f"No blockquote found in {discussion_url}")
            return None #, None

        # Remove the footer element (section of the quote)
        if blockquote.find('footer'):
            blockquote.footer.decompose()
        
        # if paraphrase is None:
        #     print(f"No paraphrase found in {discussion_url}")
        #     return blockquote.get_text(strip=True), None

        # Extract the text from blockquote
        highlight = blockquote.get_text(strip=True)

        # clean any extra html or other tags
        highlight_clean = re.sub(r'<.*?>', '', highlight)
        # highlight_clean = highlight_clean.replace('\n', '')
        # paraphrase = paraphrase.get_text(strip=True)
    
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code} response: {response.text}")

    return highlight_clean #, paraphrase


def pull_highlight_labels(service):
    '''Pulls the highlighted sections and their labels
    Example: https://edit.tosdr.org/points/12831
    quoteText: Choose whether your name and photo appear next to your activity, like reviews and recommendations, that appear in ads
    Title: Your identity is used in ads that are shown to other users'''
    # Define the base API URL
    base_url = "https://tosdr.org/api/1/service/"

    # Example for Google (service: google)
    url = f"{base_url}{service}"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response as JSON
        data = response.json()
        if len(data['points']) < 1:
            print(f"No points available for {service}")
            # return None
        service = response.json()['name']
        service_class = response.json()['class']
        service_links = response.json()['links']

        service_df = pd.DataFrame(response.json()['pointsData']).T
        service_df = service_df.reset_index()

        for index, row in service_df.iterrows():
            discussion_url = row['discussion']
            if discussion_url == None or discussion_url == '':
                continue
            highlight = pull_quoteText(discussion_url)
            time.sleep(1) # prevent rate limiting

            service_df.loc[index, 'highlight'] = highlight
            # service_df.loc[index, 'paraphrase'] = paraphrase
            if row['quoteDoc'] not in service_links:
                continue
            service_df.loc[index, 'full_doc_link'] = service_links[row['quoteDoc']]['url']

        service_df['service'] = service
        service_df['service_class'] = service_class

    # if rate limited then wait 5 seconds and try again
    elif response.status_code == 429:
        print("Rate limited, waiting 30 seconds")
        time.sleep(60)
        pull_highlight_labels(service)

    else:
        print(f"Failed to retrieve data for {service}. Status Code: {response.status_code} response: {response.text}")

    return service_df

def find_doc_id_names(content):
    # Parse the HTML
    soup = BeautifulSoup(content, 'html.parser')

    # Try to find the unordered list with class "list-group"
    ul = soup.find('ul', class_='list-group')

    # Check if the 'ul' element was found
    if ul is None:
        print("Unordered list not found!")
        print("Here is the fetched HTML:", soup.prettify())  # This will help you inspect the HTML structure
        if "Oops! It looks like you're doing many different things in a short period of time." in soup.prettify():
            print("Rate limited")
            time.sleep(60)
            find_doc_id_names(content)
        else:
            return None
    else:
        # Initialize a dictionary to store the results
        labels_dict = {}

        # Loop through each list item in the unordered list
        for li in ul.find_all('li', class_='list-group-item'):
            # Get the anchor tag
            a_tag = li.find('a')

            # If the anchor tag exists, extract the text and href
            if a_tag:
                link_text = a_tag.text.strip()
                href = a_tag['href'].strip()
                labels_dict[link_text] = href

        # Output the result
        print(labels_dict)

        return labels_dict
    
def get_docs(content):
    soup = BeautifulSoup(content, 'html.parser')

    # find all of the div with class docAnchor output a dictionary with {id: text}
    docs_dict = {}
    # Find all div elements with class 'docAnchor'
    for div in soup.find_all('div', class_='docAnchor'):
        # Extract the id attribute
        doc_id = div.get('id')

        # Find the div with class 'panel-body' and extract the data-content attribute
        panel_body = div.find('div', class_='panel-body')
        if panel_body:
            doc_text = panel_body.get('data-content', '').strip()  # Default to an empty string if not found
            # remove the html tags
            doc_text = BeautifulSoup(doc_text, 'html.parser').get_text()
            doc_text_clean = re.sub(r'<.*?>', '', doc_text)

            # Add the id and cleaned text to the dictionary
            docs_dict[doc_id] = doc_text_clean

    return docs_dict
    
