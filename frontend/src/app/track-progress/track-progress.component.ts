import { Component, OnInit } from '@angular/core';
import {MatIconRegistry} from "@angular/material";
import {DomSanitizer} from "@angular/platform-browser";

@Component({
  selector: 'app-track-progress',
  templateUrl: './track-progress.component.html',
  styleUrls: ['./track-progress.component.scss']
})
export class TrackProgressComponent implements OnInit {

  constructor(private iconRegistry: MatIconRegistry,
              private sanitizer: DomSanitizer) {
    iconRegistry.addSvgIcon('progress-next',
      sanitizer.bypassSecurityTrustResourceUrl('/assets/tiny_arrow.svg'));
    iconRegistry.addSvgIcon('complete',
      sanitizer.bypassSecurityTrustResourceUrl('/assets/complete.svg'));
  }

  ngOnInit() {
  }

}
