import {Component, EventEmitter, OnDestroy, OnInit, Output} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {AccountService} from '../account.service';
import {Participant} from '../participant';
import {Session} from '../session';


@Component({
  selector: 'app-account-details',
  templateUrl: './account-details.component.html',
  styleUrls: ['./account-details.component.scss']
})
export class AccountDetailsComponent implements OnInit {

  account: Participant;
  isDataLoaded = false;

  constructor(private accountService: AccountService) {}

  ngOnInit() {
    this.accountService.getAccount().subscribe(acct => {
      this.account = acct;
      this.isDataLoaded = true;
    });
    this.accountService.refreshAccount();
  }

}
