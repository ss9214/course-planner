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

  // get(endpoint: string): Observable<any> {
  //   return this.http.get(`${this.ROOT_URL}/get${endpoint}`).pipe(
  //     catchError((error) => {
  //       console.error('Error making HTTP request', error);
  //       return error;
  //     })
  //   );
  // }



  fetchCourseData(): Observable<any> {
    const obs = this.http.get(`http://localhost:5000/api/get/courses`)
    return obs
    // const obs = this.get('/courses');

  }
  sendScheduleData(data:any) : Observable<any>{
    return this.http.post(`http://localhost:5000/api/post/schedule`,data)
  }

}