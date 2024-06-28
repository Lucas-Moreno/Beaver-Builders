import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { QuestionModalComponent } from './pages/question-modal/question-modal.component';
import { GlobalService } from './services/global.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  logEntries: { id: number, moving: boolean }[] = [];
  isGameOver = false;
  isGameWin = false;
  questions: any[] = [];

  backgroundClass = 'background-one';

  constructor(public dialog: MatDialog, private globalService: GlobalService) { }

  async ngOnInit() {
    this.globalService.logEntries$.subscribe(logEntries => {
      this.logEntries = logEntries;
      if (this.logEntries.length >= 5) {
        this.isGameOver = true;
      }
    });

    try {
      this.globalService.get('/questions').subscribe(async (res) => {
        this.questions = await res.slice(0, 5);
      });
    } catch (error) {
      console.error('Erreur lors de la récupération des questions', error);
    }
  }

  openDialog() {
    if (this.questions.length > 0) {
      const dialogRef = this.dialog.open(QuestionModalComponent, {
        width: '400px',
        data: { 'questions': this.questions }
      });
      dialogRef.afterClosed().subscribe(result => {
        if (result.incorrect > 3) {
          this.isGameOver = true;
        } else {
          this.isGameWin = true;
          this.toggleBackground();
        }
        console.log('Correct Answers:', result.correct);
        console.log('Incorrect Answers:', result.incorrect);
      });
    }
  }
  
  toggleBackground() {
    this.isGameOver = !this.isGameOver;
    this.backgroundClass = this.isGameOver ? 'background-two' : 'background-one';
  }

}
