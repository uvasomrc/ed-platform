import {Component, Input, OnInit, Renderer2, ViewChild} from '@angular/core';
import {Filter, Search} from '../search';
import {WorkshopService} from '../workshop.service';
import {FormControl, FormGroup} from '@angular/forms';
import {ActivatedRoute} from '@angular/router';
import {Workshop} from '../workshop';
import {MatSidenav} from '@angular/material';
import 'rxjs/add/operator/debounceTime';

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

  @ViewChild('sidenav') public sideNav: MatSidenav;

  constructor(private workshopService: WorkshopService,
              private route: ActivatedRoute,
              private renderer: Renderer2) {
    this.route.params.subscribe(params => {
      this.search = new Search();
      if ('query' in params) {
        this.search.query = params['query'];
      } else {
        this.search.query = '';
      }
      this.search.query = params['query'];
    });
    renderer.listen(window, 'resize', (event) => {
      this.checkWindowWidth();
    });
  }

  private checkWindowWidth(): void {
    if (window.innerWidth > 768) {
      this.sideNav.mode = 'side';
      this.sideNav.opened = false;
    }else {
      this.sideNav.mode = 'over';
      this.sideNav.opened = false;
    }
  }

  ngOnInit() {
    this.doSearch();
    this.searchBox = new FormControl();
    this.searchForm = new FormGroup({
      searchBox: this.searchBox
    });

    this.searchBox.setValue(this.search.query);

    this.searchBox.valueChanges
      .debounceTime(300).subscribe(query => {
        this.search.query = query;
        this.doSearch();
    });

  }

  updateQuery(query) {
    this.search.query = query;
    this.search.start = 0;
    this.doSearch();
  }

  doSearch() {
    this.workshopService.searchWorkshops(this.search).subscribe(
      (search) => {
        console.log("Searching ...");
        this.search = search;
        this.workshops = search.workshops;
        this.checkWindowWidth();
      }
    );
  }

  onScroll() {
    console.log('Scrolled!');
    if (this.loading) { return; }

    if (this.workshops != null && this.workshops.length === this.search.total) {
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
