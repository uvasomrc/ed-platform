import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Session} from '../session';
import {AccountService} from '../account.service';
import {Participant} from '../participant';
import {Router} from "@angular/router";

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
              private router: Router) {}

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

  teacherDashboard() {
    this.router.navigate(['teacherDashboard', this.session.id]);
  }

  goWorkshop(id) {
    this.router.navigate(['workshop', id]);
  }
}
