const arrow = document.getElementById('arrow');
const arrowLeft1 = document.getElementById('arrow-left1');
const arrowLeft2 = document.getElementById('arrow-left2');
const arrowRight1 = document.getElementById('arrow-right1');
const arrowRight2 = document.getElementById('arrow-right2');
const indicator = document.getElementById('indicator');
const cross = document.getElementById('cross');
const resultsElement = document.getElementById('results');

document.getElementById('backToMenu').addEventListener('click', function() {
  window.location.href = "/testSelectionPanel";
});

// let alert = new Audio("{{url_for('static', filename='alert.mp3')}}");
let d1;
let runningTest;
let direction;
let startTestTime;
let startTime;
let reactionTime;
let reactionTimes = [];
let isCorrect = [];
let timeCodes = [];
let isRunning = false;
let numTests1 = 0;
let numTests2 = 0;
let coef;
let initialTime;
let responseTimeout;


function negOrPos() {
  return Math.random() < 0.5 ? -1 : 1;
}

function setArrow1() {   //fonction pour afficher les flèches congruentes
  coef = negOrPos();

  arrow.style.top = `calc(50% + ${coef*90 - 30}px)`;
  arrowLeft1.style.top = arrow.style.top
  arrowLeft2.style.top = arrow.style.top
  arrowRight1.style.top = arrow.style.top
  arrowRight2.style.top = arrow.style.top
  directionCentre = Math.random() < 0.5 ? '←' : '→';
  arrow.textContent = directionCentre;
  arrowLeft1.textContent = directionCentre;
  arrowLeft2.textContent = directionCentre;
  arrowRight1.textContent = directionCentre;
  arrowRight2.textContent = directionCentre;
}

function setArrow2() {  //fonction pour afficher les flèches non congruentes
  coef = negOrPos();
  // arrow.style.left = `${window.innerWidth / 2 - 25}px`;
  // arrow.style.left = `${window.innerWidth / 2 - 25}px`;
  // arrow.style.top = `${window.innerHeight / 2 - 5 + 35*coef}px`;
  arrow.style.top = `calc(50% + ${coef*90 - 30}px)`;

  arrowLeft1.style.top = arrow.style.top
  arrowLeft2.style.top = arrow.style.top
  arrowRight1.style.top = arrow.style.top
  arrowRight2.style.top = arrow.style.top
  directionCentre = Math.random() < 0.5 ? '←' : '→';
  let directionCote = directionCentre === '←' ? '→' : '←';
  arrow.textContent = directionCentre;
  arrowLeft1.textContent = directionCote;
  arrowLeft2.textContent = directionCote;
  arrowRight1.textContent = directionCote;
  arrowRight2.textContent = directionCote;
}

function showArrow() {
  let timeCode = new Date() - startTestTime;
  timeCodes.push(timeCode);
  arrow.style.opacity = 1;
  arrowLeft1.style.opacity = 1;
  arrowLeft2.style.opacity = 1;
  arrowRight1.style.opacity = 1;
  arrowRight2.style.opacity = 1;
  startTime = new Date();
// Ajouter un délai de 3 secondes pour vérifier si l'utilisateur n'a pas répondu
  responseTimeout = setTimeout(function() {
  reactionTime = 1700
  reactionTimes.push(1700); // Ajouter -1 aux réponses de reactionTimes
  isCorrect.push(0);
  endTest();
}, 1700);
}

function hideArrow() {
  arrow.style.opacity = 0;
  arrowLeft1.style.opacity = 0;
  arrowLeft2.style.opacity = 0;
  arrowRight1.style.opacity = 0;
  arrowRight2.style.opacity = 0;
  // Annuler le délai de 3 secondes si l'utilisateur a déjà répondu
  clearTimeout(responseTimeout);

}

function playAlert(){
  alert.play();
  setTimeout(showIndicator, Math.random() * 400 + 200)
}

function showIndicator() {
  indicator.textContent = '*'
  // indicator.style.left = `${window.innerWidth / 2 - 10}px`;
  indicator.style.top = `${window.innerHeight / 2 + 10 + 90*coef}px`;
  indicator.style.opacity = 1;
  setTimeout(hideIndicator, 100)
 
}

