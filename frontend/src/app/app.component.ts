import { Component } from '@angular/core';
import {Http} from "@angular/http";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app works!';
  apiRoot: string = 'http://localhost:5000';

  constructor(private http: Http) {
  }

  doGET() {
    console.log("GET");
    let url = `${this.apiRoot}/track`;
    this.http.get(url).subscribe(res => console.log(res.json()));
  }

}
