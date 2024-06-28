import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { GlobalService } from 'src/app/services/global.service';

@Component({
  selector: 'app-question-modal',
  templateUrl: './question-modal.component.html',
  styleUrls: ['./question-modal.component.scss']
})
export class QuestionModalComponent {

  currentQuestionIndex = 0;
  score = 0;
  correctAnswers = 0;
  incorrectAnswers = 0;

  constructor(
    public dialogRef: MatDialogRef<QuestionModalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any, private globalService: GlobalService,
  ) { }

  checkAnswer(userAnswer: boolean) {
    const question = this.data.questions[this.currentQuestionIndex];
    if (question.answer === userAnswer) {
      this.correctAnswers++;
    } else {
      this.incorrectAnswers++;
      this.globalService.addLogEntry();
    }

    if (this.currentQuestionIndex < this.data.questions.length - 1) {
      this.currentQuestionIndex++;
    } else {
      this.dialogRef.close({ correct: this.correctAnswers, incorrect: this.incorrectAnswers });
    }
  }


}
