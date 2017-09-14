import {Component, OnDestroy, OnInit} from '@angular/core';
import {WorkshopService} from '../workshop.service';
import {TrackService} from '../track.service';
import {Track} from '../track';
import {Workshop} from '../workshop';
import {Router} from '@angular/router';
import {Subscription} from "rxjs/Subscription";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, OnDestroy {

  workshops: Workshop[] = [];
  tracks: Track[] = [];
  workshopSub: Subscription;
  trackSub: Subscription;

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


}