function hideIndicator() {
  indicator.style.opacity = 0
  setTimeout(showArrow, 400)
}

function showCross() {
  cross.textContent = '+'
  // cross.style.left = `${window.innerWidth / 2 - 15}px`;
  arrow.style.top = `calc(50% + ${coef*35 - 30}px)`;
  // cross.style.top = `${window.innerHeight / 2}px`;
  cross.style.opacity = 1;
}

function startTest1() {
  if (isRunning) {
    return;
  }
  isRunning = true;
  runningTest = 1;
  if (numTests1 === 0) {
    startTestTime = new Date();
  }
  numTests1++;
  setArrow1()
  d1 = Math.random() * 600 + 400;
  setTimeout(playAlert, d1)
  initialTime = new Date();
  console.log(reactionTimes);
}

function startTest2() {
  if (isRunning) {
    return;
  }
  isRunning = true;
  if (numTests2 === 0) {
    startTestTime = new Date();
  }
  runningTest = 2;
  numTests2++;
  initialTime = new Date();
  setArrow2()
  d1 = Math.random() * 1200 + 900;
  setTimeout(showArrow, d1)
}

function endTest() {
  let endTime = 0;
  hideArrow();
  isRunning = false;
 
  if (numTests1 > 0){ 
    nb_minutes_1 = 5;
    endTime = nb_minutes_1 * 60 * 1000; //1er test dure 1min30
  } else { 
    nb_minutes_2 = 15;
    endTime = nb_minutes_2 * 60 * 1000; //2ème test dure 3min
  }
  if (new Date() - startTestTime < endTime) {
  
    if (numTests1 > 0) {
      setTimeout(startTest1, 3500-reactionTime);
    } 
    if (numTests2 > 0) {
      setTimeout(startTest2, 3500-reactionTime);
    }
  } else {
      numTests1 = 0;
      numTests2 = 0;
      showResults();
      sendResults(reactionTimes, timeCodes, runningTest=runningTest, isCorrect=isCorrect);
  }
}

function sendResults() {
  fetch('/results', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      reactionTimes: reactionTimes,
      timeCodes: timeCodes,
      runningTest: runningTest,
      isCorrect: isCorrect
    })
  })
  .then(response => {
    if (response.ok) {
      console.log('Results have been successfully saved.');
    } else {
      console.error('An error occurred while saving the results.');
    }
  })
  .catch(error => {
    console.error('An error occurred while saving the results.', error);
  });
}

function sendResult(reactionTime, timeCode, runningTest) {
  fetch('/result', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      reactionTime: reactionTime,
      timeCode: timeCode,
      runningTest: runningTest
    })
  })
  .then(response => {
    if (response.ok) {
      console.log('Results have been successfully saved.');
    } else {
      console.error('An error occurred while saving the results.');
    }
  })
  .catch(error => {
    console.error('An error occurred while saving the results.', error);
  });
}


function showResults() {
  sendResults();
  resultsElement.textContent = `Vos temps de réaction sont : ${reactionTimes.join(', ')}`;
}

document.addEventListener("keydown", function(event) {

  if (!isRunning) {
    return;
  }
  if ((event.key === 'ArrowLeft') || (event.key === 'ArrowRight')) {
    let timeCode = new Date() - startTestTime;
    let reactionTime = new Date() - startTime;
    reactionTimes.push(reactionTime);
    timeCodes.push(timeCode);
    if ((event.key === 'ArrowLeft' && directionCentre === '←') || (event.key === 'ArrowRight' && directionCentre === '→')) {
      
      isCorrect.push(1);
      //console.log(reactionTime, timeCode, runningTest);
      //console.log("timeCodes", timeCodes);
      //sendResult(reactionTime=reactionTime, timeCode=timeCode, runningTest=runningTest);
    } 
    
    else {
      isCorrect.push(0);
    }
    // Annuler le délai de 3 secondes si l'utilisateur a déjà répondu
    clearTimeout(responseTimeout);
    endTest();
  }
})
