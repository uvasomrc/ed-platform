import {Injectable, OnDestroy} from '@angular/core';
import {ApiService} from './api.service';
import {Participant} from './participant';
import {Subscription} from 'rxjs/Subscription';
import {Subject} from 'rxjs/Subject';
import {Observable} from 'rxjs/Observable';
import {Session} from './session';
import {BehaviorSubject} from 'rxjs/BehaviorSubject';
import {Workshop} from './workshop';
import {environment} from '../environments/environment';
import {RequestOptions} from '@angular/http';
import {Search} from './search';

@Injectable()
export class AccountService implements OnDestroy {
  USER_KEY = 'currentUser';
  ROUTE_KEY = 'currentPath';
  login_subscription: Subscription;
  logged_in = false;
  participant = new BehaviorSubject<Participant>(this.from_local());
  login_url = environment.api + '/api/login';

  constructor(private api: ApiService) {}

  getOptions(): RequestOptions {
    return this.api.getOptions();
  }

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
    console.log('Refresh the participant details from the server.');
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

  updatePaticipant(participant: Participant): Observable<Participant> {
    this.api.updateParticipant(participant).subscribe( updated_p => {
      this.participant.next(updated_p);
    });
    return this.participant.asObservable();
  }

  updateParticipantImage(participant: Participant, file: File) {
    this.api.updateParticipantImage(participant, file).subscribe();
  }

  getWorkshopsForParticipant(participant: Participant): Observable<Workshop[]> {
    return (this.api.getWorkshopsForParticipant(participant));
  }

  search(search: Search): Observable<Search> {
    return (this.api.searchParticipants(search));
  }

  login(token: string): Observable<Participant> {
    const po = this.api.login(token);
    po.subscribe(participant => {
        localStorage.setItem(this.USER_KEY, JSON.stringify(participant));
        this.logged_in = true;
        this.participant.next(participant);
        (<any>window).gtag('event', participant.display_name, {
          'event_category': 'login'
        });
      },
      err => {
        this.logged_in = false;
        this.participant.next(null);
      });
    return po;
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
