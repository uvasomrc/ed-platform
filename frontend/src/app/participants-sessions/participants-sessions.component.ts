import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Session} from "../session";
import {OuterSubscriber} from "rxjs/OuterSubscriber";

@Component({
  selector: 'app-participants-sessions',
  templateUrl: './participants-sessions.component.html',
  styleUrls: ['./participants-sessions.component.css']
})
export class ParticipantsSessionsComponent implements OnInit {

  @Input()
  session: Session;

  @Output()
  unRegister: EventEmitter<Session> = new EventEmitter();

  constructor() { }

  ngOnInit() {
  }

  removeSession() {
    this.unRegister.emit(this.session);
  }

}
