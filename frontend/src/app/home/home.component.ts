import {Component, OnDestroy, OnInit} from '@angular/core';
import {WorkshopService} from '../workshop.service';
import {TrackService} from '../track.service';
import {Track} from '../track';
import {Workshop} from '../workshop';
import {Router} from '@angular/router';
import {Subscription} from 'rxjs/Subscription';
import { trigger, state, style, transition, animate, keyframes, query, stagger } from '@angular/animations';
import {Participant} from '../participant';
import {AccountService} from '../account.service';
import {Search} from "../search";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {

  featuredWorkshops: Workshop[] = [];
  tracks: Track[] = [];
  showControls = false;
  account: Participant;

  constructor(private workshopService: WorkshopService,
              private trackService: TrackService,
              private router: Router,
              private accountService: AccountService) {}

  public ngOnInit() {
    this.workshopService.getFeaturedWorkshops().subscribe(
      (results) => {
        this.featuredWorkshops = results;
      }
    );
    this.trackService.getTracks().subscribe(
      (tracks) => {
        this.tracks = tracks;
      }
    );
    this.accountService.getAccount().subscribe(acct => {
      this.account = acct;
    });
    this.showControls = true;
  }

  goSearch(query) {
    this.router.navigate(['search', query]);
  }

  goNewTrack() {
    this.router.navigate(['track-form', 0]);
  }

  goNewWorkshop() {
    this.router.navigate(['workshop-form', 0]);
  }

}
