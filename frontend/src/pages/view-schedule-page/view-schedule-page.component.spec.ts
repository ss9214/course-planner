import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewSchedulePageComponent } from './view-schedule-page.component';

describe('ViewSchedulePageComponent', () => {
  let component: ViewSchedulePageComponent;
  let fixture: ComponentFixture<ViewSchedulePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewSchedulePageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ViewSchedulePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});