import { Injectable } from '@angular/core';
import { Router, CanActivate} from '@angular/router';
import {AccountService} from './account.service';

@Injectable()
export class AuthGuard implements CanActivate {

  constructor(private router: Router,
              private accountService: AccountService) {}

  canActivate() {
    if (this.accountService.isLoggedIn()) {
      console.log('You may view stuffs.');
      return true;
    }

    // not logged in so redirect to home page
    this.router.navigate(['home']);
    return false;
  }

  /*
  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {
    return true;
  }
  */
}

