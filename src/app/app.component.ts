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

  constructor(public dialog: MatDialog, private globalService: GlobalService) {}

  ngOnInit(): void {
    this.globalService.logEntries$.subscribe(logEntries => {
      this.logEntries = logEntries;
      if (this.logEntries.length >= 5) {
        this.isGameOver = true;
      }
    });
  }

  openDialog() {
    const questions = this.globalService.getRandomQuestions(5);
    const dialogRef = this.dialog.open(QuestionModalComponent, {
      width: '400px',
      data: { questions }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.incorrect > 3) {
        this.isGameOver = true;
      } else {
        this.isGameWin = true;
      }
      console.log('Correct Answers:', result.correct);
      console.log('Incorrect Answers:', result.incorrect);
    });
  }

 

}
