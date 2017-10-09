import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {environment} from '../environments/environment';
import {Participant} from './participant';
import {AccountService} from './account.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  login_url = environment.api + '/api/login';
  account: Participant;

  constructor(private router: Router,
              private accountService: AccountService) {
  }

  ngOnInit() {
    this.accountService.getAccount().subscribe(acct => {
      this.account = acct;
    });
    this.accountService.refreshAccount();
  }

  goSearch() {
    this.router.navigate(['search']);
  }

  goHome() {
    this.router.navigate(['home']);
  }

  goLogin() {
    window.location.href = this.login_url;
  }

  goLogout() {
    this.accountService.logout();
    this.router.navigate(['home']);
  }

  goAccount() {
    this.router.navigate(['accountDetails']);
  }

}
