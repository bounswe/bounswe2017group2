import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, FormControl } from '@angular/forms';
import {Validators} from '@angular/forms';
import {HttpClient,HttpHeaders} from '@angular/common/http';
import { UserAndTokenService } from '../user.token.service';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { Location }                 from '@angular/common';
import 'rxjs/add/operator/switchMap';
//import {UserAndTokenService} from '../user.token.service';

@Component({
  selector: 'app-root',
  templateUrl: './concert-detail.component.html',
  styleUrls: ['./design.css'],
  //providers: [UserAndTokenService]
})
export class ConcertDetailComponent implements OnInit{
  title = 'Concert Detail';
  commentForm: FormGroup;
  isValid: boolean=false;
  concert: any;
  concertID: any=0;
  token: any=null;
  isLoggedIn: boolean=false;
  private sub: any;
  constructor(private fb: FormBuilder,private http: HttpClient,private userAndToken: UserAndTokenService,private userService: UserAndTokenService,
    private route: ActivatedRoute,
    private location: Location) { // <--- inject FormBuilder 
    //this.concertID = 5;                                                                //ID of concert
    //userAndToken=null;
    //var token="";

  }
  ngOnInit() {
      this.token=this.userAndToken.getUserAndToken();
      //this.route.paramMap.switchMap((params: ParamMap) => this.concertID=0+params.get('id'));
      this.sub = this.route.params.subscribe(params => {
        this.concertID = +params['id']; });// (+) converts string 'id' to a number
        if(this.token){
          //userAndToken.setUserAndToken(this.token);
          this.isLoggedIn=true;
        }
        console.log('concert id is '+this.concertID);  
        console.log('token is '+this.userAndToken.getUserAndToken());  
        this.http.get('http://34.210.127.92:8000/concert/'+this.concertID+'/').subscribe( data => {
          this.concert=data;
        });
        if(this.token){
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