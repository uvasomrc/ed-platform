import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Session} from '../session';
import * as moment from 'moment';

@Component({
  selector: 'app-session-form',
  templateUrl: './session-form.component.html',
  styleUrls: ['./session-form.component.scss']
})
export class SessionFormComponent implements OnInit {

  sessionForm: FormGroup;
  date: FormControl;
  instructor_notes: FormControl;
  duration_minutes: FormControl;
  location: FormControl;
  max_attendees: FormControl;
  minDate = new Date();

  @Input()
  session: Session = new Session();

  @Output()
  newSession: EventEmitter<Session> = new EventEmitter();

  constructor() {
    this.session = new Session();
  }

  ngOnInit() {
    this.loadForm();
  }

  loadForm() {
    let momentDate = moment(this.session.date_time);
    console.log(`Moment Time is ${momentDate.toJSON()}`);
    this.date = new FormControl(this.session.date_time, [Validators.required]);
    this.instructor_notes = new FormControl(this.session.instructor_notes);
    this.duration_minutes = new FormControl(this.session.duration_minutes, [Validators.required]);
    this.location = new FormControl(this.session.location, [Validators.required]);
    this.max_attendees = new FormControl(this.session.max_attendees, [Validators.required]);

    this.sessionForm = new FormGroup({
      date: this.date,
      instructor_notes: this.instructor_notes,
      duration_minutes: this.duration_minutes,
      location: this.location,
      max_attendees: this.max_attendees
    });

    /*
    this.date.valueChanges.subscribe(d => { this.session.date_time = d.toDate(); });
    this.instructor_notes.valueChanges.subscribe(i => this.session.instructor_notes = i);
    this.duration_minutes.valueChanges.subscribe(d => this.session.duration_minutes = d);
    this.location.valueChanges.subscribe(l => this.session.location = l);
    this.max_attendees.valueChanges.subscribe(m => this.session.max_attendees = m);
    */
    this.editSession(this.session);
  }

  editSession(session: Session) {
    this.session = session;
    if(this.session.date_time) {
      console.log(`setting the date to ${this.session.date_time}`)
      this.date.patchValue(this.session.date_time);
    }
    this.instructor_notes.patchValue(this.session.instructor_notes);
    this.duration_minutes.patchValue(this.session.duration_minutes);
    this.location.patchValue(this.session.location);
    this.max_attendees.patchValue(this.session.max_attendees);
  }

  onSubmit() {
    if (this.sessionForm.valid) {
      this.session.date_time = this.date.value.toDate();
      this.session.instructor_notes = this.instructor_notes.value;
      this.session.duration_minutes = this.duration_minutes.value;
      this.session.location = this.location.value;
      this.session.max_attendees = this.max_attendees.value;
      this.newSession.emit(this.session);
      // Fixme: This should just be a reset, but that doesn't work.
      this.sessionForm.reset();
    }
  }

}
