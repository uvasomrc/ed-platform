import {Component, Input, OnInit} from '@angular/core';
import {MatIconRegistry} from '@angular/material';
import {DomSanitizer} from '@angular/platform-browser';
import {Track} from '../track';

@Component({
  selector: 'app-track-progress',
  templateUrl: './track-progress.component.html',
  styleUrls: ['./track-progress.component.scss']
})
export class TrackProgressComponent implements OnInit {

  @Input('track')
  track: Track;

  @Input('codeIndex')
  codeIndex = -1;


  constructor(private iconRegistry: MatIconRegistry,
              private sanitizer: DomSanitizer) {
    iconRegistry.addSvgIcon('progress-next',
      sanitizer.bypassSecurityTrustResourceUrl('/assets/track/tiny_arrow.svg'));
    iconRegistry.addSvgIcon('connector',
      sanitizer.bypassSecurityTrustResourceUrl('/assets/track/connector.svg'));
    iconRegistry.addSvgIcon('connector-blank',
      sanitizer.bypassSecurityTrustResourceUrl('/assets/track/connector_blank.svg'));
    iconRegistry.addSvgIcon('circle-open',
      sanitizer.bypassSecurityTrustResourceUrl('/assets/track/circle_open.svg'));
    iconRegistry.addSvgIcon('circle-full',
      sanitizer.bypassSecurityTrustResourceUrl('/assets/track/circle_full.svg'));
    iconRegistry.addSvgIcon('checked',
      sanitizer.bypassSecurityTrustResourceUrl('/assets/track/checked.svg'));
  }

  ngOnInit() {
  }

}
