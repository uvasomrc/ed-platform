import {Component, OnInit} from '@angular/core';
import {Router, RoutesRecognized} from '@angular/router';
import {Participant} from './participant';
import {AccountService} from './account.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

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
    const current_url = this.router.routerState.snapshot.url;
    this.accountService.goLogin(current_url);
  }

  goLogout() {
    this.accountService.logout();
    this.router.navigate(['home']);
  }

}
