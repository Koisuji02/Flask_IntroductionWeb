'use strict';

/* il COSTRUTTORE (come in Java) */
function Exam(code, name, credits, date, score) {
    this.code = code;
    this.name = name;
    this.credits = credits;
    this.date = dayjs(date);
    this.score = score;
}

/* la lista degli Exam (costruttore della list) */
function ExamList() {
    this.list = [];

    this.init = () => {
        this.list.push(
            new Exam('16ACF', 'Analisi I', 10, '2021-02-01', 28),
            new Exam('15AHM', 'Chimica', 8, '2021-02-15', 21),
            new Exam('14BHD', 'Informatica', 8, '2021-02-06', 30),
        );
    };

    this.getAll = () => {
        return this.list;
    }
}

// metodo più rapido
function createTableRow2(exam) {
    return `<tr>
        <td>${exam.date.format('YYYY-MM-DD')}</td>
        <td>${exam.name}</td>
        <td>${exam.credits}</td>
        <td>${exam.score}</td>
        <td><button id="${exam.code}" class="btn btn-success">+</button></td>
    </tr>`;
}

function createTableRow(exam){
    const tr = document.createElement('tr'); // creo riga della tabella

    const tdDate = document.createElement('td'); // creo singoli elementi della riga
    tdDate.innerText = exam.date.format('YYYY-MM-DD'); // formatta la stringa "data"
    tr.appendChild(tdDate);

    const tdName = document.createElement('td');
    tdName.innerText = exam.name;
    tr.appendChild(tdName);

    const tdCredits = document.createElement('td');
    tdCredits.innerText = exam.credits;
    tr.appendChild(tdCredits);

    const tdScore = document.createElement('td');
    tdScore.innerText = exam.score;
    tr.appendChild(tdScore);

    // creo il bottone per togliere esami
    const tdAction = document.createElement('td');
    const button = document.createElement('button');
    button.id = exam.code;
    button.className = 'btn btn-danger';
    button.innerText = 'X';
    tdAction.append(button);
    tr.appendChild(tdAction);

    tdAction.addEventListener('click', e =>{
        tr.remove();
        console.log(e.target.id);
    })

    return tr;
}

function fillExamTable(exams) {
    const examTable = document.querySelector('#exam-table');
    // equivalente a -> const examTable = document.getElementById('exam-table');
    for(let exam of exams){
        const examEl = createTableRow2(exam);
        // metodo classico (dove aggiungo i nodi):
        //examTable.prepend(examEl);
        // metodo 2 (passo il codice HTML con le stringhe literal `${exam.name}`):
        examTable.insertAdjacentHTML('afterbegin', examEl);
    }
}

/* MAIN */
const examList = new ExamList();
examList.init();
const exams = examList.getAll();
fillExamTable(exams);