import { Injectable } from '@angular/core';
import {Http} from '@angular/http';
import {Track} from './track';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import { environment } from '../environments/environment';

@Injectable()
export class TrackService {

  apiRoot = environment.api;
  results: Track[];
  loading: boolean;

  constructor(private http: Http) {
    this.results = [];
    this.loading = false;
  }

  getTracks(): Observable<Track[]> {
    const url = `${this.apiRoot}/api/track`;
    return this.http.get(url)
      .map(res => {
        return res.json().tracks.map(item => {
          const image_url = `${this.apiRoot}${item._links.image}`
          return new Track(item.id, item.title, item.description, image_url);
        });
      });
  }

}
