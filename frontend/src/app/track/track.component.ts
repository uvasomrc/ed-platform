import {Component, Input, OnInit} from '@angular/core';
import {TrackService} from "../track.service";
import {Track} from "../track";

@Component({
  selector: 'app-track',
  templateUrl: './track.component.html',
  styleUrls: ['./track.component.css']
})
export class TrackComponent implements OnInit {

  @Input('track') track: Track;

  ngOnInit(): void {
    console.log(`my Track is ${this.track}`);
  }

}

