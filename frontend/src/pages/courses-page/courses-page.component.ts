import { Component, OnInit } from '@angular/core';
import {MatCardModule} from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import {MatFormFieldModule, MatFormField} from '@angular/material/form-field';
import { FormControl, ReactiveFormsModule, FormGroup } from '@angular/forms';
import { RouterLink } from '@angular/router';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { CommonModule } from '@angular/common';
import {MatInputModule} from '@angular/material/input';
import {MatIconModule} from '@angular/material/icon';
import { DataService } from '../../data.service';
import { SharedService } from '../../shared.service';
@Component({
    selector: 'app-course-page',
    standalone: true,
    imports: [MatIconModule, MatInputModule, CommonModule,MatCardModule,MatButtonModule,MatFormFieldModule, MatFormField,RouterLink,ReactiveFormsModule,MatCheckboxModule],
    templateUrl: './courses-page.component.html',
    styleUrl: './courses-page.component.css'
  })

  export class CoursePageComponent implements OnInit {
    createFilterForm = new FormGroup({
      course_number: new FormControl(''),
      professor: new FormControl(''),
      info: new FormControl(''),
      cics: new FormControl(''),
      compsci: new FormControl(''),
      one_hundred:new FormControl(''),
      two_hundred:new FormControl(''),
      three_hundred:new FormControl(''),
      four_hundred:new FormControl(''),
      five_hundred:new FormControl(''),
      fall:new FormControl(''),
      spring:new FormControl(''),
      summer:new FormControl(''),
      winter:new FormControl(''),
      data:new FormControl(''),
      ai_ml:new FormControl(''),
      cybersec:new FormControl(''),
      swe:new FormControl('')
    })

    courses:any[]=[];
    visibleCourses:any[]=[];
    satisfiedCourses:string = "";
    constructor(private dataService: DataService, private shared: SharedService) {}
    curr_course:string ="";
    ngOnInit() {
      const obs = this.dataService.fetchCourseData()
      obs.subscribe(data => {
        this.courses = data.Data;
        this.visibleCourses = this.courses;
      });
    }

    changeSchedule(course:string,change:string) {
      this.shared.satisfiedCourses.subscribe(courses => this.satisfiedCourses = courses);
      if (change=='add') {
        this.satisfiedCourses = this.satisfiedCourses + course + ", ";
      } else if (change== 'remove') {
        this.satisfiedCourses = this.satisfiedCourses.replace(course + ", ", "")
      }
      
      this.shared.changeSatisfiedCourses(this.satisfiedCourses);
    }

    onFilter() {
      const formValues = this.createFilterForm.value;
      this.visibleCourses = this.courses;
      if (formValues.course_number != null && formValues.course_number != '' && formValues.course_number != undefined) {
        let num_entry = +formValues.course_number;
        this.visibleCourses = this.visibleCourses.filter(course => {
          let course_number = course["Course Name"].substring(course["Course Name"].indexOf(" "),course["Course Name"].indexOf(":"))
          if (course_number.length == 5){
            course_number = course_number.substring(0,4);
          }
          return +course_number == num_entry;
        })
      
      } else { 
        this.visibleCourses = this.courses

        // filter by professor
        if (formValues.professor != null && formValues.professor != '' && formValues.professor != undefined){
          let professor = formValues.professor;
          this.visibleCourses = this.visibleCourses.filter(course => {
            let professors = course["Instructors"].substring(course["Instructors"].indexOf(":") + 1)
            return professors.includes(professor);
          })
        }

        //filter by subject
        if (formValues.cics || formValues.compsci || formValues.info) {
          this.visibleCourses = this.visibleCourses.filter(course => {
            let subject = course["Course Name"].substring(0,course["Course Name"].indexOf(" "));
            if (formValues.cics && subject == "CICS"){
              return true;
            } else if (formValues.compsci && subject == "COMPSCI"){
              return true;
            } else if (formValues.info && subject == "INFO"){
              return true;
            }
            return false
          })
        }

        // filter by course level (non exclusive since a class can't be both 100-199 and 200-299)
        if (formValues.one_hundred || formValues.two_hundred || formValues.three_hundred || formValues.four_hundred || formValues.five_hundred) {
          this.visibleCourses = this.visibleCourses.filter(course => {
            let course_number = course["Course Name"].substring(course["Course Name"].indexOf(" "),course["Course Name"].indexOf(":"))
            if (course_number.length == 5){
              course_number = +course_number.substring(0,4);
            } else {
              course_number = +course_number;
            }
            if (formValues.one_hundred && (course_number >= 100) && (course_number < 200)){return true;}
            if (formValues.two_hundred && (course_number >= 200) && (course_number < 300)){return true;}
            if (formValues.three_hundred && (course_number >= 300) && (course_number < 400)){return true;}
            if (formValues.four_hundred && (course_number >= 400) && (course_number < 500)){return true;}
            if (formValues.five_hundred && (course_number >= 500)){return true;}
            return false;
          })
        }

        //filter by semester
        if (formValues.fall || formValues.spring) {
          this.visibleCourses = this.visibleCourses.filter(course => {
            let semesters: any[] = course["Semesters Offered"];
            for (const semester of semesters) {
              if (formValues.fall && semester.includes('Fall')) {
                return true;
              }
              if (formValues.spring && semester.includes('Spring')) {
                return true;
              }
            }
            return false;
          })
        }
      }
    }
  }