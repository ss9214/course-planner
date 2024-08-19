import { Routes } from '@angular/router';
import { HomePageComponent } from '../pages/home-page/home-page.component'
import { CoursePageComponent } from '../pages/courses-page/courses-page.component';
import { SchedulePageComponent } from '../pages/create-new-schedule-page/create-new-schedule-page.component';
import { ViewSchedulePageComponent } from '../pages/created-schedule-page/created-schedule-page.component';
import { ClassInfoPageComponent } from '../pages/class-info-page/class-info-page.component';
import { LoginPageComponent } from '../pages/login-page/login-page.component';
import { SavedSchedulesPageComponent } from '../pages/saved-schedules-page/saved-schedules-page.component';

export const routes: Routes = [
    {
        path: '',
        title: 'Home Page',
        component: HomePageComponent
    },
    {
        path: 'courses',
        title: 'Course Page',
        component: CoursePageComponent
    },
    {
        path: 'create-schedule',
        title: 'Schedule Page',
        component: SchedulePageComponent
    },
    {
        path: 'created-schedule',
        title: 'View Schedule Page',
        component: ViewSchedulePageComponent
    },
    {
        path: 'class-info',
        title: 'Class Info Page',
        component: ClassInfoPageComponent
    },
    {
        path: 'login',
        title: 'Login Page',
        component:LoginPageComponent
    },
    {
        path: 'saved-schedules',
        title: 'Saved Schedules Page',
        component:SavedSchedulesPageComponent
    },
    
];
