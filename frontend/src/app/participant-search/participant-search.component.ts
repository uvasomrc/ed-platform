import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {AccountService} from '../account.service';
import {Participant} from '../participant';
import {Search} from '../search';
import {FormControl, FormGroup} from "@angular/forms";


@Component({
  selector: 'app-participant-search',
  templateUrl: './participant-search.component.html',
  styleUrls: ['./participant-search.component.scss']
})
export class ParticipantSearchComponent implements OnInit {

  @Input()
  search = new Search();

  @Output()
  selected: EventEmitter<Participant> = new EventEmitter();

  searchForm: FormGroup;
  searchBox: FormControl;

  constructor(private accountService: AccountService) { }

  ngOnInit() {
    this.searchBox = new FormControl();
    this.searchForm = new FormGroup({
      searchBox: this.searchBox
    });

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
    this.accountService.search(this.search).subscribe( search => {
      this.search = search;
    });
  }

  select(p: Participant) {
    console.log(`Selected ${p.display_name}`);
    this.selected.next(p);
  }
}
