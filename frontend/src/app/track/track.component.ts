import {Component, Input, OnInit, ViewEncapsulation} from '@angular/core';
import {Track} from '../track';
import {Router} from "@angular/router";


@Component({
  selector: 'app-track',
  templateUrl: './track.component.html',
  styleUrls: ['./track.component.scss'],
  encapsulation: ViewEncapsulation.Emulated
})
export class TrackComponent implements OnInit {

  @Input('track') track: Track;

  constructor(private router: Router) {}

  ngOnInit(): void {
    console.log(`my Track is ${this.track}`);
  }

  goTrack(id: Number) {
    this.router.navigate(['track', id]);
  }

}

