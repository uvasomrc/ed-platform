import { Component, OnInit } from '@angular/core';
import {Participant} from '../participant';
import {Session} from '../session';
import {WorkshopService} from '../workshop.service';
import {ActivatedRoute} from '@angular/router';
import {FormControl, FormGroup, Validators} from "@angular/forms";

@Component({
  selector: 'app-teacher-dashboard',
  templateUrl: './teacher-dashboard.component.html',
  styleUrls: ['./teacher-dashboard.component.css']
})
export class TeacherDashboardComponent implements OnInit {

  account: Participant;
  session: Session;
  session_id = 0;
  is_data_loaded = false;
  email_form: FormGroup;
  email_title: FormControl;
  email_content: FormControl;

  constructor(private workshopService: WorkshopService,
              private route: ActivatedRoute) {
    this.route.params.subscribe( params =>
      this.session_id = params['id']);
  }

  ngOnInit() {
    this.workshopService.getSession(this.session_id).subscribe(
      session => {
        this.session = session;
        this.is_data_loaded = true;
      }
    );
    this.createFormControls();
    this.createForm();
  }

  createFormControls() {
    this.email_title = new FormControl('', [Validators.required, Validators.maxLength(256)]);
    this.email_content = new FormControl('', [Validators.required, Validators.minLength(20)]);
  }

  createForm() {
    this.email_form = new FormGroup({
      email_title: this.email_title,
      email_content: this.email_content
    });
  }

  onSendEmail() {
    if (this.email_form.valid) {
      console.log(`Sending an email message with subject: ${this.email_title.value}`);
    }
  }


}
