import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
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
              private route: ActivatedRoute,
              private router: Router) {
    this.route.params.subscribe( params =>
      account_service.login(params['token']));
      this.router.navigate(['home']);
  }

  ngOnInit() {}

}
