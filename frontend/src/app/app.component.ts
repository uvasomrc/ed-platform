import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router, RoutesRecognized} from '@angular/router';
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
  title: String;

  constructor(private router: Router,
              private accountService: AccountService) {
    router.events.subscribe(event => {
      if (event instanceof RoutesRecognized) {
        const route = event.state.root.firstChild;
        this.title = route.data.title || '';
        console.log('Title', this.title);
      }
    });
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

  goLogin() {
    window.location.href = this.login_url;
  }

  goLogout() {
    this.accountService.logout();
    this.router.navigate(['home']);
  }

}
