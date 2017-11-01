import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: '<h1>{{title}}</h1>   <nav> <a routerLink="/signup">Sign me up</a> <a routerLink="/login">Log me in</a></nav> <router-outlet></router-outlet>'
})
export class AppComponent {
  title = 'Register';
}
