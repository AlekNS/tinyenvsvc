import { Component } from '@angular/core';

@Component({
  selector: 'app-nav-top-bar',
  template: `
<div>
<mat-toolbar color="primary" style="width: 100%">
  <div style="width:960px; margin: 0 auto">
    <mat-toolbar-row>
      <span>TEService</span>
      <span style="flex: 1"></span>
      <button mat-button>
        <mat-icon>logout</mat-icon>
        Logout
      </button>
    </mat-toolbar-row>
  </div>
</mat-toolbar>
</div>
`,
})
export class NavTopBarComponent {

}
