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
    return this.http.post(`http://localhost:5000/api/post/save-schedule`,data);
  }

  removeSavedScheduleData(data:any) : Observable<any> {
    return this.http.post(`http://localhost:5000/api/post/remove-schedule`,data);
  }

  fetchSavedScheduleData() : Observable<any> {
    return this.http.get(`http://localhost:5000/api/get/saved-schedules`);
  }
}