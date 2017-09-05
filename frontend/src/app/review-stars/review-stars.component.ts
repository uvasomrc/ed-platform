import {Component, Input, OnInit} from '@angular/core';
import {TimesPipe} from '../times.pipe';

@Component({
  selector: 'app-review-stars',
  templateUrl: './review-stars.component.html',
  styleUrls: ['./review-stars.component.css']
})
export class ReviewStarsComponent implements OnInit {

  @Input()
  score: Number;

  @Input()
  max_score: Number;

  constructor() { }

  ngOnInit() {
  }

  getStars(): Star[] {
    const stars = Array<Star>();
    for (let i = 1; i <= this.max_score; i++) {
      if (i <= this.score) {
        stars.push(new Star('star', 'on'));
      } else {
        stars.push(new Star('star', 'off'));
      }
    }
    return stars;
  }

}

class Star {
  constructor(public icon: string, public style: string){}
}
