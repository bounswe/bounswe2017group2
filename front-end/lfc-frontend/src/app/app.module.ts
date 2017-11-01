import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CreateConcertComponent } from './create-concert/create-concert.component';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule} from '@angular/common/http';
import { Headers, RequestOptions} from '@angular/http';
import { HeaderComponent } from './header/header.component';
import { LoginFormComponent } from './login-form/login-form.component';
import { FooterComponent } from './footer/footer.component'; 
import { RegistrationComponent } from './registration/registration.component';

import { AppComponent } from './app.component';
import { ConcertDetailComponent } from './concert-detail/concert-detail.component';
import { MainpageComponent } from './mainpage/mainpage.component';
import { UserAndTokenService } from './user.token.service';
import { RouterModule }   from '@angular/router';

@NgModule({
  declarations: [
    CreateConcertComponent,
    HeaderComponent,
    LoginFormComponent,
    FooterComponent,
    AppComponent,
    RegistrationComponent,
    ConcertDetailComponent,
    //UserAndTokenService,
    MainpageComponent
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule,
    HttpClientModule,RouterModule.forRoot([
      {
        path: 'login',
        component: LoginFormComponent
      },
      {
        path:'signup',
        component: RegistrationComponent
      },      {
        path:'mainpage',
        component: MainpageComponent
      },
      {
        path: '',
        redirectTo: '/mainpage',
        pathMatch: 'full'
      },
      {
        path: 'concert/:id',
        component: ConcertDetailComponent
      }
      ])
  ],
  providers: [UserAndTokenService],
  bootstrap: [AppComponent]
})
export class AppModule { }
