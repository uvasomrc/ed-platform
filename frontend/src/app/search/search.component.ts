import {Component, Input, OnInit} from '@angular/core';
import {Filter, Search} from '../search';
import {WorkshopService} from '../workshop.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {

  @Input()
  search: Search;

  constructor(private workshopService: WorkshopService) { }

  ngOnInit() {
    this.search = new Search();
    this.doSearch('');
  }

  doSearch(query: string) {
    this.search.query = query;

    this.workshopService.searchWorkshops(this.search).subscribe(
      (search) => {
        this.search = search;
      }
    );
  }

  addFilter(field: string, value: string) {
    this.search.addFilter(field, value);
    this.doSearch(this.search.query);
  }

  removeFilter(filter: Filter) {
    this.search.removeFilter(filter);
    this.doSearch(this.search.query);
  }

}
