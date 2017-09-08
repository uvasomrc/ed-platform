import { Injectable } from '@angular/core';
import {Participant} from './participant';
import {ApiService} from './api.service';
import {Subject} from 'rxjs/Subject';
import {Observable} from 'rxjs/Observable';

@Injectable()
export class AccountService {

  private userSubject = new Subject<Participant>();

  constructor(private api: ApiService) {
  }

  refreshUser() {
    this.api.getAccount().subscribe(participant => {
      this.userSubject.next(participant);
    });
  }

  login(token: string) {
    this.api.setToken(token);
    this.api.getAccount().subscribe(participant => {
      this.userSubject.next(participant);
    });
  }

  logout() {
    this.api.logout();
    this.userSubject.next();
  }

  getCurrentUser(): Observable<Participant> {
    return this.userSubject.asObservable();
  }
}
