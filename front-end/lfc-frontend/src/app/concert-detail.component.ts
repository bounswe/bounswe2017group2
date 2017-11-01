import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, FormControl } from '@angular/forms';
import {Validators} from '@angular/forms';
import {HttpClient,HttpHeaders} from '@angular/common/http';
@Component({
  selector: 'app-root',
  templateUrl: './concert-detail.component.html',
  styleUrls: ['./design.css']
})
export class ConcertDetailComponent {
  title = 'Concert Detail';
  commentForm: FormGroup;
  isValid: boolean=false;
  concert: any;
  concertID: any;
  constructor(private fb: FormBuilder,private http: HttpClient) { // <--- inject FormBuilder 
    this.concertID = 14;                                                                //ID of concert
    this.http.get('http://34.210.127.92:8000/concert/'+this.concertID+'/').subscribe( data => {
      this.concert=data;
    });
    this.createCommentForm();
  }

  createCommentForm(){
    this.commentForm = this.fb.group({
      content: ['',Validators.required]
    });
  }
  sendComment(){
    let formVal=JSON.stringify(this.commentForm.value);
    this.http.post('http://34.210.127.92:8000/concert/'+this.concertID+'/newcomment/',formVal,{headers: new HttpHeaders().set('Content-Type', 'application/json'),}).subscribe(
      response => {
        window.location.reload();
    });
  }
}
