import {Component, Input} from '@angular/core';
import {Workshop} from '../workshop';
import {Router} from '@angular/router';

@Component({
  selector: 'app-workshop',
  templateUrl: './workshop.component.html',
  styleUrls: ['./workshop.component.css']
})
export class WorkshopComponent  {

  @Input('workshop') workshop: Workshop;

  constructor(private router: Router) {}

  goWorkshop(id: Number) {
    this.router.navigate(['workshop', id]);
  }


}
