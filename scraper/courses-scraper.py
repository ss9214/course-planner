import requests 
from bs4 import BeautifulSoup 
import csv 

courses = []

def update_classes(soup):
    main = soup.find('div', attrs={'id':'block-system-main'})
    course_names = list(map(lambda x: x.text, main.find_all('a')))
    instructors = list(map(lambda x: x.text, main.find_all('h3')))
    descriptions = list(map(lambda x: x.text, main.find_all('p')))
    print(course_names)
    print("\n")
    print(instructors)
    print("\n")
    print(descriptions)
    print("\n")
    print(len(course_names))
    print(len(instructors))
    print(len(descriptions))



r = requests.get("https://www.cics.umass.edu/content/Fall-23-course-descriptions")
soup = BeautifulSoup(r.content, 'html.parser')
update_classes(soup)