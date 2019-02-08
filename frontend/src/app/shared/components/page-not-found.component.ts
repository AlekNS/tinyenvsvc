import { Component } from '@angular/core';

interface PartialResponse {
  status(code: number): this;
}

@Component({
  selector: 'app-page-not-found',
  template: '<h1>Page Not Found</h1>',
})
export class PageNotFoundComponent { }
