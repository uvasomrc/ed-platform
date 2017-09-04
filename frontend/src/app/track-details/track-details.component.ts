import { Component, OnInit } from '@angular/core';
import {Track} from '../track';
import {Workshop} from '../workshop';
import {TrackService} from '../track.service';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-track-details',
  templateUrl: './track-details.component.html',
  styleUrls: ['./track-details.component.css']
})
export class TrackDetailsComponent implements OnInit {

  track_id = 49;
  track: Track;
  workshops: Workshop[] = [];
  isDataLoaded = false;

  constructor(private trackService: TrackService,
              private route: ActivatedRoute) {
    this.route.params.subscribe( params =>
          this.track_id = params['id']);
  }

  ngOnInit() {
    this.trackService.getTrack(this.track_id).subscribe(
      (track) => {
        this.track = track;
        this.getWorkshops(track);
        this.isDataLoaded = true;
      }

    );
  }

  getWorkshops(track: Track) {
    this.trackService.getWorkshops(track).subscribe(
      (workshops) => {this.workshops = workshops; }
    );
  }

}
