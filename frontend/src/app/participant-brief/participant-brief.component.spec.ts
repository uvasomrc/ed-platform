import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ParticipantBriefComponent } from './participant-brief.component';

describe('ParticipantBriefComponent', () => {
  let component: ParticipantBriefComponent;
  let fixture: ComponentFixture<ParticipantBriefComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ParticipantBriefComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ParticipantBriefComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
