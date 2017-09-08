import {Component, OnDestroy, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {environment} from '../environments/environment';
import {Participant} from './participant';
import {AccountService} from './account.service';
import {Subscription} from 'rxjs/Subscription';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnDestroy {

  login_url = environment.api + '/api/login';
  user: Participant;
  userSubscription: Subscription;

  constructor(private router: Router,
              private accountService: AccountService) {
    this.userSubscription = this.accountService.getCurrentUser().subscribe(
      participant => {
        this.user = participant;
      });
    this.accountService.refreshUser();
  }

  ngOnDestroy() {
    this.userSubscription.unsubscribe();
  }

  goHome() {
    this.router.navigate(['home']);
  }

  goLogin() {
    window.location.href = this.login_url;
  }

}
