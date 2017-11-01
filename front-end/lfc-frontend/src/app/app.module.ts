import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CreateConcertComponent } from './create-concert/create-concert.component';
import { ReactiveFormsModule } from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {Headers, RequestOptions} from '@angular/http';
import { HeaderComponent } from './header/header.component';
import { LoginFormComponent } from './login-form/login-form.component';
import { FooterComponent } from './footer/footer.component'; 

import { AppComponent } from './app.component';
@NgModule({
  declarations: [
    CreateConcertComponent,
    HeaderComponent,
    LoginFormComponent,
    FooterComponent,
    AppComponent
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
