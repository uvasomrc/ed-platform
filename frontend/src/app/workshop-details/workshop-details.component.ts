import { Component, OnInit } from '@angular/core';
import {WorkshopService} from '../workshop.service';
import {ActivatedRoute, Router} from '@angular/router';
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
              private router: Router,
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

  isLoggedIn() {
    return this.accountService.isLoggedIn();
  }

  goLogin() {
    const current_url = this.router.routerState.snapshot.url;
    this.accountService.goLogin(current_url);
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
