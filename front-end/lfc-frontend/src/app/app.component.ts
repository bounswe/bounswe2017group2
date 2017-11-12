import { Component, OnInit } from '@angular/core';
import { UserAndTokenService } from './user.token.service';
import { NgIf} from '@angular/common';
@Component({
  selector: 'app-root',
  //template: '<h1>{{title}}</h1>   <nav> <a routerLink="/signup">Sign me up</a> <a routerLink="/login">Log me in</a></nav> <router-outlet></router-outlet>'
  templateUrl: 'app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent /*implements OnInit*/{
  title = 'Looking for concerts';
  isLoggedIn: boolean=false;
  token: any=null;
  constructor(private userAndToken: UserAndTokenService){

  }
  ngOnInit() {
    this.token=this.userAndToken.getUserAndToken().token;
    if(this.token){
      this.isLoggedIn=true;
    }
  }

}
