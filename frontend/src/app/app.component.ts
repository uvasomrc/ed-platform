import {Component, Inject, OnInit} from '@angular/core';
import {NavigationEnd, Router, RoutesRecognized} from '@angular/router';
import {Participant} from './participant';
import {AccountService} from './account.service';
import {environment} from "../environments/environment";
import {MAT_DIALOG_DATA, MatDialog} from "@angular/material";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  account: Participant;
  title: String;
  loggedIn = false;
  ga_id = environment.ga_id;

  constructor(private router: Router,
              private accountService: AccountService,
              private dialog: MatDialog) {
    router.events.subscribe(event => {
      if (event instanceof RoutesRecognized) {
        const route = event.state.root.firstChild;
        this.title = route.data.title || '';
        console.log('Title', this.title);
      }

      // For google Analytics tracking of page views through the router
      if (event instanceof NavigationEnd ) {
        (<any>window).gtag('config', this.ga_id, {'page_path': event.urlAfterRedirects});
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

  goSearch($event) {
    $event.preventDefault();
    this.router.navigate(['search']);
  }

  goHome($event) {
    $event.preventDefault();
    this.router.navigate(['home']);
  }

  goAbout($event) {
    $event.preventDefault();
    this.router.navigate(['about']);
  }

  goHelp($event) {
    $event.preventDefault();
    this.router.navigate(['help']);
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

  showEmailAddresses() {
    this.accountService.getEmailAddresses().subscribe(addresses => {
      var modal = this.dialog.open(EmailListDialogComponent, {
        width: '500px',
        data: {email_addresses: addresses}
      });
    });
  }


}


@Component({
  selector: 'app-email-list-dialog',
  templateUrl: 'email-list-dialog.html',
})
export class EmailListDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: any) {}
}
