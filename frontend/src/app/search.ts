import {Workshop} from './workshop';
export class Search {
 query: string;
 filters: Array<Filter>;
 total = 0;
 hits: Array<Workshop>;
 facets: Array<Facet>;

 constructor(values: Object= {}) {
   Object.assign(this, values);
   this.hits = new Array<Workshop>();
   if ('hits' in values) {
     for (const w of values['hits']) {
       this.hits.push(new Workshop(w));
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
     for (const f in values['filters']) {
       this.filters.push(new Filter(f));
     }
   }
 }

 addFilter(field: string, value: string) {
   let filter = new Filter();
   filter.field = field;
   filter.value = value;
   this.filters.push(filter);
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
