import {Component, Input, OnInit} from '@angular/core';
import {Session} from '../session';
import {Participant} from '../participant';

@Component({
  selector: 'app-session',
  templateUrl: './session.component.html',
  styleUrls: ['./session.component.css']
})
export class SessionComponent implements OnInit {

  @Input()
  session: Session;
  instructor: Participant;

  constructor() { }

  ngOnInit() {
      this.instructor = this.session.participant_sessions.filter(
        ps => ps.is_instructor)[0].participant;
  }
}
