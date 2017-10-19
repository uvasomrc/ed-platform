import {Component, OnInit} from '@angular/core';
import {Track} from '../track';
import {Workshop} from '../workshop';
import {TrackService} from '../track.service';
import {ActivatedRoute} from '@angular/router';
import {Code} from "../code";

@Component({
  selector: 'app-track-details',
  templateUrl: './track-details.component.html',
  styleUrls: ['./track-details.component.scss']
})
export class TrackDetailsComponent implements OnInit {

  track_id = 0;
  track: Track;
  workshops: Workshop[] = [];
  isDataLoaded = false;
  codeIndex = 0;
  code: Code;

  constructor(private trackService: TrackService,
              private route: ActivatedRoute) {
    this.route.params.subscribe( params =>
          this.track_id = params['id']);
  }

  ngOnInit() {
    this.trackService.getTrack(this.track_id).subscribe(
      (track) => {
        this.track = track;
        this.getCode(track.codes[this.codeIndex]);
      }
    );
  }

  prevCode() {
    if (this.codeIndex === 0) {
      return;
    } else {
      this.codeIndex--;
      this.getCode(this.track.codes[this.codeIndex]);
    }
  }


  nextCode() {
    if (this.codeIndex === this.track.codes.length - 1) {
      return;
    } else {
      this.codeIndex++;
      this.getCode(this.track.codes[this.codeIndex]);
    }
  }

  getCode(code: Code) {
    this.trackService.getCode(code).subscribe(
      (fullCode) => {this.code = fullCode; }
    );
    this.isDataLoaded = true;
  }

}
