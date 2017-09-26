import {Component, OnDestroy, OnInit} from '@angular/core';
import {WorkshopService} from '../workshop.service';
import {TrackService} from '../track.service';
import {Track} from '../track';
import {Workshop} from '../workshop';
import {Router} from '@angular/router';
import {Subscription} from 'rxjs/Subscription';
import { trigger, state, style, transition, animate, keyframes, query, stagger } from '@angular/animations';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  animations: [
  /*
    trigger('slide', [
      state('left', style({ transform: 'translateX(0)' })),
      state('right', style({ transform: 'translateX(-50%)' })),
      transition('* => *', animate(300))
    ])
*/
    trigger('slide', [
      state('1', style({ transform: 'translateX(0)' })),
      state('2', style({ transform: 'translateX(-300px)' })),
      state('3', style({ transform: 'translateX(-560px)' })),
      state('4', style({ transform: 'translateX(-800px)' })),
      state('5', style({ transform: 'translateX(-920px)' })),
      transition('* => *', animate(300))
    ])
  ]
})
export class HomeComponent implements OnInit, OnDestroy {

  workshops: Workshop[] = [];
  tracks: Track[] = [];
  workshopSub: Subscription;
  trackSub: Subscription;
  sponsors: Sponsor[] = [];
  showControls = false;
  sponsor_index = 3;
  sponsor_state = '3';

  constructor(private workshopService: WorkshopService,
              private trackService: TrackService,
              private router: Router) {}

  public ngOnInit() {
    this.workshopSub = this.workshopService.getAllWorkshops().subscribe(
      (workshops) => {
        this.workshops = workshops;
      }
    );

    this.trackSub = this.trackService.getTracks().subscribe(
      (tracks) => {
        this.tracks = tracks;
      }
    );

    this.setSponsors();
    this.showControls = true;
  }

  setSponsors() {
    this.sponsors.push(new Sponsor('../../assets/sponsors/uva-info-tech.png', 'hidden'));
    this.sponsors.push(new Sponsor('../../assets/sponsors/uva-adcs.png', 'hidden'));
    this.sponsors.push(new Sponsor('../../assets/sponsors/uva_somrc_logo.png', 'visible'));
    this.sponsors.push(new Sponsor('../../assets/sponsors/uva-library.png', 'hidden'));
    this.sponsors.push(new Sponsor('../../assets/sponsors/bio-connector.png', 'hidden'));
  }

  public ngOnDestroy() {
    this.workshopSub.unsubscribe();
    this.trackSub.unsubscribe();
  }

  onAddWorkshop(workshop) {
    this.workshopService
      .addWorkshop(workshop)
      .subscribe((newWorkshop) => {
        this.workshops = this.workshops.concat(newWorkshop);
      });
  }

  left() {
    if (this.sponsor_index <= 1) { return; }
    console.log('sponsor state ' + this.sponsor_state);
    this.sponsor_index = this.sponsor_index - 1;
    this.sponsor_state = this.sponsor_index.toString();
  }

  right() {
    if (this.sponsor_index >= 5) { return; }
    console.log('sponsor state ' + this.sponsor_state);
    this.sponsor_index = this.sponsor_index + 1;
    this.sponsor_state = this.sponsor_index.toString();
  }
}

class Sponsor {
  constructor(public image: String, public style: String) {}
}
