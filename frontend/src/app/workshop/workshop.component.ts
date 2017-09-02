import {Component, Input} from '@angular/core';
import {Workshop} from '../workshop';

@Component({
  selector: 'app-workshop',
  templateUrl: './workshop.component.html',
  styleUrls: ['./workshop.component.css']
})
export class WorkshopComponent  {

  @Input('workshop') workshop: Workshop;

}
