import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Session} from '../session';
import {AccountService} from '../account.service';

@Component({
  selector: 'app-session',
  templateUrl: './session.component.html',
  styleUrls: ['./session.component.css']
})
export class SessionComponent implements OnInit {

  @Input()
  session: Session;

  @Output()
  unRegister: EventEmitter<Session> = new EventEmitter();

  @Output()
  register: EventEmitter<Session> = new EventEmitter();

  status = 'active';

  constructor(private accountService: AccountService) { }

  ngOnInit() {
  }

  removeSession() {
    this.accountService.unRegister(this.session).subscribe( session => {
      this.session = session;
      this.status = 'removed';
      this.unRegister.emit(this.session);
    });
  }

  addSession() {
    this.accountService.register(this.session).subscribe( session => {
      this.session = session;
      this.status = 'active';
      this.register.emit(this.session);
    });
  }

}
