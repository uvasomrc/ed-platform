import { Injectable } from '@angular/core';
import {Participant} from './participant';
import {Observable} from 'rxjs/Observable';
import {ApiService} from "./api.service";

@Injectable()
export class AccountService {

  constructor(private api: ApiService) {}

  setToken(token: string) {
    this.api.token = token;
  }

  getAccount(): Observable<Participant> {
    return this.api.getAccount();
  }
}
