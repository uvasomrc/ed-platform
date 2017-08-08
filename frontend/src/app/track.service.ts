import { Injectable } from '@angular/core';
import {Http} from "@angular/http";
import {Track} from "./track";
import {Observable} from "rxjs/Observable";
import "rxjs/add/operator/map";

@Injectable()
export class TrackService {

  apiRoot:string = 'http://localhost:5000';
  results: Track[];
  loading: boolean;

  constructor(private http:Http) {
    this.results = [];
    this.loading = false;
  }

  getTracks():Observable<Track[]> {
    let url = `${this.apiRoot}/track`;
    return this.http.get(url)
      .map(res => {
        return res.json().tracks.map(item => {
          return new Track(item.name);
        })
      });
  }

}
