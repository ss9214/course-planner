import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClassInfoPageComponent } from './class-info-page.component';

describe('ClassInfoPageComponent', () => {
  let component: ClassInfoPageComponent;
  let fixture: ComponentFixture<ClassInfoPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClassInfoPageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ClassInfoPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});