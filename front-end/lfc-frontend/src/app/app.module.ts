import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CreateConcertComponent } from './create-concert.component';
import { ReactiveFormsModule } from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {Headers, RequestOptions} from '@angular/http'; 
@NgModule({
  declarations: [
    CreateConcertComponent
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [CreateConcertComponent]
})
export class AppModule { }
