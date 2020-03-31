import { ApiService } from './../api.service';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormsModule } from '@angular/forms';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss']
})
export class ResultComponent implements OnInit {

  public parentList = [];

  resultForm: FormGroup;

  constructor(private fb: FormBuilder, private apiService: ApiService) { }

  ngOnInit() {
    this.resultForm = this.fb.group({
      res_type: ['M'],
      course: ['BTECH', [Validators.required]],
      sem: ['5', [Validators.required, Validators.min(1), Validators.max(8), Validators.maxLength(1)]],
      roll_no: ['0101CS171001', Validators.required],
      no: ['3', [Validators.required, Validators.min(1), Validators.maxLength(3)]]
    });
    // this.resultForm.valueChanges.subscribe(this.updateCourse);
  }

  get res_type() {
    return this.resultForm.get('res_type');
  }

  get course() {
    return this.resultForm.get('course');
  }

  get sem() {
    return this.resultForm.get('sem');
  }

  get roll_no() {
    return this.resultForm.get('roll_no');
  }

  get no() {
    return this.resultForm.get('no');
  }

  onSubmit(): void {
    this.apiService.getResult(this.resultForm.value).subscribe(
      response => this.parentList.push.apply(this.parentList, response),
      error => console.log('error', error)
    );
  }

}
