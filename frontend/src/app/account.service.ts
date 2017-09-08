import { Injectable } from '@angular/core';
import {Participant} from './participant';
import {ApiService} from './api.service';
import {Subject} from 'rxjs/Subject';
import {Observable} from 'rxjs/Observable';
import {HttpErrorResponse} from "@angular/common/http";

@Injectable()
export class AccountService {

  private userSubject  = new Subject<Participant>();
  private errorSubject = new Subject<string>();

  constructor(private api: ApiService) {
  }

  refreshUser() {
    if (!this.api.token) return;
    this.api.getAccount().subscribe(
      // Successful responses call the first callback.
      data => {
        this.userSubject.next(data);
        console.log('Got this back:' + JSON.stringify(data));
      },
      (err: HttpErrorResponse) => {
        console.log('Something went wrong!' + err);
        if (err.error instanceof Error) {
          this.errorSubject.next(err.message);
        } else {
          this.errorSubject.next(err.error);
        }
      });
  }

  login(token: string) {
    this.api.setToken(token);
    this.refreshUser();
  }

  logout() {
    this.api.logout();
    this.userSubject.next();
  }

  getCurrentUser(): Observable<Participant> {
    return this.userSubject.asObservable();
  }
}
