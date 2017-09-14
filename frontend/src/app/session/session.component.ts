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

  constructor() { }

  ngOnInit() {
  }
}
