import { Component, OnInit } from '@angular/core';
import {MatCardModule} from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import {MatFormFieldModule, MatFormField} from '@angular/material/form-field';
import { FormControl, ReactiveFormsModule, FormGroup, FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { CommonModule } from '@angular/common';
import {MatInputModule} from '@angular/material/input';
import {MatIconModule} from '@angular/material/icon';
import { DataService } from '../../data.service';
import {MatRadioModule} from '@angular/material/radio';
import {MatSliderModule} from '@angular/material/slider';
import { SharedService } from '../../shared.service';
import {MatSelectModule} from '@angular/material/select';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
@Component({
    selector: 'app-created-schedule-page',
    standalone: true,
    imports: [MatAutocompleteModule,FormsModule,MatSelectModule,MatSliderModule, MatRadioModule,MatIconModule, MatInputModule, CommonModule,MatCardModule,MatButtonModule,MatFormFieldModule, MatFormField,RouterLink,ReactiveFormsModule,MatCheckboxModule],
    templateUrl: './created-schedule-page.component.html',
    styleUrl: './created-schedule-page.component.css',
  })

  export class ViewSchedulePageComponent implements OnInit {
    schedule = {}
    list_schedule:any[] = []
    saved:boolean=false
    editSched:boolean=false
    courses:any[]=[]
    course_names:any[]=[]
    constructor(private dataService: DataService, private shared: SharedService) {}
    ngOnInit() {
      new Promise(resolve => setTimeout(resolve, 700)).then(()=>{
        this.shared.createdSchedule.subscribe(sched => {this.schedule = sched})
        Object.values(this.schedule).forEach(value=> {this.list_schedule.push(value)})
      })
      const obs = this.dataService.fetchCourseData()
      obs.subscribe(data => {
        this.courses = data.Data;
        this.course_names = this.courses.map(course=>(course["Course Name"].substring(0,course["Course Name"].indexOf(":"))))
        console.log(this.courses)
        console.log(this.course_names)
      });
    }
    addSaved(schedule:any){
      //this.shared.updateSavedSchedules(schedule,"add")
      this.dataService.sendSavedScheduleData({"Schedule Name": "Favorite Schedule", "Schedule": schedule}).subscribe(response=> {
        console.log('Schedule Saved', response);
      })
      this.saved=true
    }
    removeSaved(schedule:any){
      // this.shared.updateSavedSchedules(schedule,"remove")
      this.dataService.removeSavedScheduleData(schedule).subscribe(response=> {
        console.log('Schedule Removed', response)
      })
      this.saved=false
    }
    saveCourse(course_name:any,replaced_course:any){
      console.log(replaced_course)
      let sem:number= -1;
      let index:number= -1;
      for (const semester of this.list_schedule) {
        const idx = semester.indexOf(replaced_course)
        if (idx >=0) {
          sem = this.list_schedule.indexOf(semester);
          index=idx;
          break;
        }
      }
      if (sem>=0 && index>=0) {
        for (const course of this.courses){
          if (course["Course Name"].includes(course_name) || course["Course Name"].replaceAll(" ","").includes(course_name)) {
            course["Course Name"] = course_name;
            this.list_schedule[sem][index] = course;
          }
        }
      }
    }
    viewInfo(course:any) {
      this.shared.updateCourseInfo(course)
    }
  }