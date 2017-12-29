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

  @Input('activeCode')
  activeCode: String;

  constructor(private router: Router) {}

  ngOnInit(): void {
    console.log(`the active code for Track is ${this.activeCode}`);
  }

  goTrack(id: Number) {
    this.router.navigate(['track', id]);
  }

}

