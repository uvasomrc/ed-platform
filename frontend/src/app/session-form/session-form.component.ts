import {Component, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {Session} from '../session';
import * as moment from 'moment';
import {MatDatepicker} from "@angular/material";

@Component({
  selector: 'app-session-form',
  templateUrl: './session-form.component.html',
  styleUrls: ['./session-form.component.scss']
})
export class SessionFormComponent implements OnInit {

  sessionForm: FormGroup;
  date: FormControl;
  time: FormGroup;
  hour: FormControl;
  minute: FormControl;
  ampm: FormControl;
  instructor_notes: FormControl;
  duration_minutes: FormControl;
  max_days_prior: FormControl;
  location: FormControl;
  max_attendees: FormControl;
  hour_values = new Array(12);
  minute_values = new Array(60);


  @Input()
  session: Session = new Session();

  @Output()
  newSession: EventEmitter<Session> = new EventEmitter();

  @Output()
  deleteSession: EventEmitter<Session> = new EventEmitter();

  @ViewChild(MatDatepicker) picker: MatDatepicker<Date>;

  constructor() {
    this.session = new Session();
  }

  ngOnInit() {
    this.loadForm();
  }

  loadForm() {
    this.date = new FormControl(this.session.date_time, [Validators.required]);
    this.hour = new FormControl([Validators.required]);
    this.minute = new FormControl([Validators.required]);
    this.ampm = new FormControl([Validators.required]);
    this.instructor_notes = new FormControl(this.session.instructor_notes);
    this.duration_minutes = new FormControl(this.session.duration_minutes, [Validators.required]);
    this.max_days_prior = new FormControl(this.session.max_days_prior);
    this.location = new FormControl(this.session.location, [Validators.required]);
    this.max_attendees = new FormControl(this.session.max_attendees, [Validators.required]);

    this.time = new FormGroup({
      hour: this.hour,
      minute: this.minute,
      ampm: this.ampm
    });

    this.sessionForm = new FormGroup({
      date: this.date,
      time: this.time,
      instructor_notes: this.instructor_notes,
      duration_minutes: this.duration_minutes,
      max_days_prior: this.max_days_prior,
      location: this.location,
      max_attendees: this.max_attendees
    });


    this.editSession(this.session);
  }

  minDate() {
    return new Date();
  }

  editSession(session: Session) {
    this.session = session;
    if (this.session.date_time) {
      console.log(`setting the date to ${this.session.date_time}`);
      this.date.patchValue(this.session.date_time);
      let hours = this.session.date_time.getHours() % 12;
      hours = hours ? hours : 12;
      this.hour.patchValue(hours);
      this.minute.patchValue(session.date_time.getMinutes());
      this.ampm.patchValue(session.date_time.getHours() >= 12 ? 'PM' : 'AM');
    }
    this.instructor_notes.patchValue(this.session.instructor_notes);
    this.duration_minutes.patchValue(this.session.duration_minutes);
    this.location.patchValue(this.session.location);
    this.max_attendees.patchValue(this.session.max_attendees);
    this.max_days_prior.patchValue(this.session.max_days_prior);
  }

  onSubmit() {
    if (this.sessionForm.valid) {
      console.log("The Date is a " + this.date.value.className);
      const date = this.date.value;
      let hours = this.hour.value;
      if (this.hour.value === 12) {
        if (this.ampm.value === 'AM') hours = 0;
      } else {
        if (this.ampm.value === 'PM') hours += 12;
      }

      date.setHours(hours);
      date.setMinutes(this.minute.value);
      this.session.date_time = date;
      this.session.instructor_notes = this.instructor_notes.value;
      this.session.duration_minutes = this.duration_minutes.value;
      this.session.location = this.location.value;
      this.session.max_attendees = this.max_attendees.value;
      this.session.max_days_prior = this.max_days_prior.value;
      this.newSession.emit(this.session);
      // Fixme: This should just be a reset, but that doesn't work.
      this.session = new Session();
      this.sessionForm.reset();
    }
  }

  onDelete() {
    this.deleteSession.emit(this.session);
    this.session = new Session();
  }

  onReset() {
    this.session = new Session();
    this.sessionForm.reset();
  }

}
