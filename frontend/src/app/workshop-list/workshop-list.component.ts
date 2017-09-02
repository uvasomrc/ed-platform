import {Component, Input} from '@angular/core';
import {Workshop} from '../workshop';

@Component({
  selector: 'app-workshop-list',
  templateUrl: './workshop-list.component.html',
  styleUrls: ['./workshop-list.component.css']
})
export class WorkshopListComponent  {

  @Input()
  workshops: Workshop[];

  constructor() {}
}
