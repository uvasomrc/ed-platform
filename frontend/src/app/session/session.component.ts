import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Session} from '../session';
import {AccountService} from '../account.service';
import {Participant} from '../participant';
import {Router} from '@angular/router';
import {DatePipe} from '@angular/common';

@Component({
  selector: 'app-session',
  templateUrl: './session.component.html',
  styleUrls: ['./session.component.scss']
})
export class SessionComponent implements OnInit {

  @Input()
  session: Session;
  account: Participant;

  @Input()
  showButtons = true;

  @Output()
  registerEvent: EventEmitter<Session> = new EventEmitter();



  constructor(private accountService: AccountService,
              private router: Router,
              private datePipe: DatePipe) {}

  ngOnInit() {
    this.accountService.getAccount().subscribe (account => {
      if (account != null) {
        this.account = account;
      }
    });
  }

  // The date pipe wasn't updating when used in the template, so moved it here.
  dateAsString() {
    return this.datePipe.transform(this.session.date_time, 'EEE. MMMM d, y, h:mm-');
  }

  goSessionDashboard() {
    this.router.navigate(['sessionDashboard', this.session.id]);
  }

  register() {
    this.session.status = 'CHANGING';
    this.accountService.register(this.session).subscribe(
      (newSession) => {
        (<any>window).gtag('event', "session #" + this.session.id, {
          'event_category': 'register'
        });
        this.session = newSession;
        this.registerEvent.emit(this.session);
      });
  }

  unRegister() {
    this.session.status = 'CHANGING';
    this.accountService.unRegister(this.session).subscribe(
      (newSession) => {
        (<any>window).gtag('event', "session #" + this.session.id, {
          'event_category': 'unregister'
        });
        this.session = newSession;
        this.registerEvent.emit(this.session);
      });
  }

}
