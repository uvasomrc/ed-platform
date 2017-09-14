import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ParticipantsSessionsComponent } from './participants-sessions.component';

describe('ParticipantsSessionsComponent', () => {
  let component: ParticipantsSessionsComponent;
  let fixture: ComponentFixture<ParticipantsSessionsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ParticipantsSessionsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ParticipantsSessionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
