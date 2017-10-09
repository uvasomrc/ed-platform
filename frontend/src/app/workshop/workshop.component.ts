import {Component, Input} from '@angular/core';
import {Workshop} from '../workshop';
import {Router} from '@angular/router';

@Component({
  selector: 'app-workshop',
  templateUrl: './workshop.component.html',
  styleUrls: ['./workshop.component.scss']
})
export class WorkshopComponent  {

  @Input('workshop') workshop: Workshop;

  constructor(private router: Router) {}

  goWorkshop() {
    this.router.navigate(['workshop', this.workshop.id]);
  }

  background() {
    return `url(${this.workshop.links.image})`;
  }
}
