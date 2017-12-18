import { Component, OnInit } from '@angular/core';
import {Participant} from '../participant';
import {Session} from '../session';
import {WorkshopService} from '../workshop.service';
import {ActivatedRoute} from '@angular/router';
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {EmailMessage} from "../EmailMessage";
import {Workshop} from "../workshop";

@Component({
  selector: 'app-session-dashboard',
  templateUrl: './session-dashboard.component.html',
  styleUrls: ['./session-dashboard.component.scss']
})
export class SessionDashboardComponent implements OnInit {

  account: Participant;
  session: Session;
  workshop: Workshop;
  session_id = 0;
  is_data_loaded = false;
  is_sending = false;
  email_form: FormGroup;
  email_title: FormControl;
  email_content: FormControl;
  messages: EmailMessage[];
  selected_tab: number;

  constructor(private workshopService: WorkshopService,
              private route: ActivatedRoute) {
    this.route.params.subscribe( params =>
      this.session_id = params['id']);
  }

  ngOnInit() {
    this.workshopService.getSession(this.session_id).subscribe(
      session => {
        this.session = session;
        this.workshopService.getWorkshopForSession(this.session).subscribe(
          workshop => {
            this.workshop = workshop;
            this.workshopService.getMessages(this.session).subscribe(
              messages => {
                this.messages = messages;
                this.is_data_loaded = true;
              });
          });
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
      const email = new EmailMessage({'subject': this.email_title.value,
                                  'content': this.email_content.value});
      this.email_form.disable();
      this.is_sending = true;
      this.workshopService.emailParticipants(email, this.session).subscribe(
        message => {
          this.messages.push(message);
          this.email_form.reset();
          this.email_form.enable();
          this.selected_tab = 2;
          this.is_sending = false;
        }
      );
      console.log(`Sending an email message with subject: ${this.email_title.value}`);
    }
  }
}
