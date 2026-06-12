import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { AuthPanel } from './components/auth-panel/auth-panel';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    MatSlideToggleModule,
    MatTableModule,
    MatCardModule,
    AuthPanel
  ],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  isDarkMode = false;

  toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
    }

}
