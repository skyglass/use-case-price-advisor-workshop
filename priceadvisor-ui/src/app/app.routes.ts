import { Routes } from '@angular/router';
import { PricingLiveComponent } from './components/pricing-live/pricing-live';
import { BankingComponent } from './components/banking/banking';

export const routes: Routes = [
  { path: 'pricing', component: PricingLiveComponent },
  { path: 'banking', component: BankingComponent },
  { path: '', redirectTo: '/pricing', pathMatch: 'full' },
  { path: '**', redirectTo: '/pricing' }
];
