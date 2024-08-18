from flask import Flask, jsonify, request
from flask_cors import CORS
from .mongoclient import coursesdb,prereqsdb
import math
import random
# Allow Cross-Origin Resource Sharing to prevent CORS errors when making requests from the front end
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/get/courses")
def send_courses():
    courses = []
    courses_cursor = coursesdb.find({})
    for c in courses_cursor:
        del c["_id"]
        courses.append(c)
    return jsonify(
        {
            "Success": True,
            "Data": courses
        }
    )

@app.route("/api/post/schedule",methods=['POST'])
def get_schedule():
    schedule = request.get_json()  # Call get_json as a method
    created_schedule = create_schedule_algorithm(schedule)
    return jsonify({'Success': True, 'data': created_schedule})

    

def create_schedule_algorithm(details):
    semesters = int(details["semesters_left"])
    credit_total = int(details["total_credits"])
    schedule = {}
    if details["major"]=="computer science":
        major_requirements=['MATH131', 'MATH132', 'MATH233 or STAT315', 'MATH235',
                            'CICS110', 'CICS160', 'CICS210', 'COMPSCI198C',
                            'COMPSCI220', 'COMPSCI230', 'COMPSCI240', 'COMPSCI250',
                            'COMPSCI311', 'COMPSCI320 or COMPSCI326',
                            'Any 300', 'Any 300', 'Any 300',
                            'Any 400', 'Any 400', 'Any 400', 'Biological Science',
                            'Physical Science', 'Physical Science', 'Gen-ed', 'Gen-ed', 'Gen-ed', 'Gen-ed']
    else:
        major_requirements=[]

    '''
    Remove gen-eds
    '''
    gen_eds_finished = int(details['gen_eds_finished'])
    if gen_eds_finished>0:
        for i in range(gen_eds_finished):
            major_requirements.remove('Gen-ed')
    '''
    Remove Physical Science
    '''
    ps_finished = int(details['physical_sciences_finished'])
    if ps_finished>0:
        for i in range(ps_finished):
            major_requirements.remove('Physical Science')
    '''
    Remove BS
    '''
    if details['biological_science_finished'] == 'yes':
        major_requirements.remove("Biological Science")
    prereqs_graph = {}
    courses_dict = {}
    for course in coursesdb.find({}): # create accessible course database in O(N) time
        name = course["Course Name"][0:course["Course Name"].find(":")].replace(" ","")
        del course["Course Name"]
        del course["_id"]
        courses_dict[name] = course

    for course in prereqsdb.find({}): # construct a dictionary with prereqs of each class in O(N) time
        course_name = course["Course Name"][0:course["Course Name"].find(":")].replace(" ","")
        try: # is the last digit a number 
            course_number = int(course_name[len(course_name) - 3:len(course_name)])
        except ValueError:
            try:
                course_number = int(course_name[len(course_name) - 4:len(course_name) - 1])
            except ValueError:
                course_number = int(course_name[len(course_name) - 5:len(course_name) - 2])
        if 'INFO' in course_name:
            pass        
        elif course_number <600:
            prereqs = course["Prerequisites"][15:]
            satisfied = course_name in details["satisfied_courses"].replace(" ","")
            prereqs_graph[course_name] = {"Prerequisites":prereqs,"Satisfied":satisfied}
    
        '''We can use satisfied to check if the course has been taken.
        Prerequisites is to determine how many prerequisites are left. 
        We can replace each course in the prerequisite boolean expression with the value of if it has been satisfied
        After using eval(), if the expression returns true, we can set the prereqs field to True,
        and then that class can be taken.'''
    
    for i in range(semesters): # worst case O(10)
        # create course schedule for i semesters
        valid_courses = []
        credits_left = (120-credit_total)
        min_sem_credits = max(int(math.ceil(credits_left/(semesters-i))),int(details["min_credits"]))
        max_sem_credits = int(details["max_credits"])
        if min_sem_credits > max_sem_credits:
            return "No schedules possible in allotted time with constraints. Try increasing the maximum credit threshold or semesters left."
        cur_sem_credits = 0
        for course_name,values in prereqs_graph.items(): # iterate through all in O(N) * O(10) => O(10N)
            if values["Prerequisites"] == "True" and not values["Satisfied"]: # course is valid
                valid_courses.append(course_name)
        # valid_courses now contains all valid courses for this semester

        schedule[f"Semester {i+1}"] = [] # create course list for this semester
        random.shuffle(valid_courses) # return a unique set of courses
        course_idx = 0
        # first put any major requirements that are satisfied
        remove_from_valid_courses = []
        for name in valid_courses:
            if name[len(name)-1] == 'H' and details['honors'] == 'no':
                remove_from_valid_courses.append(name)
            
        for name in valid_courses:
            if (name in major_requirements or
                ((name in ['COMPSCI320','COMPSCI326'] and 'COMPSCI320 or COMPSCI326' in major_requirements) or 
                 name in ['MATH233','STAT315'] and 'MATH233 or STAT315' in major_requirements)) and cur_sem_credits < min_sem_credits:
                course_credits = int(courses_dict[name]['Credits'])
                courses_dict[name]['Course Name'] = name
                schedule[f"Semester {i+1}"].append(courses_dict[name])
                cur_sem_credits+=course_credits
                if name in ['COMPSCI320','COMPSCI326']:
                    major_requirements.remove('COMPSCI320 or COMPSCI326')
                elif name in ['MATH233','STAT315']:
                    major_requirements.remove('MATH233 or STAT315')
                else:
                    major_requirements.remove(name)
                remove_from_valid_courses.append(name)
                '''
                set course to satisfied
                '''
                
                prereqs_graph[name]["Satisfied"] = True

        for name in remove_from_valid_courses:
            valid_courses.remove(name)
        # courses that are not major requirements
        while cur_sem_credits < min_sem_credits:
            if "Physical Science" in major_requirements and {"Course Name": "Physical Science", "Credits": "4"} not in schedule[f"Semester {i+1}"]:
                schedule[f"Semester {i+1}"].append({"Course Name": "Physical Science", "Credits": "4"})
                major_requirements.remove("Physical Science")
                cur_sem_credits+=4
            elif "Biological Science" in major_requirements:
                schedule[f"Semester {i+1}"].append({"Course Name": "Biological Science", "Credits": "4"})
                major_requirements.remove("Biological Science")
                cur_sem_credits+=4
            elif "Gen-ed" in major_requirements:
                schedule[f"Semester {i+1}"].append({"Course Name": "Gen-ed", "Credits": "4"})
                major_requirements.remove("Gen-ed")
                cur_sem_credits+=4
            if cur_sem_credits < max_sem_credits and (not course_idx == len(valid_courses)): 
                # prioritize any gen-eds left for next 3 sems before any other classes
                course_name = valid_courses[course_idx]

                '''
                Get Course Number
                '''
                try: # is the last digit a number 
                    course_number = int(course_name[len(course_name) - 3:len(course_name)])
                except ValueError:
                    try:
                        course_number = int(course_name[len(course_name) - 4:len(course_name) - 1])
                    except ValueError:
                        course_number = int(course_name[len(course_name) - 5:len(course_name) - 2])
                '''
                Check if class is valid, if it is then add to semester course list
                '''
                if ((credit_total < 57 or details["grad_classes"]=="no") and course_number >=500) or (credit_total >= 90 and course_number < 300) or (credit_total >= 57 and course_number < 200) or (i < 3 and ("Gen-ed" in major_requirements or "Biological Science" in major_requirements or "Physical Science" in major_requirements)): 
                    # not junior status and its a grad class == big no no 
                    # if opted out grad classes
                    # or if junior status and random freshman classes
                    # or senior and random sophomore classes
                    course_idx+=1 # skip this class, don't add it
                
                else: #valid class, sophomores can technically take junior classes if there's spots, just has to override
                    course_credits = int(courses_dict[course_name]['Credits'])
                    courses_dict[course_name]['Course Name'] = course_name
                    schedule[f"Semester {i+1}"].append(courses_dict[course_name])
                    cur_sem_credits+=course_credits
                    if course_number >=400 and 'Any 400' in major_requirements:
                        major_requirements.remove('Any 400')
                    elif course_number >=300 and 'Any 300' in major_requirements:
                        major_requirements.remove('Any 300')
                    valid_courses.remove(course_name)
                    # size of courses decreased so idx stays the same

                    '''
                    Set this course to satisfied
                    '''
                    prereqs_graph[course_name.replace(" ","")]["Satisfied"] = True

        '''
        Semester is over, update prereqs of every class
        '''
        
        credit_total+=cur_sem_credits
        for course,values in prereqs_graph.items():
            expression = values['Prerequisites']
            if not values["Satisfied"]:
                courses = expression.split()
                for course_name in courses:
                    if course_name[0] == "(":
                        course_name = course_name[1:]
                    if course_name[len(course_name)-1] == ')':
                        course_name = course_name[0:len(course_name)-1]
                    if course_name != 'and' and course_name != 'or':
                        try:
                            temp = prereqs_graph[course_name]['Satisfied']
                        except KeyError:
                            temp = False
                        expression = expression.replace(course_name, f"{temp}")
                    # run through every course, replace it with its satisfied boolean value
            try:
                if f"{eval(expression)}" == "True":
                    prereqs_graph[course]["Prerequisites"] = "True"
            except:
                pass
                    
    return schedule
            
@app.route("/api/post/verify-schedule",methods=['POST'])
def verify_schedule():
    schedule = request.get_json()
    prereqs_graph = {}
    courses_dict = {}
    course_names = []
    for semester in schedule:
        for course in semester:
            course_names.append(course["Course Name"])
    for course in coursesdb.find({}): # create accessible course database in O(N) time
        name = course["Course Name"][0:course["Course Name"].find(":")].replace(" ","")
        del course["Course Name"]
        del course["_id"]
        courses_dict[name] = course
    for course in prereqsdb.find({}): # construct a dictionary with prereqs of each class in O(N) time
        course_name = course["Course Name"][0:course["Course Name"].find(":")].replace(" ","")

        prereqs = course["Prerequisites"][15:]
        prereqs_graph[course_name] = {"Prerequisites":prereqs,"Satisfied":False}
    
    for semester in schedule:
        for course in semester:
            prereqs_graph[course]["Course Name"]["Satisfied"]=True

if __name__ == "__main__":
    app.run(debug=True)