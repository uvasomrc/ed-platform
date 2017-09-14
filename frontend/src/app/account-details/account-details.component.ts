import {Component, EventEmitter, OnDestroy, OnInit, Output} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {AccountService} from '../account.service';
import {Participant} from '../participant';
import {Session} from "../session";


@Component({
  selector: 'app-account-details',
  templateUrl: './account-details.component.html',
  styleUrls: ['./account-details.component.css']
})
export class AccountDetailsComponent implements OnInit {

  account: Participant;
  isDataLoaded = false;

  constructor(private router: Router,
              private accountService: AccountService) {
  }

  ngOnInit() {
    this.accountService.getAccount().subscribe(acct => {
      this.account = acct;
      this.isDataLoaded = true;
    });
    this.accountService.refreshAccount();
  }

  upcomingSessions(): Array<Session> {
    return this.account.sessions.filter( s => {
      return s.date_time.valueOf() >= new Date().valueOf() && s.instructors.filter( i => i.id === this.account.id).length == 0;
    } );
  }

  pastSessions(): Array<Session> {
    return this.account.sessions.filter( s => {
      return s.date_time.valueOf() < new Date().valueOf() && s.instructors.filter( i => i.id === this.account.id).length == 0;
    } );
  }

  teachingSessions(): Array<Session> {
    return this.account.sessions.filter( s => {
      return s.instructors.filter( i => i.id === this.account.id).length > 0;
    } );
  }

  instructing(): boolean {
    return this.teachingSessions().length > 0;
  }

  onUnRegister(session) {
    console.log("Unregistered for session:" + session.id);
  }


}
