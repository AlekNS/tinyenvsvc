import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PageNotFoundComponent } from './components/page-not-found.component';
import { MatCardModule, MatFormFieldModule, MatCommonModule, MatInputModule, MatButtonModule, MatToolbarModule, MatIconModule, MatTabsModule } from '@angular/material';
import { NavTopBarComponent } from './components/top-nav.component';

@NgModule({
  imports: [
    CommonModule,
    MatCommonModule,
    MatInputModule,
    MatCardModule,
    MatFormFieldModule,
    MatButtonModule,
    MatToolbarModule,
    MatIconModule,
  ],
  declarations: [PageNotFoundComponent,NavTopBarComponent],
  exports: [
    PageNotFoundComponent,
    NavTopBarComponent,
    MatCommonModule,
    MatInputModule,
    MatCardModule,
    MatFormFieldModule,
    MatButtonModule,
    MatToolbarModule,
    MatIconModule,
    MatTabsModule,
  ]
})
export class SharedModule { }
