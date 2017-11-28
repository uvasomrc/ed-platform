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
  animations: [
  /*
    trigger('slide', [
      state('left', style({ transform: 'translateX(0)' })),
      state('right', style({ transform: 'translateX(-50%)' })),
      transition('* => *', animate(300))
    ])
*/
    trigger('slide', [
      state('1', style({ transform: 'translateX(-50px)' })),
      state('2', style({ transform: 'translateX(-300px)' })),
      state('3', style({ transform: 'translateX(-580px)' })),
      state('4', style({ transform: 'translateX(-800px)' })),
      state('5', style({ transform: 'translateX(-920px)' })),
      transition('* => *', animate(300))
    ])
  ]
})
export class HomeComponent implements OnInit {

  workshops: Workshop[] = [];
  tracks: Track[] = [];
  sponsors: Sponsor[] = [];
  showControls = false;
  sponsor_index = 1;
  sponsor_state = '1';
  account: Participant;

  constructor(private workshopService: WorkshopService,
              private trackService: TrackService,
              private router: Router,
              private accountService: AccountService) {}

  public ngOnInit() {
    const search = new Search();
    search.date_restriction = "30days";
    this.workshopService.searchWorkshops(search).subscribe(
      (results) => {
        this.workshops = results.workshops;
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
    this.setSponsors();
    this.showControls = true;
  }

  goSearch(query) {
    this.router.navigate(['search', query]);
  }

  setSponsors() {
    this.sponsors.push(new Sponsor('../../assets/sponsors/uva-info-tech.png', 'hidden'));
    this.sponsors.push(new Sponsor('../../assets/sponsors/uva-adcs.png', 'hidden'));
    this.sponsors.push(new Sponsor('../../assets/sponsors/uva_somrc_logo.png', 'visible'));
    this.sponsors.push(new Sponsor('../../assets/sponsors/uva-library.png', 'hidden'));
    this.sponsors.push(new Sponsor('../../assets/sponsors/bio-connector.png', 'hidden'));
  }

  left() {
    if (this.sponsor_index <= 1) { return; }
    this.sponsor_index = this.sponsor_index - 1;
    this.sponsor_state = this.sponsor_index.toString();
  }

  right() {
    if (this.sponsor_index >= 5) { return; }
    this.sponsor_index = this.sponsor_index + 1;
    this.sponsor_state = this.sponsor_index.toString();
  }

  goNewTrack() {
    this.router.navigate(['track-form', 0]);
  }

  goNewWorkshop() {
    this.router.navigate(['workshop-form', 0]);
  }

}

class Sponsor {
  constructor(public image: String, public style: String) {}
}
