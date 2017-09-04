import { Injectable } from '@angular/core';
import {Track} from './track';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import {ApiService} from './api.service';
import {Workshop} from './workshop';

@Injectable()
export class TrackService {

  constructor(private api: ApiService) {}

  getTracks(): Observable<Track[]> {
    return this.api.getTracks();
  }

  getTrack(track_id: number): Observable<Track> {
    return this.api.getTrack(track_id);
  }

  getWorkshops(track: Track): Observable<Workshop[]> {
    return this.api.getTrackWorkshops(track);
  }


}
