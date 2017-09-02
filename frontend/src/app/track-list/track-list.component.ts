import {Component, Input, OnInit} from '@angular/core';
import {Track} from "../track";

@Component({
  selector: 'app-track-list',
  templateUrl: './track-list.component.html',
  styleUrls: ['./track-list.component.css']
})
export class TrackListComponent  {

  @Input()
  tracks: Track[];

  constructor() {}

}
