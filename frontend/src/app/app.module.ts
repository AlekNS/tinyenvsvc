import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule, NoopAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import en from '@angular/common/locales/en';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { registerLocaleData, APP_BASE_HREF } from '@angular/common';

import { DashboardModule } from './dashboard/dashboard.module';
import { SharedModule } from './shared/shared.module';
import { CoreModule } from './core/core.module';
import { AuthModule } from './auth/auth.module';
import { DataModule } from './data/data.module';

registerLocaleData(en);

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    // BrowserAnimationsModule,
    NoopAnimationsModule,

    SharedModule,
    CoreModule,
    AuthModule,
    DashboardModule,
    DataModule,

    AppRoutingModule,
  ],
  bootstrap: [AppComponent],
  providers: [
    { provide: APP_BASE_HREF, useValue: '/' },
  ],
})
export class AppModule { }
