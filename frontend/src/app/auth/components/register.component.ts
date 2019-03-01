import { Component, OnInit } from '@angular/core';
import { Validators, FormControl, FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-auth-register',
  templateUrl: './register.component.html',
  styleUrls: ['./common.component.scss']
})
export class RegisterComponent implements OnInit {
  validateForm: FormGroup;

  constructor(private fb: FormBuilder) {
  }

  ngOnInit(): void {
    this.validateForm = this.fb.group({
      email: [null, [Validators.email, Validators.required]],
      password: [null, [Validators.minLength(6), Validators.required]],
      checkPassword: [null, [Validators.required, this.confirmationValidator]],
    });
  }

  submitForm(): void {
    for (const i in this.validateForm.controls) {
      this.validateForm.controls[i].markAsDirty();
      this.validateForm.controls[i].updateValueAndValidity();
    }

    // dispatch
  }

  confirmationValidator = (control: FormControl): { [s: string]: boolean } => {
    if (!control.value) {
      return { required: true };
    } else if (control.value !== this.validateForm.controls.password.value) {
      return { confirm: true, error: true };
    }
  };
}
