import { Injectable } from "@angular/core";
import { BehaviorSubject } from "rxjs";


@Injectable({
  providedIn: "root"
})

export class SharedService{
    private satisfiedCoursesSource = new BehaviorSubject<string>("");
    private createdScheduleSource = new BehaviorSubject<any>({});
    // private savedSchedulesSource = new BehaviorSubject<any>([]);
    private courseInfoSource = new BehaviorSubject<any>({});
    satisfiedCourses = this.satisfiedCoursesSource.asObservable();
    createdSchedule = this.createdScheduleSource.asObservable();
    // savedSchedules = this.savedSchedulesSource.asObservable();
    courseInfo = this.courseInfoSource.asObservable();
    constructor(){}
    changeSatisfiedCourses(courses: string){
      this.satisfiedCoursesSource.next(courses)
    }
    updateSchedule(schedule:any){
      this.createdScheduleSource.next(schedule["data"])
      this.createdSchedule.subscribe(x=>{console.log(x);console.log("hi")})
    }
    // updateSavedSchedules(schedule:any,change:any){
    //   const array = this.savedSchedulesSource.getValue()
    //   if (change=='add'){
    //     array.push(schedule)
    //   } else if (change=='remove'){
    //     array.splice(array.indexOf(schedule),1)
    //   }
    //   this.savedSchedulesSource.next(array)
    // }
    updateCourseInfo(course:any) {
      this.courseInfoSource.next(course)
    }
  }