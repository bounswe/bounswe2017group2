import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, FormControl } from '@angular/forms';
import {Validators} from '@angular/forms';
import {HttpClient,HttpHeaders} from '@angular/common/http';
import {UserAndTokenService} from './user.token.service';
@Component({
  selector: 'app-root',
  templateUrl: './concert-detail.component.html',
  styleUrls: ['./design.css'],
  providers: [UserAndTokenService]
})
export class ConcertDetailComponent {
  title = 'Concert Detail';
  commentForm: FormGroup;
  isValid: boolean=false;
  concert: any;
  concertID: any;
  constructor(private fb: FormBuilder,private http: HttpClient,private userAndToken: UserAndTokenService) { // <--- inject FormBuilder 
    this.concertID = 5;                                                                //ID of concert
    userAndToken=null;
    var token="";
    if(userAndToken)
      userAndToken.setUserAndToken(token);
    this.http.get('http://34.210.127.92:8000/concert/'+this.concertID+'/').subscribe( data => {
      this.concert=data;
    });
    if(userAndToken){
      this.createCommentForm();
    }
  }

  createCommentForm(){
    this.commentForm = this.fb.group({
      content: ['',Validators.required]
    });
  }
  sendComment(){
    let formVal=JSON.stringify(this.commentForm.value);
    let header=new HttpHeaders().set('Content-Type', 'application/json');
    header = header.append('Authorization','Token '+this.userAndToken.getUserAndToken());
    this.http.post('http://34.210.127.92:8000/concert/'+this.concertID+'/newcomment/',formVal,{headers: header,}).subscribe(
      response => {
        window.location.reload();
    });
  }
}
