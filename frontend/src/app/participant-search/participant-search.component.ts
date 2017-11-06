import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {AccountService} from '../account.service';
import {Participant} from '../participant';
import {Search} from '../search';


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

  constructor(private accountService: AccountService) { }

  ngOnInit() {
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
