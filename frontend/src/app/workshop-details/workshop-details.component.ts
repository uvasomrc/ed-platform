import {Component, Inject, OnInit} from '@angular/core';
import {WorkshopService} from '../workshop.service';
import {ActivatedRoute, Router} from '@angular/router';
import {Workshop} from '../workshop';
import {AccountService} from '../account.service';
import {Track} from '../track';
import {Code} from '../code';
import {Participant} from '../participant';
import {Post} from '../post';
import {Session} from '../session';
import {MAT_DIALOG_DATA, MatDialog, MatDialogRef} from "@angular/material";

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
  post: Post;

  constructor(private workshopService: WorkshopService,
              private accountService: AccountService,
              private router: Router,
              private route: ActivatedRoute,
              private dialog: MatDialog) {
    this.route.params.subscribe(params => {
      this.workshop_id = params['id'];
      if ('code' in params) {
        const trackingCode = params['code'];
        const action = params['action'];
        const sessionId = params['sessionId']
        this.confirm_registration(action, trackingCode, sessionId);
      }
      this.load_workshop();
    });
    accountService.getAccount().subscribe(a => this.account = a);
  }

  follow() {
    this.workshopService.follow(this.workshop).subscribe(
    (workshop) => {
      this.workshop = workshop;
      (<any>window).gtag('event', this.workshop.title, {
        'event_category': 'follow'
      });
    });
  }

  unFollow() {
    this.workshopService.unFollow(this.workshop).subscribe(
      (workshop) => {
        this.workshop = workshop;
        (<any>window).gtag('event', this.workshop.title, {
          'event_category': 'unfollow'
        });
      });
  }

  onRegistrationChange(session) {
    this.workshopService.getWorkshop(this.workshop.id).subscribe(
      (workshop) => {
        this.workshop = workshop;
      });
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
        if (this.workshop.code_id !== null && this.workshop.code_id.length > 0) {
          this.workshopService.getCodeByString(this.workshop.code_id).subscribe(
            (code) => {
              this.code = code;
              this.updatedLoaded();
            });
        } else {
          this.code = new Code();
          this.updatedLoaded();
        }
        if (this.workshop.discourse_enabled) {
          this.workshopService.getPost(workshop).subscribe(
            (post) => {
              this.post = post;
            }
          );
        }

      });
    /**/
  }

  confirm_registration(action: String, trackingCode: String, sessionId: Number) {
    if (action.toLowerCase() === 'unfollow') {
      this.workshopService.unFollowByTrackingCode(trackingCode, this.workshop_id).subscribe(
        (workshop) => {
          this.workshop = workshop;
          const dialogRef = this.dialog.open(UnFollowDialogComponent, {
            width: '250px',
            data: { workshop: workshop}
          });
          (<any>window).gtag('event', this.workshop.title, {
            'event_category': 'unfollow_by_email_link'
          });
        }
      );
    }
    if (action.toLowerCase() === 'confirm') {
      this.workshopService.confirmRegistration(trackingCode, sessionId).subscribe(
        (session) => {
          console.log('You are confirmed for session:' + session);
          const dialogRef = this.dialog.open(ConfirmRegistrationDialogComponent, {
              width: '250px',
              data: { session: session}
          });
          (<any>window).gtag('event', this.workshop.title, {
            'event_category': 'confirm_by_email_link'
          });
        }
      );
    }
    if (action.toLowerCase() === 'decline') {
      this.workshopService.cancelRegistration(trackingCode, sessionId).subscribe(
        (session) => {
          console.log('You are no longer registered for session:' + session);
          const dialogRef = this.dialog.open(DeclineRegistrationDialogComponent, {
            width: '250px',
            data: { session: session}
          });
          (<any>window).gtag('event', this.workshop.title, {
            'event_category': 'cancel_by_email_link'
          });
        }
      );
    }
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

  displaySessions(): Session[] {
    return this.workshop.sessions.filter(s => !s.isPast());
  }

  availableSessions(): Session[] {
    return this.workshop.sessions.filter(s => !s.isPast() && !s.isFull());
  }

  attendedSession(): Session {
    return this.workshop.sessions.filter(s => s.status === 'ATTENDED' || s.status === 'AWAITING_REVIEW')[0];
  }

  goLogin() {
    const current_url = this.router.routerState.snapshot.url;
    this.accountService.goLogin(current_url);
  }

  goEdit() {
    this.router.navigate(['workshop-form', this.workshop.id]);
  }

  goWorkshopDashboard() {
    this.router.navigate(['workshopDashboard', this.workshop.id]);
  }

}


@Component({
  selector: 'app-un-follow-dialog',
  templateUrl: 'un-follow-dialog.html',
})
export class UnFollowDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: any) {}
}

@Component({
  selector: 'app-confirm-registration-dialog',
  templateUrl: 'confirm-registration-dialog.html',
})
export class ConfirmRegistrationDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: any) {}
}

@Component({
  selector: 'app-decline-registration-dialog',
  templateUrl: 'decline-registration-dialog.html',
})
export class DeclineRegistrationDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: any) {}
}
