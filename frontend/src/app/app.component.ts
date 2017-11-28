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
  loggedIn = false;

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
      console.log('Account Updated');
      this.account = acct;
      if (this.account === null) {  this.loggedIn = false; }
      else { this.loggedIn = true; }
    });
    this.accountService.refreshAccount();
  }

  goSearch() {
    this.router.navigate(['search', '']);
  }

  goHome() {
    this.router.navigate(['home']);
  }

  goAbout() {
    //fixme: should go to about page.
    this.router.navigate(['home']);
  }

  goHelp() {
    //fixme: should go to about page.
    this.router.navigate(['home']);
  }

  goParticipantEditor() {
    this.router.navigate(['participant-form', 0 ]);
  }

  goWorkshopEditor() {
    this.router.navigate(['workshop-form', 0 ]);
  }

  goTrackEditor() {
    this.router.navigate(['track-form', 0 ]);
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
