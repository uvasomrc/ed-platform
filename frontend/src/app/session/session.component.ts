import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Session} from '../session';
import {AccountService} from '../account.service';
import {Participant} from '../participant';
import {Router} from "@angular/router";
import {DatePipe} from "@angular/common";

@Component({
  selector: 'app-session',
  templateUrl: './session.component.html',
  styleUrls: ['./session.component.scss']
})
export class SessionComponent implements OnInit {

  @Input()
  session: Session;

  account: Participant;

  @Output()
  unRegister: EventEmitter<Session> = new EventEmitter();

  @Output()
  register: EventEmitter<Session> = new EventEmitter();

  available = false;
  removed = false;

  constructor(private accountService: AccountService,
              private router: Router,
              private datePipe: DatePipe) {}

  ngOnInit() {
    this.available = this.session.isAvailable();
    this.accountService.getAccount().subscribe (account => {
      if (account != null) {
        this.account = account;
        if (this.session.registered() || this.session.instructing()) {
          this.available = false;
        }
      }
    });
  }

  removeSession() {
    this.accountService.unRegister(this.session).subscribe( session => {
      this.session = session;
      this.removed = true;
      this.unRegister.emit(this.session);
    });
  }

  addSession() {
    console.log('Adding Session!');
    this.accountService.register(this.session).subscribe( session => {
      this.session = session;
      this.removed = false;
      this.register.emit(this.session);
    });
  }

  // The date pipe wasn't updating when used in the template, so moved it here.
  dateAsString() {
    return this.datePipe.transform(this.session.date_time, 'EEE. MMMM d, y, h:mm-');
  }


  teacherDashboard() {
    this.router.navigate(['teacherDashboard', this.session.id]);
  }

  goWorkshop(id) {
    this.router.navigate(['workshop', id]);
  }
}
