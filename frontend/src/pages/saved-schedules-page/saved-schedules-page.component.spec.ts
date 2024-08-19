import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SavedSchedulesPageComponent } from './saved-schedules-page.component';

describe('SavedSchedulesPageComponent', () => {
  let component: SavedSchedulesPageComponent;
  let fixture: ComponentFixture<SavedSchedulesPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SavedSchedulesPageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SavedSchedulesPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});