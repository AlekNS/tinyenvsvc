import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './components/dashboard.component';
import { HomeComponent } from './components/home.component';
import { UploadsComponent } from './components/uploads.component';

const routes: Routes = [
  {
    path: 'dashboard',
    component: DashboardComponent,
    children: [
      {
        path: '',
        component: HomeComponent,
      },
      {
        path: 'uploads',
        component: UploadsComponent,
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: []
})
export class DashboardRoutingModule { }
