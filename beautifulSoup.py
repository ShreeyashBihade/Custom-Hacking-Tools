import requests
from bs4 import BeautifulSoup

url = 'https://realpython.github.io/fake-jobs/' # A test website

resp = requests.get(url)
# print(resp.text) # Printing raw HTML of the page

s = BeautifulSoup(resp.content, 'html.parser') # Making an object 's' and passing the content of 'resp' and telling it to parse using it's built-in HTML parser

# Searching for Job Titles
results = s.find(id='ResultsContainer')
job_title = results.find_all('h2', class_='title is-5')

for job in job_title:
    print(job.text)
