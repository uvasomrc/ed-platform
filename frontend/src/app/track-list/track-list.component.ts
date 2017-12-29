import {Component, Input, OnInit} from '@angular/core';
import {Track} from "../track";

@Component({
  selector: 'app-track-list',
  templateUrl: './track-list.component.html',
  styleUrls: ['./track-list.component.css']
})
export class TrackListComponent implements OnInit {

  @Input()
  tracks: Track[];

  @Input()
  activeCode: String;

  constructor() {}

  ngOnInit() {
    console.log(`the active code for list is ${this.activeCode}`);
  }

}
