import {Component, Input, OnInit} from '@angular/core';
import {TrackService} from "../track.service";
import {Track} from "../track";
import {Observable} from "rxjs/Observable";

@Component({
  selector: 'app-track-list',
  templateUrl: './track-list.component.html',
  styleUrls: ['./track-list.component.css']
})
export class TrackListComponent implements OnInit {

  private trackService:TrackService;
  private tracks: Observable<Track[]>;

  constructor(trackService:TrackService) {
    this.trackService = trackService;
  }

  ngOnInit() {
    this.tracks = this.trackService.getTracks();
  }
}
