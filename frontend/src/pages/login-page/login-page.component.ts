import { Component, OnInit } from '@angular/core';
import {MatCardModule} from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import {MatFormFieldModule, MatFormField} from '@angular/material/form-field';
import { FormControl, ReactiveFormsModule, FormGroup, FormArray } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
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
  selector: 'app-login-page',
  standalone: true,
  imports: [MatSelectModule,MatSliderModule, MatRadioModule,MatIconModule, MatInputModule, CommonModule,MatCardModule,MatButtonModule,MatFormFieldModule, MatFormField,RouterLink,ReactiveFormsModule,MatCheckboxModule],
  templateUrl: './login-page.component.html',
  styleUrl: './login-page.component.css'
})
export class LoginPageComponent {
  hide = true;
  username = '';
  password = '';
  error = '';
  loading = false;

  constructor(private dataService: DataService, private router: Router) {}

  invalid_email(){
    console.log(sessionStorage.getItem("invalidEmail"));
    return sessionStorage.getItem("invalidEmail");
  }
}