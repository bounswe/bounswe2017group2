import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, FormControl } from '@angular/forms';
import {Validators} from '@angular/forms'

@Component({
  selector: 'app-root',
  templateUrl: './create-concert.component.html',
  styleUrls: ['./create-concert.component.css']
})
export class CreateConcertComponent {
  title = 'app';
  concertForm: FormGroup;

  constructor(private fb: FormBuilder) { // <--- inject FormBuilder
    this.createForm();
  }

  createForm() {
    this.concertForm = this.fb.group({
      name: ['',Validators.required], // <--- the FormControl called "name"
      artist: ['',Validators.required],
      //location: '',
      date_time: ['',Validators.required],
      price_min: [Number,Validators.required],
      price_max: [Number,Validators.required],
      tags: this.fb.array([]),
    });
  }
  get tags(): FormArray {
    return this.concertForm.get('Choices') as FormArray;
  }
  addTag(){
    this.tags.push(new FormControl("",Validators.required));
  }
  deleteTag(i){
    this.tags.removeAt(i);
  }}
