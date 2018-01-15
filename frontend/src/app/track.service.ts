import { Injectable } from '@angular/core';
import {Track} from './track';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import {ApiService} from './api.service';
import {Workshop} from './workshop';
import {Code} from './code';

@Injectable()
export class TrackService {

  constructor(private api: ApiService) {
  }

  getTracks(): Observable<Track[]> {
    return this.api.getTracks();
  }

  getTrack(track_id: number): Observable<Track> {
    return this.api.getTrack(track_id);
  }

  getCode(code: Code): Observable<Code> {
    return this.api.getCode(code);
  }

  addTrack(track: Track): Observable<Track> {
    return this.api.addTrack(track);
  }

  updateTrack(track: Track): Observable<Track> {
    return this.api.updateTrack(track);
  }

  deleteTrack(track: Track): Observable<Track> {
    return this.api.deleteTrack(track);
  }

  addCode(code: Code): Observable<Code> {
    return this.api.addCode(code);
  }

  getAllCodes(): Observable<Code[]> {
    return this.api.getAllCodes();
  }

  updateTrackImage(track: Track, file: File) {
    this.api.updateTrackImage(track, file).subscribe();
  }

}
