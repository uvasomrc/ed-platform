import {Component, OnInit} from '@angular/core';
import {WorkshopService} from '../workshop.service';
import {ActivatedRoute, Router} from '@angular/router';
import {Workshop} from '../workshop';
import {AccountService} from '../account.service';
import {Track} from '../track';
import {Code} from '../code';
import {Participant} from '../participant';
import {Post} from '../post';
import {Session} from '../session';

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
              private route: ActivatedRoute) {
    this.route.params.subscribe(params => {
      this.workshop_id = params['id'];
      this.load_workshop();
    });
    accountService.getAccount().subscribe(a => this.account = a);
  }

  follow() {
    this.workshopService.follow(this.workshop).subscribe(
    (workshop) => {
      this.workshop = workshop;
    });
  }

  unFollow() {
    this.workshopService.unFollow(this.workshop).subscribe(
      (workshop) => {
        this.workshop = workshop;
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




}
