import {Component, Input, OnInit, ViewEncapsulation} from '@angular/core';
import {Track} from '../track';


@Component({
  selector: 'app-track',
  templateUrl: './track.component.html',
  styleUrls: ['./track.component.css'],
  encapsulation: ViewEncapsulation.Emulated
})
export class TrackComponent implements OnInit {

  @Input('track') track: Track;

  ngOnInit(): void {
    console.log(`my Track is ${this.track}`);
  }

}

