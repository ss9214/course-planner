import requests 
from bs4 import BeautifulSoup 

courses = {}
course_offerings = []
def update_classes(soup,sem):
    main = soup.find('div', attrs={'id':'block-system-main'})
    curr = main.find('h2')
    curr = curr.find_next('h2')
    course_names = list(map(lambda x: x.text.strip(), main.find_all('a')))
    for course in course_names:
        try:
            courses[course]['Semesters Offered'].append(sem)
        except KeyError:
            courses[course] = {'Semesters Offered': [sem]}
    while True:
        if curr.name == 'h2':
            if curr.a == None:
                break
            curr_course = curr.a.text.strip()
        else:
            if curr.name =='h3':
                try: 
                    courses[curr_course]['Instructors']
                except KeyError:
                    courses[curr_course]['Instructors'] = curr.text.strip()
            elif curr.name == 'p':
                try: 
                    courses[curr_course]['Description']
                except KeyError:
                    text = curr.text.strip()
                    desc = text.split("Prerequisite: ")
                    if len(desc) > 1:
                        prereqs = desc[1]
                        desc = desc[0]
                    else:
                        prereqs = None
                    courses[curr_course]['Description'] = desc
                    courses[curr_course]['Prerequisites'] = prereqs
        curr = curr.find_next()
    del_keys = []
    for key in courses:
        if key.split(":")[0] not in course_offerings:
            del_keys.append(key)
    for key in del_keys:
        del courses[key]
def find_course_offerings(soup):
    main = soup.find('div', attrs={'id':'block-system-main'})
    rows = main.find_all('tr')
    for row in rows:
        course = row.find_all('td')
        if len(course) == 5:
            course_offerings.append(course[0].text.strip() + " " + course[1].text.strip())
soups = []
soups.append((BeautifulSoup(requests.get("https://www.cics.umass.edu/content/Fall-24-course-descriptions").content, 'html.parser'),"Fall 2024"))
soups.append((BeautifulSoup(requests.get("https://www.cics.umass.edu/content/Spring-24-course-descriptions").content, 'html.parser'),"Spring 2024"))
soups.append((BeautifulSoup(requests.get("https://www.cics.umass.edu/content/Fall-23-course-descriptions").content, 'html.parser'),"Fall 2023"))
soups.append((BeautifulSoup(requests.get("https://www.cics.umass.edu/content/Spring-23-course-descriptions").content, 'html.parser'),"Spring 2023"))
soups.append((BeautifulSoup(requests.get("https://www.cics.umass.edu/content/Fall-22-course-descriptions").content, 'html.parser'),"Fall 2022"))
soups.append((BeautifulSoup(requests.get("https://www.cics.umass.edu/content/Spring-22-course-descriptions").content, 'html.parser'),"Spring 2022"))
soup_offerings = BeautifulSoup(requests.get("https://www.cics.umass.edu/content/course-offering-plan").content, 'html.parser')
find_course_offerings(soup_offerings)
for soup,sem in soups:
    update_classes(soup,sem)
courses = dict(sorted(courses.items()))

