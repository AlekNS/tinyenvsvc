import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardRoutingModule } from './dashboard-routing.module';
import { DashboardComponent } from './components/dashboard.component';
import { SharedModule } from '../shared/shared.module';
import { HomeComponent } from './components/home.component';
import { UploadsComponent } from './components/uploads.component';

@NgModule({
  declarations: [
    DashboardComponent,
    HomeComponent,
    UploadsComponent,
  ],
  imports: [
    CommonModule,
    DashboardRoutingModule,
    SharedModule,
  ]
})
export class DashboardModule { }
