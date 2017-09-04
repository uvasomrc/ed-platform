import { Component, OnInit } from '@angular/core';
import {WorkshopService} from "../workshop.service";
import {TrackService} from "../track.service";
import {Track} from "../track";
import {Workshop} from "../workshop";
import {Router} from "@angular/router";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  workshops: Workshop[] = [];
  tracks: Track[] = [];

  constructor(private workshopService: WorkshopService,
              private trackService: TrackService,
              private router: Router) {}

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
