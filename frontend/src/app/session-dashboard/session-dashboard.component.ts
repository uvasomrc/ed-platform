import { Component, OnInit } from '@angular/core';
import {Participant} from '../participant';
import {Session} from '../session';
import {WorkshopService} from '../workshop.service';
import {ActivatedRoute} from '@angular/router';
import {EmailMessage} from '../EmailMessage';
import {Workshop} from '../workshop';

@Component({
  selector: 'app-session-dashboard',
  templateUrl: './session-dashboard.component.html',
  styleUrls: ['./session-dashboard.component.scss']
})
export class SessionDashboardComponent implements OnInit {

  account: Participant;
  session: Session;
  workshop: Workshop;
  session_id = 0;
  is_data_loaded = false;
  messages: EmailMessage[];
  selected_tab: number;
  is_sending = false;

  constructor(private workshopService: WorkshopService,
              private route: ActivatedRoute) {
    this.route.params.subscribe( params =>
      this.session_id = params['id']);
  }

  ngOnInit() {
    this.workshopService.getSession(this.session_id).subscribe(
      session => {
        this.session = session;
        this.workshopService.getWorkshopForSession(this.session).subscribe(
          workshop => {
            this.workshop = workshop;
            this.workshopService.getMessages(this.session).subscribe(
              messages => {
                this.messages = messages;
                this.is_data_loaded = true;
              });
          });
      }
    );
  }

  sendEmail(email) {
    this.is_sending = true;
    this.workshopService.emailParticipants(email, this.session).subscribe(
      message => {
        this.messages.push(message);
        this.selected_tab = 2;
        this.is_sending = false;
      }
    );
  }

}
