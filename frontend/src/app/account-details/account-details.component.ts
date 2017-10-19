import {Component, EventEmitter, OnDestroy, OnInit, Output} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {AccountService} from '../account.service';
import {Participant} from '../participant';
import {Session} from '../session';
import {Workshop} from "../workshop";


@Component({
  selector: 'app-account-details',
  templateUrl: './account-details.component.html',
  styleUrls: ['./account-details.component.scss']
})
export class AccountDetailsComponent implements OnInit {

  account: Participant;
  workshops: Workshop[];
  isDataLoaded = false;

  constructor(private accountService: AccountService) {}

  ngOnInit() {
    this.accountService.getAccount().subscribe(acct => {
      this.account = acct;
      this.accountService.getWorkshopsForParticipant(acct).subscribe(ws => {
        this.workshops = ws;
        this.isDataLoaded = true;
      });

    });
    this.accountService.refreshAccount();
  }

  upcomingWorkshops() {
    return this.workshops.filter(ws => ws.registered())
  }

  pastWorkshops() {
    return this.workshops.filter(ws => ws.attended())
  }

  instructingWorkshops() {
    return this.workshops.filter(ws => ws.instructing())
  }


}
