import { Routes } from '@angular/router';
import { HomePageComponent } from '../pages/home-page/home-page.component'
import { CoursePageComponent } from '../pages/courses-page/courses-page.component';
import { SchedulePageComponent } from '../pages/schedule-page/schedule-page.component';
import { ViewSchedulePageComponent } from '../pages/view-schedule-page/view-schedule-page.component';
import { ClassInfoPageComponent } from '../pages/class-info-page/class-info-page.component';

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
        path: 'schedule',
        title: 'Schedule Page',
        component: SchedulePageComponent
    },
    {
        path: 'view-schedule',
        title: 'View Schedule Page',
        component: ViewSchedulePageComponent
    },
    {
        path: 'class-info',
        title: 'Class Info Page',
        component: ClassInfoPageComponent
    }
];
