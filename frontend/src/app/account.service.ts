import {Injectable, OnDestroy} from '@angular/core';
import {ApiService} from './api.service';
import {Participant} from './participant';
import {Subscription} from 'rxjs/Subscription';
import {Subject} from 'rxjs/Subject';
import {Observable} from 'rxjs/Observable';
import {Session} from "./session";
import {BehaviorSubject} from "rxjs/BehaviorSubject";
import {Workshop} from "./workshop";
import {environment} from "../environments/environment";

@Injectable()
export class AccountService implements OnDestroy {
  USER_KEY = 'currentUser';
  ROUTE_KEY = 'currentPath';
  login_subscription: Subscription;
  logged_in = false;
  participant = new BehaviorSubject<Participant>(this.from_local());
  login_url = environment.api + '/api/login';

  constructor(private api: ApiService) {}

  from_local() {
    if (localStorage.getItem(this.USER_KEY) !== 'undefined') {
      this.logged_in = true;
      return new Participant(JSON.parse(localStorage.getItem(this.USER_KEY)));
    } else {
      return null;
    }
  }

  goLogin(returnUrl) {
    console.log('The Return URL IS:' + returnUrl);
    localStorage.setItem(this.ROUTE_KEY, returnUrl);
    window.location.href = this.login_url;
  }

  getRouteAfterLogin() {
    console.log('Returning user to ' + localStorage.getItem(this.ROUTE_KEY));
    return localStorage.getItem(this.ROUTE_KEY);
  }

  refreshAccount() {
    console.log('Refresh the account details from the server.');
    this.api.getAccount().subscribe(participant => {
      localStorage.setItem(this.USER_KEY, JSON.stringify(participant));
      this.logged_in = true;
      this.participant.next(participant);
    },
    err => {
      this.logged_in = false;
      this.participant.next(null);
    });
  }

  getAccount(): Observable<Participant> {
    return (this.participant.asObservable());
  }

  getWorkshopsForParticipant(participant:Participant): Observable<Workshop[]> {
    return (this.api.getWorkshopsForParticipant(participant));
  }

  login(token: string): void {
    this.login_subscription = this.api.login(token).subscribe(participant => {
      this.refreshAccount();
    });
  }

  ngOnDestroy() {
    this.login_subscription.unsubscribe();
  }

  isLoggedIn(): boolean {
    return (this.logged_in);
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
