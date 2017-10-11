import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CreateConcertComponent } from './create-concert.component';
import { ReactiveFormsModule } from '@angular/forms';
@NgModule({
  declarations: [
    CreateConcertComponent
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [CreateConcertComponent]
})
export class AppModule { }
