import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthService).token;
  const isAuthRequest = req.url.includes('/auth/token');
  const isConfigRequest = req.url.endsWith('/app-config.json') || req.url.endsWith('app-config.json');

  if (!token || isAuthRequest || isConfigRequest) {
    return next(req);
  }

  return next(req.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`
    }
  }));
};
