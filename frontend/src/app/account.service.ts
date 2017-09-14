import {Injectable, OnDestroy} from '@angular/core';
import {ApiService} from './api.service';
import {Participant} from './participant';
import {Subscription} from 'rxjs/Subscription';
import {Subject} from 'rxjs/Subject';
import {Observable} from 'rxjs/Observable';
import {Session} from "./session";

@Injectable()
export class AccountService implements OnDestroy {
  USER_KEY = 'currentUser';
  login_subscription: Subscription;
  participant = new Subject<Participant>();
  cachedParticipant: Participant;

  constructor(private api: ApiService) {}

  refreshAccount() {
    console.log('Refresh the account details from the server.');
    this.api.getAccount().subscribe(participant => {
      localStorage.setItem(this.USER_KEY, JSON.stringify(participant));
      this.cachedParticipant = participant;
      this.participant.next(participant);
    },
    err => {
      this.participant.next(null);
    });
  }

  getAccount(): Observable<Participant> {
    return (this.participant.asObservable());
  }

  getCachedAccount(): Participant {
    return this.cachedParticipant;
  }

  login(token: string): void {
    this.login_subscription = this.api.login(token).subscribe(participant => {
      localStorage.setItem(this.USER_KEY, JSON.stringify(participant));
      this.refreshAccount();
    });
  }

  ngOnDestroy() {
    this.login_subscription.unsubscribe();
  }

  isLoggedIn(): boolean {
    return (this.getAccount() !== null);
  }

  logout() {
    this.api.logout();
    localStorage.setItem(this.USER_KEY, 'undefined');
    this.refreshAccount();
  }

  register(session): Observable<Session> {
    return this.api.register(session);
  }

  unRegister(session): Observable<Session> {
    return this.api.unRegister(session);
  }

}
