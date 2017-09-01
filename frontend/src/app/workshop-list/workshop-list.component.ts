import { Component, OnInit } from '@angular/core';
import {Workshop} from "../workshop";
import {WorkshopService} from "../workshop.service";
import {Observable} from "rxjs/Observable";

@Component({
  selector: 'app-workshop-list',
  templateUrl: './workshop-list.component.html',
  styleUrls: ['./workshop-list.component.css']
})
export class WorkshopListComponent implements OnInit {

  workshopService: WorkshopService;
  workshops: Observable<Workshop[]>;

  constructor(workshopService: WorkshopService) {
    this.workshopService = workshopService;
  }

  ngOnInit() {
    this.workshops = this.workshopService.getWorkshops();
  }

}
