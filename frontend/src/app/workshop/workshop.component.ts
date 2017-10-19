import {Component, Input} from '@angular/core';
import {Workshop} from '../workshop';
import {Router} from '@angular/router';
import {AccountService} from '../account.service';

@Component({
  selector: 'app-workshop',
  templateUrl: './workshop.component.html',
  styleUrls: ['./workshop.component.scss']
})
export class WorkshopComponent  {

  @Input('workshop') workshop: Workshop;

  constructor(private router: Router,
              private accountService: AccountService) {}

  loggedIn() {
    return this.accountService.isLoggedIn();
  }

  goWorkshop() {
    this.router.navigate(['workshop', this.workshop.id]);
  }

  teacherDashboard() {
    const s = this.workshop.sessions.filter(s => s.instructing())[0];
    this.router.navigate(['teacherDashboard', s.id]);
  }


}
