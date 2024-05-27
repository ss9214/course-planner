from openai import OpenAI
from mongoclient import coursesdb,prereqsdb
import ast
from apikey import api_key

client = OpenAI(api_key=api_key)

courses = []
courses_cursor = coursesdb.find({})
for c in courses_cursor:
    del c["_id"]
    del c["Description"]
    try:
        del c["Instructors"]
    except KeyError:
        pass
    try:
        del c['Semesters Offered']
    except KeyError:
        pass
    courses.append(c)
cicscourses = list(filter(lambda x: "CICS" in x["Course Name"], courses))
cscourses = list(filter(lambda x: "COMPSCI" in x["Course Name"] or "MATH" in x["Course Name"], courses))
infocourses = list(filter(lambda x: "INFO" in x["Course Name"], courses))
templatecics=f'''
        You are a subject matter expert on the topic: "University of Massachusetts Amherst CICS Courses"

        Each course is formatted as a json like this:
        {{
            "Course Name": "Some course names
            "Prerequisites": "The prerequisite courses that must be completed before taking this course.
        }}  

        in this list of courses for a CICS major: {cicscourses}
        
        Your task is to simplify the "Prerequisites" field of each course to a boolean expression that can be interpreted. Use these examples as templates. 
        DO NOT include them in the response unless they are in the course list I provided!

        For example:
        The course 
        {{
            "Course Name: "CICS 110: Foundations of Programming"
            "Prerequisites": "Prerequisites: R1 (or a score of 15 or higher on the math placement test Part A), or one of the following courses: MATH 101&102 or MATH 104 or MATH 127 or MATH 128 or MATH 131 or MATH 132. 4 credits."
        }}
        must have its "prerequisites" field simplified to "Prerequisites: True", because any class that has R1 as it's requirement is alerady satisfied by everyone, so it can be listed as true, as the prerequisites are sastisfied.

        Another example:
        The course 
        {{
            "Course Name: "CICS 160: Object-Oriented Programming"
            "Prerequisites": "CICS 110 (previously INFO 190S) or COMPSCI 121 with a grade of C or above."
        }}
        must have its "prerequisites" field simplified to "Prerequisites: "CICS 110", since its previous name does not matter, and COMPSCI121 is not in the course list I gave you because it is no longer offered.

        Another example:
        The course 
        {{
            "Course Name: "COMPSCI 311: Introduction to Algorithms"
            "Prerequisites": "Prerequisites: COMPSCI 187 (or CICS 210) and either COMPSCI 250 or MATH 455, all with a grade of C or better.. 4 credits."
        }}
        must have its "prerequisites" field simplified to "Prerequisites: CICS210 and COMPSCI250", since COMPSCI 187 and MATH 455 are not in the course list.

        Last example:
        The course 
        {{
            "Course Name: "COMPSCI 325: Introduction to Human Computer Interaction"
            "Prerequisites": "Prerequisites: COMPSCI 187 (or CICS 210) with a grade of C or better OR INFO 248 and COMPSCI 186 (or 187 or CICS 160;INFO 190T) with a grade of C or better. 3 credits."
        }}
        must have its "prerequisites" field simplified to "Prerequisites: CICS210 or (INFO248 and CICS160)", since COMPSCI 187,COMPSCI 187, and INFO190T are not in the course list.

        You must respond as a list of jsons of all courses modified like the examples above.
        '''
