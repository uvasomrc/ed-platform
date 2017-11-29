import {Workshop} from './workshop';
import {Participant} from './participant';
export class Search {
 query: string;
 filters: Array<Filter>;
 total = 0;
 workshops: Array<Workshop>;
 participants: Array<Participant>;
 facets: Array<Facet>;
 date_restriction: string;
 start = 0;
 size = 20;

 constructor(values: Object= {}) {
   Object.assign(this, values);
   this.workshops = new Array<Workshop>();
   if ('workshops' in values) {
     for (const w of values['workshops']) {
       this.workshops.push(new Workshop(w));
     }
   }
   this.participants = new Array<Participant>();
   if ('participants' in values) {
     for (const p of values['participants']) {
       this.participants.push(new Participant(p));
     }
   }
   this.facets = new Array<Facet>();
   if ('facets' in values) {
     for (const f in values['facets']) {
       this.facets.push(new Facet(f, values['facets'][f]));
     }
   }
   this.filters = new Array<Filter>();
   if ('filters' in values) {
     for (const f of values['filters']) {
       this.filters.push(new Filter(f));
     }
   }
 }

 addFilter(field: string, value: string) {
   const filter = new Filter();
   filter.field = field;
   filter.value = value;
   this.filters.push(filter);
 }

 removeFilter(filter: Filter) {
   const index: number = this.filters.indexOf(filter);
   if (index !== -1) {
     this.filters.splice(index, 1);
   }
 }

}

export class Filter {
  field: string;
  value: string;

  constructor(values: Object = {}) {
    Object.assign(this, values);
  }

}

class Facet {
  name: string;
  counts: Array<FacetCount>;

  constructor(name, counts) {
    this.name = name;
    this.counts = new Array<FacetCount>();
    for (const count of counts) {
      this.counts.push(new FacetCount(count));
    }
  }
}

class FacetCount {
  category: string;
  hit_count = 0;
  is_selected = false;

  constructor(values: Object = {}) {
    Object.assign(this, values);
  }
}
