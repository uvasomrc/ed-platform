import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {AccountService} from '../account.service';
import {Participant} from '../participant';


@Component({
  selector: 'app-account-details',
  templateUrl: './account-details.component.html',
  styleUrls: ['./account-details.component.css']
})
export class AccountDetailsComponent implements OnInit {

  participant = new Participant();

  constructor(private account_service: AccountService,
              private route: ActivatedRoute) {
    this.route.params.subscribe( params =>
      account_service.setToken(params['token']));
  }

  ngOnInit() {
    this.account_service.getAccount().subscribe(
      account => this.participant = account);
  }

}
