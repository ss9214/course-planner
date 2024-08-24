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
  selector: 'app-saved-schedules-page',
  standalone: true,
  imports: [MatAutocompleteModule,FormsModule,MatSelectModule,MatSliderModule, MatRadioModule,MatIconModule, MatInputModule, CommonModule,MatCardModule,MatButtonModule,MatFormFieldModule, MatFormField,RouterLink,ReactiveFormsModule,MatCheckboxModule],
  templateUrl: './saved-schedules-page.component.html',
  styleUrl: './saved-schedules-page.component.css'
})
export class SavedSchedulesPageComponent implements OnInit {

  constructor(private dataService:DataService, private shared:SharedService) {}
  
  saved_schedules:any[]=[];
  ngOnInit(): void {
    this.dataService.fetchSavedScheduleData().subscribe(response=>this.saved_schedules=response["data"])
  }
  makeSchedule(schedule:any) {
    console.log(schedule)
    this.shared.updateSchedule(schedule)
    //window.location.replace('/created-schedule')
  }
}