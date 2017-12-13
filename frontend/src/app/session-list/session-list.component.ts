import {Component, Input, OnInit} from '@angular/core';
import {Session} from "../session";

@Component({
  selector: 'app-session-list',
  templateUrl: './session-list.component.html',
  styleUrls: ['./session-list.component.css']
})
export class SessionListComponent {

  @Input()
  sessions: Session[];

  constructor() {}
}
