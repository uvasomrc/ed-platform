import { Component, OnInit } from '@angular/core';
import {EmailMessage} from "../EmailMessage";
import {Participant} from "../participant";
import {Workshop} from "../workshop";
import {FormControl, FormGroup} from "@angular/forms";
import {ActivatedRoute} from "@angular/router";
import {WorkshopService} from "../workshop.service";

@Component({
  selector: 'app-workshop-dashboard',
  templateUrl: './workshop-dashboard.component.html',
  styleUrls: ['./workshop-dashboard.component.scss']
})
export class WorkshopDashboardComponent implements OnInit {

  account: Participant;
  workshop_id: number;
  workshop: Workshop;
  is_data_loaded = false;
  messages: EmailMessage[];
  is_sending= false;
  selected_tab: number;

  constructor(private workshopService: WorkshopService,
              private route: ActivatedRoute) {
    this.route.params.subscribe( params =>
      this.workshop_id = params['id']);
  }

  ngOnInit() {
    this.workshopService.getWorkshop(this.workshop_id).subscribe(
      workshop => {
        this.workshop = workshop;
        this.workshopService.getFollowEmails(this.workshop).subscribe(
          emails => {
            this.messages = emails;
            this.is_data_loaded = true;
          });
      }
    );
  }

  sendEmail(email) {
    this.is_sending = true;
    this.workshopService.emailFollowers(email, this.workshop).subscribe(
      message => {
        this.messages.push(message);
        this.selected_tab = 2;
        this.is_sending = false;
      }
    );
  }


}
