import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CreateConcertComponent } from './create-concert.component';
import { ConcertDetailComponent } from './concert-detail.component';
import { ReactiveFormsModule } from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {Headers, RequestOptions} from '@angular/http'; 
@NgModule({
  declarations: [
    CreateConcertComponent,
    ConcertDetailComponent
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [ConcertDetailComponent]
})
export class AppModule { }
