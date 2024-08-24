import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, catchError } from 'rxjs';
import { FormGroup } from '@angular/forms';

export interface Parameter {
  param: string;
  value: string;
}

@Injectable({
  providedIn: 'root'
})

export class DataService {
  private readonly ROOT_URL = 'http://localhost:5000/api';
  courses: any[] = [];
  constructor(private http: HttpClient) {}

  fetchCourseData(): Observable<any> {
    return this.http.get(`http://localhost:5000/api/get/courses`);

  }

  sendScheduleData(data:any) : Observable<any>{
    return this.http.post(`http://localhost:5000/api/post/schedule`,data);
  }

  sendSavedScheduleData(data:any) : Observable<any> {
    let user:any = sessionStorage.getItem("loggedinUser")
    let email:any=null;
    if (user) {user = JSON.parse(user); email = user["email"]}
    return this.http.post(`http://localhost:5000/api/post/save-schedule`,{"Email":email, "Schedule":data});
  }

  removeSavedScheduleData(data:any) : Observable<any> {
    let user:any = sessionStorage.getItem("loggedinUser")
    let email:any=null;
    if (user) {user = JSON.parse(user); email = user["email"]}
    return this.http.post(`http://localhost:5000/api/post/remove-schedule`,{"Email":email, "Schedule":data});
  }

  fetchSavedScheduleData() : Observable<any> {
    let user:any = sessionStorage.getItem("loggedinUser")
    let email:any=null;
    if (user) {user = JSON.parse(user); email = user["email"]}
    return this.http.post(`http://localhost:5000/api/post/saved-schedules`,{"Email":email});
  }
}