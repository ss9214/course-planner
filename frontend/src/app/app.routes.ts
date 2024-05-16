import { Routes } from '@angular/router';
import { HomePageComponent } from '../pages/home-page/home-page.component'
import { CoursePageComponent } from '../pages/courses-page/courses-page.component';


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
    }
];
