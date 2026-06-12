import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, map, Observable, tap } from 'rxjs';
import { AppConfigService } from '../config/app-config.service';

export interface LoginRequest {
  clientId: string;
  username: string;
  password: string;
}

interface TokenResponse {
  access_token: string;
  expires_in: number;
  refresh_expires_in?: number;
  token_type: string;
  scope?: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly tokenKey = 'priceadvisor.accessToken';
  private readonly authState = new BehaviorSubject<boolean>(!!localStorage.getItem(this.tokenKey));
  readonly isAuthenticated$ = this.authState.asObservable();

  constructor(private http: HttpClient, private cfg: AppConfigService) {}

  get token(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  login(request: LoginRequest): Observable<void> {
    const c = this.cfg.config;
    const body = new URLSearchParams();
    body.set('grant_type', 'password');
    body.set('client_id', request.clientId);
    body.set('username', request.username);
    body.set('password', request.password);
    body.set('scope', 'openid profile customer-id transfer-service-audience');

    return this.http.post<TokenResponse>(`${c.apiBaseUrl}${c.authTokenPath}`, body.toString(), {
      headers: new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' })
    }).pipe(
      tap(response => {
        localStorage.setItem(this.tokenKey, response.access_token);
        this.authState.next(true);
      }),
      map(() => void 0)
    );
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    this.authState.next(false);
  }
}
