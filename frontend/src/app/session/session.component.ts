import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Session} from '../session';
import {AccountService} from '../account.service';
import {Participant} from '../participant';
import {Router} from "@angular/router";

@Component({
  selector: 'app-session',
  templateUrl: './session.component.html',
  styleUrls: ['./session.component.css']
})
export class SessionComponent implements OnInit {

  @Input()
  session: Session;

  account: Participant;

  @Output()
  unRegister: EventEmitter<Session> = new EventEmitter();

  @Output()
  register: EventEmitter<Session> = new EventEmitter();

  taking = false;
  teaching = false;
  available = false;
  removed = false;

  constructor(private accountService: AccountService,
              private router: Router) {}

  ngOnInit() {
    this.available = this.session.isAvailable();
    this.accountService.getAccount().subscribe (account => {
      this.account = account;
      this.taking = this.account.isUpcoming(this.session);
      this.teaching = this.account.isTeaching(this.session);
      if (this.teaching || this.taking) { this.available = false; }
    });
  }

  status() {
    if (this.removed) { return 'removed'; }
    if (this.taking) { return 'taking'; }
    if (this.teaching) { return 'teaching'; }
    if (this.available) { return 'available'; }
  }

  removeSession() {
    this.accountService.unRegister(this.session).subscribe( session => {
      this.session = session;
      this.removed = true;
      this.taking  = false;
      this.unRegister.emit(this.session);
    });
  }

  addSession() {
    console.log('Adding Session!');
    this.accountService.register(this.session).subscribe( session => {
      this.session = session;
      this.taking = true;
      this.removed = false;
      this.register.emit(this.session);
    });
  }

  teacherDashboard() {
    this.router.navigate(['teacherDashboard', this.session.id]);
  }

}
