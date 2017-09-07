import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import {environment} from '../environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  login_url = environment.api + '/api/login';

  constructor(private router: Router) {}

  goHome() {
    this.router.navigate(['home']);
  }

  goLogin() {
    window.location.href = this.login_url;
  }

}
