import {Component, Input, OnInit} from '@angular/core';
import {Workshop} from "../workshop";

@Component({
  selector: 'app-workshop',
  templateUrl: './workshop.component.html',
  styleUrls: ['./workshop.component.css']
})
export class WorkshopComponent implements OnInit {

  @Input('workshop') workshop: Workshop;

  ngOnInit(): void {
    console.log(`my Workshop is ${this.workshop}`);
  }
}
