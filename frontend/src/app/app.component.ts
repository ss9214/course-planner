import { Component, OnInit } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { NgIf } from '@angular/common';
import { MatMenuModule } from '@angular/material/menu';
import { DataService } from '../data.service';
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MatMenuModule, NgIf, RouterOutlet, RouterLink, MatToolbarModule, MatButtonModule, MatDividerModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'frontend';
  constructor(public dataService: DataService) {}
  
  logout(){
    console.log(sessionStorage.getItem('loggedinUser'))
    sessionStorage.removeItem('loggedinUser');
  }
  getUserName(){
    let user:any = sessionStorage.getItem('loggedinUser');
    if (user){
      return user['name'];
    }
    return user
  }
  checkUser(){
    return sessionStorage.getItem('loggedinUser')
  }
  login(){
    window.location.replace('/login') 
  }

  signup(){
    window.location.replace('/signup')
  }
  
  courses(){
    window.location.replace('/courses')
  }
  
  build_schedule(){
    window.location.replace('/create-schedule')
  }

  view_schedule(){
    window.location.replace('/created-schedule')
  }

  view_saved_schedules() {
    window.location.replace('/saved-schedules')
  }
  home(){
    window.location.replace('/')
  }
}
