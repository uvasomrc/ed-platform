import { Component, OnInit } from '@angular/core';
import {WorkshopService} from '../workshop.service';
import {ActivatedRoute, Router} from '@angular/router';
import {Workshop} from '../workshop';
import {AccountService} from "../account.service";
import {Track} from "../track";
import {Code} from "../code";
import {Participant} from "../participant";

@Component({
  selector: 'app-workshop-details',
  templateUrl: './workshop-details.component.html',
  styleUrls: ['./workshop-details.component.scss']
})
export class WorkshopDetailsComponent implements OnInit {

  workshop_id = 0;
  workshop: Workshop;
  tracks: Track[];
  isDataLoaded = false;
  code: Code;
  account: Participant;

  constructor(private workshopService: WorkshopService,
              private accountService: AccountService,
              private router: Router,
              private route: ActivatedRoute) {
    this.route.params.subscribe( params => {
      this.workshop_id = params['id'];
      this.load_workshop();
    });
    accountService.getAccount().subscribe(a => this.account = a);
  }

  load_workshop() {
    this.workshopService.getWorkshop(this.workshop_id).subscribe(
      (workshop) => {
        this.workshop = workshop;
        this.workshopService.getTracksForWorkshop(workshop).subscribe(
          (tracks) => {
            this.tracks = tracks;
            this.updatedLoaded();
          }
        );
        if (this.workshop.code_id !== '') {
          this.workshopService.getCodeByString(this.workshop.code_id).subscribe(
            (code) => {
              this.code = code;
              this.updatedLoaded();
            }
          );
        } else {
          this.code = new Code();
          this.updatedLoaded();
        }
      }
    );
  }

  ngOnInit() {
  }

  updatedLoaded() {
    if (this.workshop != null && this.tracks != null && this.code != null) {
      this.isDataLoaded = true;
    }
  }

  similarWorkshops(): Workshop[] {
    return this.code.workshops.filter(w => w.id !== this.workshop.id);
  }

  registerState(): String {
    if (this.workshop.instructing()) {
      return 'instructing';
    } else if (this.workshop.awaiting_review()) {
      return 'awaiting';
    } else if (this.workshop.registered()) {
      return 'registered';
    } else if (this.workshop.wait_listed()) {
      return 'wait_listed';
    } else if (this.workshop.hasUpcomingSession()) {
      if (this.workshop.sessions.length > 0 && this.workshop.nextSession().isFull()) {
        return 'full';
      } else if (this.isLoggedIn() && this.workshop.nextSession().isAvailable()) {
        return 'available';
      } else if (!this.isLoggedIn() && this.workshop.nextSession().isAvailable()) {
        return 'login';
      }
    }
  }

  isLoggedIn() {
    return this.accountService.isLoggedIn();
  }

  goLogin() {
    const current_url = this.router.routerState.snapshot.url;
    this.accountService.goLogin(current_url);
  }

  goTeacher() {
    this.router.navigate(['teacherDashboard', this.workshop.nextSession().id]);
  }

  goEdit() {
    this.router.navigate(['workshop-form', this.workshop.id]);
  }

  register() {
    const session = this.workshop.nextSession();
    this.accountService.register(session).subscribe(
      (newSession) => {
        this.workshop.replaceSession(newSession);
      });
  }

  unRegister() {
    const session = this.workshop.nextSession();
    this.accountService.unRegister(session).subscribe(
      (newSession) => {
        this.workshop.replaceSession(newSession);
      });
  }


}
