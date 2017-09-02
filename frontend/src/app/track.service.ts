import { Injectable } from '@angular/core';
import {Http} from '@angular/http';
import {Track} from './track';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import { environment } from '../environments/environment';
import {ApiService} from "./api.service";

@Injectable()
export class TrackService {

  constructor(private api: ApiService) {}

  getTracks(): Observable<Track[]> {
    return this.api.getTracks();
  }

}
