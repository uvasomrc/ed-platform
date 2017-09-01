import { Injectable } from '@angular/core';
import {Http, Headers, RequestOptions} from '@angular/http';
import {Track} from './track';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import { environment } from '../environments/environment';
import {Workshop} from "./workshop";

@Injectable()
export class WorkshopService {

  apiRoot = environment.api;
  url = `${this.apiRoot}/api/workshop`;
  results: Workshop[];
  loading: boolean;
  headers: Headers;
  options: RequestOptions;

  constructor(private http: Http) {
    this.results = [];
    this.loading = false;
    this.headers = new Headers({ 'Content-Type': 'application/json',
      'Accept': 'q=0.8;application/json;q=0.9' });
    this.options = new RequestOptions({ headers: this.headers });
  }

  getWorkshops(): Observable<Workshop[]> {
    return this.http.get(this.url)
      .map(res => {
        return res.json().workshops.map(item => {
          const image_url = `${this.apiRoot}${item._links.image}`;
          return new Workshop(item.id, item.title, item.description, image_url);
        });
      });
  }

  createWorkshop(workshop: Workshop): Observable<Workshop> {
    const body = JSON.stringify(workshop);
    return this.http
      .post(this.url, body, this.options)
      .map(res => {
        return res.json().workshops.map(item => {
          const image_url = `${this.apiRoot}${item._links.image}`;
          return new Workshop(item.id, item.title, item.description, image_url);
        });
      });
  }

}
