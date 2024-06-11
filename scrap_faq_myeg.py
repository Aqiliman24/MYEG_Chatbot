import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL of the website
base_url = 'https://help.myeg.com.my'

# URL of the website's FAQ page
# faq_url = urljoin(base_url, '/portal/en/kb/myeg-services-berhad')

# Send a GET request to the FAQ URL
response = requests.get(base_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)
    # Find all the question links (adjust the selector as needed)
    question_links = soup.find_all('div', class_='ContentList__topicContent commonStyle__displayBlock')
    print(question_links)

    faqs = []
    for link in question_links:
        print(link)
        question = link.get_text(strip=True)
        answer_url = urljoin(base_url, link['href'])
        
        # Send a GET request to the answer URL
        answer_response = requests.get(answer_url)
        
        if answer_response.status_code == 200:
            # Parse the HTML content of the answer page
            answer_soup = BeautifulSoup(answer_response.content, 'html.parser')
            
            # Find the answer content (adjust the selector as needed)
            answer = answer_soup.find('div', class_='description KbDetailLtContainer__description').get_text(strip=True)
            
            faqs.append({'question': question, 'answer': answer})
        else:
            print(f"Failed to retrieve the answer page for question: {question}")
    
    # Print the FAQs
    for faq in faqs:
        print(f"Q: {faq['question']}")
        print(f"A: {faq['answer']}")
        print()
else:
    print(f"Failed to retrieve the FAQ page. Status code: {response.status_code}")

# error due to  URL is serving a web page that is part of the Zoho support system.
# URL Structure
# Dynamic Content
# Permissions and Authentication