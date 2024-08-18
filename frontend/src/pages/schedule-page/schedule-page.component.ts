import { Component, OnInit } from '@angular/core';
import {MatCardModule} from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import {MatFormFieldModule, MatFormField} from '@angular/material/form-field';
import { FormControl, ReactiveFormsModule, FormGroup, FormArray } from '@angular/forms';
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

@Component({
    selector: 'app-schedule-page',
    standalone: true,
    imports: [MatSelectModule,MatSliderModule, MatRadioModule,MatIconModule, MatInputModule, CommonModule,MatCardModule,MatButtonModule,MatFormFieldModule, MatFormField,RouterLink,ReactiveFormsModule,MatCheckboxModule],
    templateUrl: './schedule-page.component.html',
    styleUrl: './schedule-page.component.css'
  })

  export class SchedulePageComponent implements OnInit {
    createScheduleForm = new FormGroup({
      honors: new FormControl(''),
      gen_eds_finished: new FormControl(''),
      physical_sciences_finished: new FormControl(''),
      biological_science_finished: new FormControl(''),
      total_credits: new FormControl(''),
      satisfied_courses: new FormControl(''),
      semesters_left: new FormControl(''),
      grad_classes: new FormControl(''),
      max_credits: new FormControl(''),
      min_credits: new FormControl(''),
      swe: new FormControl(''),
      datasci: new FormControl(''),
      cybersec: new FormControl(''),
      ai_ml: new FormControl(''),
      major: new FormControl(''),
      restrictedSems: new FormArray([]),
    });
    restrictedCourses:any[]=['false'].constructor(8);
    selectedCourses:any[]=[];
    satisfiedCourses:any[]=[];
    courses:any[]=[];
    constructor(private dataService: DataService, private shared: SharedService) {}
    ngOnInit() {
      console.log(sessionStorage.getItem("loggedinUser"))
      this.createScheduleForm.patchValue({major:'computer science'})
      const obs = this.dataService.fetchCourseData()
      obs.subscribe(data => {
        this.courses = data.Data;
      });

    }
    
    get semesters(): FormArray {
      const control = this.createScheduleForm.get('semesters');
      if (control instanceof FormArray) {
        return control;
      } else {
        throw new Error('The control is not a FormArray');
      }
    }

    updateSpecificSem(sem_num:number){
      this.restrictedCourses[sem_num] == 'true' ? this.restrictedCourses[sem_num] = 'false' : this.restrictedCourses[sem_num] = 'true';
      console.log(this.restrictedCourses[sem_num])
    }

    createSchedule(){
      const formValues = this.createScheduleForm.value;
      if (formValues.semesters_left == null || formValues.semesters_left == '' || formValues.semesters_left == undefined){
        this.createScheduleForm.patchValue({semesters_left:'8'})
      }
      if (formValues.grad_classes == null || formValues.grad_classes == '' || formValues.grad_classes == undefined){
        this.createScheduleForm.patchValue({grad_classes:'yes'})
      }
      if (formValues.honors == null || formValues.honors == '' || formValues.honors == undefined){
        this.createScheduleForm.patchValue({honors:'no'})
      }
      if (formValues.biological_science_finished == null || formValues.biological_science_finished == '' || formValues.biological_science_finished == undefined){
        this.createScheduleForm.patchValue({honors:'no'})
      }
      if (formValues.physical_sciences_finished == null || formValues.physical_sciences_finished == '' || formValues.physical_sciences_finished == undefined){
        this.createScheduleForm.patchValue({physical_sciences_finished:'0'})
      } else if (+formValues.physical_sciences_finished > 2) {
        this.createScheduleForm.patchValue({physical_sciences_finished:'2'})
      }
      if (formValues.gen_eds_finished == null || formValues.gen_eds_finished == '' || formValues.gen_eds_finished == undefined ){
        this.createScheduleForm.patchValue({gen_eds_finished:'0'})
      } else if (+formValues.gen_eds_finished > 4) {
        this.createScheduleForm.patchValue({gen_eds_finished:'4'})
      }
      if (formValues.max_credits == null || formValues.max_credits == '' || formValues.max_credits == undefined || +formValues.max_credits > 24 || +formValues.max_credits < 0){
        this.createScheduleForm.patchValue({max_credits:'19'})
      }
      if (formValues.min_credits == null || formValues.min_credits == '' || formValues.min_credits == undefined || +formValues.min_credits < 0){
        this.createScheduleForm.patchValue({min_credits:'12'})
      }
      if (formValues.total_credits == null || formValues.total_credits == '' || formValues.total_credits == undefined || +formValues.total_credits < 0){
        this.createScheduleForm.patchValue({total_credits:'0'})
      }

      this.dataService.sendScheduleData(this.createScheduleForm.value).subscribe(response => {
        this.shared.updateSchedule(response)
        console.log('Data sent successfully', response);
      });
    }
  }