import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Session} from "../session";

@Component({
  selector: 'app-session-list',
  templateUrl: './session-list.component.html',
  styleUrls: ['./session-list.component.css']
})
export class SessionListComponent {

  @Input()
  sessions: Session[];

  @Output()
  registerEvent: EventEmitter<Session> = new EventEmitter();

  onRegistrationChange(session: Session) {
    this.registerEvent.emit(session);
  }

  constructor() {}
}
