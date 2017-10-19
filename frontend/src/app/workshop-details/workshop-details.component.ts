import { Component, OnInit } from '@angular/core';
import {WorkshopService} from '../workshop.service';
import {ActivatedRoute} from '@angular/router';
import {Workshop} from '../workshop';
import {AccountService} from "../account.service";

@Component({
  selector: 'app-workshop-details',
  templateUrl: './workshop-details.component.html',
  styleUrls: ['./workshop-details.component.scss']
})
export class WorkshopDetailsComponent implements OnInit {

  workshop_id = 0;
  workshop: Workshop;
  isDataLoaded = false;

  constructor(private workshopService: WorkshopService,
              private accountService: AccountService,
              private route: ActivatedRoute) {
    this.route.params.subscribe( params =>
      this.workshop_id = params['id']);
  }

  ngOnInit() {
    this.workshopService.getWorkshop(this.workshop_id).subscribe(
      (workshop) => {
        this.workshop = workshop;
        this.isDataLoaded = true;
      }
    );
  }

  register() {
    const session = this.workshop.nextSession();
    this.accountService.register(session).subscribe(
      (newSession) => {
        this.workshop.replaceSession(newSession);
      });
  }

  unRegister() {
    const session = this.workshop.nextSession();
    this.accountService.unRegister(session).subscribe(
      (newSession) => {
        this.workshop.replaceSession(newSession);
      });
  }


}
