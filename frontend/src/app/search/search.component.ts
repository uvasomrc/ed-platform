import {Component, Input, OnInit} from '@angular/core';
import {Filter, Search} from '../search';
import {WorkshopService} from '../workshop.service';
import {FormControl, FormGroup} from '@angular/forms';
import {ActivatedRoute} from '@angular/router';
import {Workshop} from '../workshop';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {

  @Input()
  search: Search;

  date_range_display: string;

  showFilters = false;

  searchForm: FormGroup;
  searchBox: FormControl;
  loading = false;
  workshops: Workshop[];

  constructor(private workshopService: WorkshopService,
              private route: ActivatedRoute) {
    this.route.params.subscribe(params => {
      this.search = new Search();
      this.search.query = params['query'];
    });
  }

  ngOnInit() {
    this.setDateRange('future', 'Upcoming');
    this.doSearch();

    this.searchBox = new FormControl();
    this.searchForm = new FormGroup({
      searchBox: this.searchBox
    });

    this.searchBox.setValue(this.search.query);

    this.searchBox.valueChanges.subscribe(query => {
      this.search.query = query;
      this.doSearch();
    });

  }

  updateQuery(query) {
    this.search.query = query;
    this.doSearch();
  }

  doSearch() {
    this.workshopService.searchWorkshops(this.search).subscribe(
      (search) => {
        this.search = search;
        this.workshops = search.workshops;
        console.log('.... and done.');
      }
    );
  }

  onScroll() {
    console.log('Scrolled!');
    if (this.loading) { return; }
    if (this.workshops.length === this.search.total) {
      console.log('We found them all, not going to query again.');
      return;
    }
    console.log('finding workshops....');
    this.loading = true;
    const scrollSearch = this.search;
    scrollSearch.start = this.workshops.length;
    this.workshopService.searchWorkshops(scrollSearch).subscribe(
      (search) => {
        console.log('found ' + search.workshops.length + ' more workshops.');
        this.workshops = this.workshops.concat(search.workshops);
        console.log('There are now ' + this.workshops.length + ' workshops.');
        this.loading = false;
      }
    );
  }

  setDateRange(value, display) {
    this.search.date_restriction = value;
    this.date_range_display = display;
    this.showFilters = false;
    this.doSearch();
  }

  removeDateRange() {
    this.search.date_restriction = '';
    this.date_range_display = '';
    this.doSearch();
  }


  addFilter(field: string, value: string) {
    this.search.addFilter(field, value);
    this.showFilters = false;
    this.doSearch();
  }

  removeFilter(filter: Filter) {
    this.search.removeFilter(filter);
    this.showFilters = false;
    this.doSearch();
  }

}
