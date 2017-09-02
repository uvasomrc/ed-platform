import { Component, OnInit } from '@angular/core';
import {WorkshopService} from './workshop.service';
import {Workshop} from './workshop';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  workshops: Workshop[] = [];

  constructor(private workshopService: WorkshopService) {}

  public ngOnInit() {
    this.workshopService
      .getAllWorkshops()
      .subscribe(
        (workshops) => {
          this.workshops = workshops;
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
