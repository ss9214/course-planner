import requests 
from bs4 import BeautifulSoup 
from mongoclient import db,coursesdb
courses = {}
course_offerings = {}
def update_classes(soup):
    main = soup.find('div', attrs={'id':'block-system-main'})
    curr = main.find('h2')
    curr = curr.find_next('h2')
    course_names = list(map(lambda x: x.text.strip(), main.find_all('a')))
    for course in course_names:
        courses[course] = {}
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
                        temp = text.split('Prerequisites:')
                        if len(temp) > 1:
                            prereqs = temp[1]
                        else: prereqs = None
                    courses[curr_course]['Description'] = desc
                    courses[curr_course]['Prerequisites'] = prereqs
        curr = curr.find_next()
    del_keys = []
    for key in courses:
        course_name = key.split(":")[0]
        course_number = 0
        try: # is the last digit a number 
            course_number = int(course_name[len(course_name) - 3:len(course_name)])
        except ValueError:
            try:
                course_number = int(course_name[len(course_name) - 4:len(course_name) - 1])
            except ValueError:
                course_number = int(course_name[len(course_name) - 5:len(course_name) - 2])
        if course_name not in course_offerings.keys():
            del_keys.append(key)
        elif course_number >=600:
            del_keys.append(key)
        else:
            courses[key]['Credits'] = course_offerings[course_name]['Credits']
            courses[key]['Semesters Offered'] = course_offerings[course_name]['Semesters Offered']
    for key in del_keys:
        del courses[key]
def find_course_offerings(soup):
    main = soup.find('div', attrs={'id':'block-system-main'})
    rows = main.find_all('tr')
    for row in rows:
        course = row.find_all('td')
        if len(course) == 5:
            course_offerings[course[0].text.strip() + " " + course[1].text.strip()] = {"Credits":course[3].text.strip(), "Semesters Offered":course[4].text.strip()}

if __name__ == "__main__":
    soups = []
    soups.append(BeautifulSoup(requests.get("https://www.cics.umass.edu/content/Fall-24-course-descriptions").content, 'html.parser'))
    soups.append(BeautifulSoup(requests.get("https://www.cics.umass.edu/content/Spring-24-course-descriptions").content, 'html.parser'))
    soups.append(BeautifulSoup(requests.get("https://www.cics.umass.edu/content/Fall-23-course-descriptions").content, 'html.parser'))
    soups.append(BeautifulSoup(requests.get("https://www.cics.umass.edu/content/Spring-23-course-descriptions").content, 'html.parser'))
    soups.append(BeautifulSoup(requests.get("https://www.cics.umass.edu/content/Fall-22-course-descriptions").content, 'html.parser'))
    soups.append(BeautifulSoup(requests.get("https://www.cics.umass.edu/content/Spring-22-course-descriptions").content, 'html.parser'))
    soup_offerings = BeautifulSoup(requests.get("https://www.cics.umass.edu/content/course-offering-plan").content, 'html.parser')
    find_course_offerings(soup_offerings)
    for soup in soups:
        update_classes(soup)
    courses = dict(sorted(courses.items()))
    for course_name,dict in courses.items():
        dict["Course Name"] = course_name
        if type(dict["Description"]) == list:
            dict["Description"] = dict["Description"][0]
        if coursesdb.find_one_and_update({"Course Name": course_name},{"$set": dict}) == None:
            coursesdb.insert_one(dict)
    math_classes = [
        {
            "Course Name":"STAT 315: Introduction to Statistics I",
            "Prerequisites":"Two semesters of single variable calculus (Math 131-132) or the equivalent, with a grade of 'C' or better in Math 132. Math 233 is recommended for this course.",
            "Description":"This course provides a calculus-based introduction to probability (an emphasis on probabilistic concepts used in statistical modeling) and the beginning of statistical inference (continued in Stat516). Coverage includes basic axioms of probability, sample spaces, counting rules, conditional probability, independence, random variables (and various associated discrete and continuous distributions), expectation, variance, covariance and correlation, probability inequalities, the central limit theorem, the Poisson approximation, and sampling distributions. Introduction to basic concepts of estimation (bias, standard error, etc.) and confidence intervals.",
            "Semesters Offered": "Fall and Spring",
            "Credits": "4"
        },
        {
            "Course Name":"MATH 131: Calculus I",
            "Prerequisites":"",
            "Description":"Continuity, limits, and the derivative for algebraic, trigonometric, logarithmic, exponential, and inverse functions. Applications to physics, chemistry, and engineering.",
            "Semesters Offered": "Fall and Spring",
            "Credits": "4"
        },
        {
            "Course Name":"MATH 131H: Honors Calculus I",
            "Prerequisites":"",
            "Description":"Honors section of Math 131",
            "Semesters Offered": "Fall and Spring",
            "Credits": "4"
        },
        {
            "Course Name":"MATH 132: Calculus II",
            "Prerequisites":"Math 131 or equivalent.",
            "Description":"The definite integral, techniques of integration, and applications to physics, chemistry, and engineering. Sequences, series, and power series. Taylor and MacLaurin series. Students expected to have and use a Texas Instruments 86 graphics, programmable calculator.",
            "Semesters Offered": "Fall and Spring",
            "Credits": "4"
        },
        {
            "Course Name":"MATH 132H: Honors Calculus II",
            "Prerequisites":"Math 131 or equivalent.",
            "Description":"Honors section of Math 132.",
            "Semesters Offered": "Fall and Spring",
            "Credits": "4"
        },
        {
            "Course Name":"MATH 233: Multivariate Calculus",
            "Prerequisites":"Math 132.",
            "Description":"Techniques of calculus in two and three dimensions. Vectors, partial derivatives, multiple integrals, line integrals. Theorems of Green, Stokes and Gauss. Honors section available. (Gen.Ed. R2)",
            "Semesters Offered": "Fall and Spring",
            "Credits": "4"
        },
        {
            "Course Name":"MATH 233H: Honors Multivariate Calculus",
            "Prerequisites":"Math 132.",
            "Description":"Honors section of Math 233.",
            "Semesters Offered": "Fall and Spring",
            "Credits": "4"
        },
        {
            "Course Name":"MATH 235: Introduction to Linear Algebra",
            "Prerequisites":"Math 132 or consent of the instructor.",
            "Description":"Basic concepts of linear algebra. Matrices, determinants, systems of linear equations, vector spaces, linear transformations, and eigenvalues.",
            "Semesters Offered": "Fall and Spring",
            "Credits": "4"
        },
        {
            "Course Name":"MATH 235H: Honors Introduction to Linear Algebra",
            "Prerequisites":"Math 132 or consent of the instructor.",
            "Description":"Honors section of Math 235.",
            "Semesters Offered": "Fall and Spring",
            "Credits": "4"
        }
    ]
    for course in math_classes:
        if coursesdb.find_one_and_update({"Course Name": course["Course Name"]},{"$set": dict}) == None:
            coursesdb.insert_one(course)

