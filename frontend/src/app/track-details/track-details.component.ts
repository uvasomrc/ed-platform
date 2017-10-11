import {Component, OnInit, SecurityContext} from '@angular/core';
import {Track} from '../track';
import {Workshop} from '../workshop';
import {TrackService} from '../track.service';
import {ActivatedRoute} from '@angular/router';
import {MatIconRegistry} from '@angular/material';
import {DomSanitizer} from '@angular/platform-browser';

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

  constructor(private trackService: TrackService,
              private route: ActivatedRoute,
              private iconRegistry: MatIconRegistry,
              private sanitizer: DomSanitizer) {
    this.route.params.subscribe( params =>
          this.track_id = params['id']);
    iconRegistry.addSvgIcon('progress-next',
        sanitizer.bypassSecurityTrustResourceUrl('/assets/tiny_arrow.svg'));
    iconRegistry.addSvgIcon('complete',
      sanitizer.bypassSecurityTrustResourceUrl('/assets/complete.svg'));
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
