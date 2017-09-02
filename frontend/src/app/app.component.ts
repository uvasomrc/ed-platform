import { Component, OnInit } from '@angular/core';
import {WorkshopService} from './workshop.service';
import {Workshop} from './workshop';
import {TrackService} from './track.service';
import {Track} from './track';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  workshops: Workshop[] = [];
  tracks: Track[] = [];

  constructor(private workshopService: WorkshopService,
              private trackService: TrackService) {}

  public ngOnInit() {
    this.workshopService.getAllWorkshops().subscribe(
        (workshops) => {
          this.workshops = workshops;
        }
      );

    this.trackService.getTracks().subscribe(
        (tracks) => {
          this.tracks = tracks;
        }
      );
  }

  onAddWorkshop(workshop) {
    this.workshopService
      .addWorkshop(workshop)
      .subscribe((newWorkshop) => {
        this.workshops = this.workshops.concat(newWorkshop);
      });
  }



}
