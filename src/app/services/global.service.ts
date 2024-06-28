import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GlobalService {

  private logEntriesSubject = new BehaviorSubject<{ id: number, moving: boolean }[]>([]);
  logEntries$ = this.logEntriesSubject.asObservable();

  private questions = [
    {
      "question": "Les insectes sont les appareils biologiques les plus abondants sur la planète?",
      "answer": false
    },
    {
      "question": "La biodiversité menace particulièrement l'avenir de la planète?",
      "answer": true
    },
    {
      "question": "Les espèces qui cohabitent dans un écosystème dépendent les unes des autres pour leur survie, c'est ce qu'on appelle la \"coopération\" écologique.",
      "answer": false
    },
    {
      "question": "Les forêts tropicales sont-elles les régions les plus pollueuses de la planète?",
      "answer": false
    },
    {
      "question": "Lors de la décomposition d'une feuille, la microbiote bénéficie de la présence d'oxygène pour métaboliser efficacement les molécules organiques.",
      "answer": false
    },
    {
      "question": "L'étude de la biomasse est essentielle pour évaluer l'état de santé d'un écosystème.",
      "answer": true
    },
    {
      "question": "Les écosystèmes sont particulièrement vulnérables aux changements climatiques.",
      "answer": true
    },
    {
      "question": "L'aire de répartition de l'ours brun (Ursus arctos) est en constante augmentation dans les dernières années en raison de sa résilience et de la préservation des habitats.",
      "answer": false
    },
    {
      "question": "Les termes \"écologie\" et \"biologie\" sont synonymes?",
      "answer": false
    },
    {
      "question": "La pollution par le plastique a un impact négatif sur les écosystèmes marins.",
      "answer": true
    }
  ];

  constructor() { }

  getRandomQuestions(num: number) {
    return this.questions.sort(() => 0.5 - Math.random()).slice(0, num);
  }

  addLogEntry() {
    const logEntries = this.logEntriesSubject.value;
    const newLogEntry = { id: logEntries.length, moving: false };
    logEntries.push(newLogEntry);
    this.logEntriesSubject.next(logEntries);
    setTimeout(() => this.moveLogEntry(newLogEntry.id), 100);
  }

  private moveLogEntry(id: number) {
    const logEntries = this.logEntriesSubject.value.map(logEntry => 
      logEntry.id === id ? { ...logEntry, moving: true } : logEntry
    );
    this.logEntriesSubject.next(logEntries);
  }

}
