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

  @Input()
  date_range_display: string;

  constructor(private workshopService: WorkshopService) { }

  ngOnInit() {
    this.search = new Search();
    this.doSearch();
  }

  updateQuery(query) {
    this.search.query = query;
    this.doSearch();
  }

  doSearch() {
    this.workshopService.searchWorkshops(this.search).subscribe(
      (search) => {
        this.search = search;
      }
    );
  }

  setDateRange(value, display) {
    this.search.date_restriction = value;
    this.date_range_display = display;
    this.doSearch();
  }

  removeDateRange() {
    this.search.date_restriction = '';
    this.date_range_display = '';
    this.doSearch();
  }


  addFilter(field: string, value: string) {
    this.search.addFilter(field, value);
    this.doSearch();
  }

  removeFilter(filter: Filter) {
    this.search.removeFilter(filter);
    this.doSearch();
  }

}
