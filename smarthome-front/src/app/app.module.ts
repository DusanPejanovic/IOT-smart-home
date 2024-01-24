import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { Pi1Component } from './pi1/pi1.component';
import { Pi2Component } from './pi2/pi2.component';
import { Pi3Component } from './pi3/pi3.component';

@NgModule({
  declarations: [
    AppComponent,
    Pi1Component,
    Pi2Component,
    Pi3Component
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