templatecs=f'''
        You are a subject matter expert on the topic: "University of Massachusetts Amherst COMPSCI Courses"

        Each course is formatted as a json like this:
        {{
            "Course Name": "Some course names
            "Prerequisites": "The prerequisite courses that must be completed before taking this course.
        }}  

        in this list of courses for a computer science major: {cscourses}
        
        Your task is to simplify the "Prerequisites" field of each course to a boolean expression that can be interpreted.
        For example:
        The course 
        {{
            "Course Name: "CICS 110: Foundations of Programming"
            "Prerequisites": "Prerequisites: R1 (or a score of 15 or higher on the math placement test Part A), or one of the following courses: MATH 101&102 or MATH 104 or MATH 127 or MATH 128 or MATH 131 or MATH 132. 4 credits."
        }}
        must have its "prerequisites" field simplified to "Prerequisites: True", because any class that has R1 as it's requirement is alerady satisfied by everyone, so it can be listed as true, as the prerequisites are sastisfied.

        Another example:
        The course 
        {{
            "Course Name: "CICS 160: Object-Oriented Programming"
            "Prerequisites": "CICS 110 (previously INFO 190S) or COMPSCI 121 with a grade of C or above."
        }}
        must have its "prerequisites" field simplified to "Prerequisites: "CICS 110", since its previous name does not matter, and COMPSCI121 is not in the course list I gave you because it is no longer offered.

        Another example:
        The course 
        {{
            "Course Name: "COMPSCI 311: Introduction to Algorithms"
            "Prerequisites": "Prerequisites: COMPSCI 187 (or CICS 210) and either COMPSCI 250 or MATH 455, all with a grade of C or better.. 4 credits."
        }}
        must have its "prerequisites" field simplified to "Prerequisites: CICS210 and COMPSCI250", since COMPSCI 187 and MATH 455 are not in the course list.

        Last example:
        The course 
        {{
            "Course Name: "COMPSCI 325: Introduction to Human Computer Interaction"
            "Prerequisites": "Prerequisites: COMPSCI 187 (or CICS 210) with a grade of C or better OR INFO 248 and COMPSCI 186 (or 187 or CICS 160;INFO 190T) with a grade of C or better. 3 credits."
        }}
        must have its "prerequisites" field simplified to "Prerequisites: CICS210 or (INFO248 and CICS160)", since COMPSCI 187,COMPSCI 187, and INFO190T are not in the course list.

        You must respond as a list of jsons of all courses modified like the examples above.
        '''
templateinfo=f'''
        You are a subject matter expert on the topic: "University of Massachusetts Amherst INFO Courses"

        Each course is formatted as a json like this:
        {{
            "Course Name": "Some course names
            "Prerequisites": "The prerequisite courses that must be completed before taking this course.
        }}  

        in this list of courses for a informatics major: {infocourses}
        
        Your task is to simplify the "Prerequisites" field of each course to a boolean expression that can be interpreted.
        For example:
        The course 
        {{
            "Course Name: "CICS 110: Foundations of Programming"
            "Prerequisites": "Prerequisites: R1 (or a score of 15 or higher on the math placement test Part A), or one of the following courses: MATH 101&102 or MATH 104 or MATH 127 or MATH 128 or MATH 131 or MATH 132. 4 credits."
        }}
        must have its "prerequisites" field simplified to "Prerequisites: True", because any class that has R1 as it's requirement is alerady satisfied by everyone, so it can be listed as true, as the prerequisites are sastisfied.

        Another example:
        The course 
        {{
            "Course Name: "CICS 160: Object-Oriented Programming"
            "Prerequisites": "CICS 110 (previously INFO 190S) or COMPSCI 121 with a grade of C or above."
        }}
        must have its "prerequisites" field simplified to "Prerequisites: "CICS 110", since its previous name does not matter, and COMPSCI121 is not in the course list I gave you because it is no longer offered.

        Another example:
        The course 
        {{
            "Course Name: "COMPSCI 311: Introduction to Algorithms"
            "Prerequisites": "Prerequisites: COMPSCI 187 (or CICS 210) and either COMPSCI 250 or MATH 455, all with a grade of C or better.. 4 credits."
        }}
        must have its "prerequisites" field simplified to "Prerequisites: CICS210 and COMPSCI250", since COMPSCI 187 and MATH 455 are not in the course list.

        Last example:
        The course 
        {{
            "Course Name: "COMPSCI 325: Introduction to Human Computer Interaction"
            "Prerequisites": "Prerequisites: COMPSCI 187 (or CICS 210) with a grade of C or better OR INFO 248 and COMPSCI 186 (or 187 or CICS 160;INFO 190T) with a grade of C or better. 3 credits."
        }}
        must have its "prerequisites" field simplified to "Prerequisites: CICS210 or (INFO248 and CICS160)", since COMPSCI 187,COMPSCI 187, and INFO190T are not in the course list.

        You must respond as a list of jsons of all courses modified like the examples above.
        '''

responsecics = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=.7, # low variability
    messages=[{"role":"user", "content":templatecics}]
)
responseinfo = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=.7, # low variability
    messages=[{"role":"user", "content":templateinfo}]
)
responsecs = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=.7, # low variability
    messages=[{"role":"user", "content":templatecs}]
)

prereqs = [responsecics.choices[0].message.content,responsecs.choices[0].message.content,responseinfo.choices[0].message.content]

for msg in prereqs:
    msg = ast.literal_eval(msg)
    for course in msg:
        if prereqsdb.find_one_and_update({"Course Name": course["Course Name"]}, {"$set": course}) == None:
            prereqsdb.insert_one(course)
