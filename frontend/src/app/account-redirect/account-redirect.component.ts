import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {AccountService} from '../account.service';
import {Participant} from '../participant';

@Component({
  selector: 'app-account-redirect',
  templateUrl: './account-redirect.component.html',
  styleUrls: ['./account-redirect.component.css']
})
export class AccountRedirectComponent implements OnInit {
  // Accepts a token from the server, then redirects the user
  // to the home page.  This allows single sign on through
  // Shibboleth.

  participant = new Participant();

  constructor(private account_service: AccountService,
              private route: ActivatedRoute,
              private router: Router) {
    this.route.params.subscribe(params => {
      account_service.login(params['token']).subscribe(p => {
        if (p.new_account) {
          this.router.navigate(['accountDetails']);
        } else {
          this.router.navigate([account_service.getRouteAfterLogin()]);
        }
      });
    });
  }

  ngOnInit() {}
}
