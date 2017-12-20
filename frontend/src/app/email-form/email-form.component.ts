import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {EmailMessage} from '../EmailMessage';

@Component({
  selector: 'app-email-form',
  templateUrl: './email-form.component.html',
  styleUrls: ['./email-form.component.css']
})
export class EmailFormComponent implements OnInit {

  email_form: FormGroup;
  email_title: FormControl;
  email_content: FormControl;

  @Output()
  newEmail: EventEmitter<EmailMessage> = new EventEmitter();

  constructor() { }

  ngOnInit() {
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
      this.newEmail.emit(email);
      this.email_form.reset();
      this.email_form.enable();
    }
  }

}
