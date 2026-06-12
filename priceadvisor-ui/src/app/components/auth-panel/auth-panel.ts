import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { AuthService } from '../../services/auth';

@Component({
  standalone: true,
  selector: 'app-auth-panel',
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule
  ],
  templateUrl: './auth-panel.html',
  styleUrl: './auth-panel.css'
})
export class AuthPanel {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);

  readonly authenticated$ = this.auth.isAuthenticated$;
  errorMessage = '';
  submitting = false;

  readonly loginForm = this.fb.group({
    clientId: ['price-advisor-ui', Validators.required],
    username: ['alice', Validators.required],
    password: ['password', Validators.required]
  });

  login(): void {
    if (this.loginForm.invalid) return;

    const value = this.loginForm.getRawValue();
    this.errorMessage = '';
    this.submitting = true;

    this.auth.login({
      clientId: value.clientId ?? 'price-advisor-ui',
      username: value.username ?? '',
      password: value.password ?? ''
    }).subscribe({
      next: () => {
        this.submitting = false;
      },
      error: err => {
        this.submitting = false;
        this.errorMessage = err?.error?.error_description ?? err?.message ?? 'Login failed';
      }
    });
  }

  logout(): void {
    this.auth.logout();
  }
}
