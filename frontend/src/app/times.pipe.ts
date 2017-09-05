import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'times'
})
export class TimesPipe implements PipeTransform {
  // Returns an array containing the given number of values.
  transform(value: Number, args?: any): any {
    return (new Array(value)).fill(1);
  }
}
