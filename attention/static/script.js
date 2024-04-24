const arrow = document.getElementById('arrow');
const arrowLeft1 = document.getElementById('arrow-left1');
const arrowLeft2 = document.getElementById('arrow-left2');
const arrowRight1 = document.getElementById('arrow-right1');
const arrowRight2 = document.getElementById('arrow-right2');
const indicator = document.getElementById('indicator');
const cross = document.getElementById('cross');
const resultsElement = document.getElementById('results');


let alert = new Audio('../assets/alert.mp3');

let direction;
let startTestTime;
let startTime;
let reactionTime;
let reactionTimes = [];
let timeCodes = [];
let isRunning = false;
let numTests1 = 0;
let numTests2 = 0;
let coef;
let initialTime;


function negOrPos() {
  return Math.random() < 0.5 ? -1 : 1;
}

function setArrow1() {   //fonction pour afficher les flèches congruentes
  coef = negOrPos();
  arrow.style.left = `${window.innerWidth / 2 - 25}px`;
  arrow.style.top = `${window.innerHeight / 2 - 5 + 35*coef}px`;
  arrowLeft1.style.top = arrow.style.top
  arrowLeft2.style.top = arrow.style.top
  arrowRight1.style.top = arrow.style.top
  arrowRight2.style.top = arrow.style.top
  let directionCentre = Math.random() < 0.5 ? '←' : '→';
  arrow.textContent = directionCentre;
  arrowLeft1.textContent = directionCentre;
  arrowLeft2.textContent = directionCentre;
  arrowRight1.textContent = directionCentre;
  arrowRight2.textContent = directionCentre;
}

function setArrow2() {  //fonction pour afficher les flèches non congruentes
  coef = negOrPos();
  arrow.style.left = `${window.innerWidth / 2 - 25}px`;
  arrow.style.top = `${window.innerHeight / 2 - 5 + 35*coef}px`;
  arrowLeft1.style.top = arrow.style.top
  arrowLeft2.style.top = arrow.style.top
  arrowRight1.style.top = arrow.style.top
  arrowRight2.style.top = arrow.style.top
  let directionCentre = Math.random() < 0.5 ? '←' : '→';
  let directionCote = directionCentre === '←' ? '→' : '←';
  arrow.textContent = directionCentre;
  arrowLeft1.textContent = directionCote;
  arrowLeft2.textContent = directionCote;
  arrowRight1.textContent = directionCote;
  arrowRight2.textContent = directionCote;
}

function showArrow() {
  arrow.style.opacity = 1;
  arrowLeft1.style.opacity = 1;
  arrowLeft2.style.opacity = 1;
  arrowRight1.style.opacity = 1;
  arrowRight2.style.opacity = 1;
  startTime = new Date();
}

function hideArrow() {
  arrow.style.opacity = 0;
  arrowLeft1.style.opacity = 0;
  arrowLeft2.style.opacity = 0;
  arrowRight1.style.opacity = 0;
  arrowRight2.style.opacity = 0;
}

function playAlert(){
  alert.play();
  setTimeout(showIndicator, 500)
}

function showIndicator() {
  indicator.textContent = '*'
  indicator.style.left = `${window.innerWidth / 2 - 10}px`;
  indicator.style.top = `${window.innerHeight / 2 + 10 + 35*coef}px`;
  indicator.style.opacity = 1;
  setTimeout(hideIndicator, 200)
  setTimeout(hideIndicator, 200)
}

function hideIndicator() {
  indicator.style.opacity = 0
  showArrow()
}

function showCross() {
  cross.textContent = '+'
  cross.style.left = `${window.innerWidth / 2 - 15}px`;
  cross.style.top = `${window.innerHeight / 2}px`;
  cross.style.opacity = 1;
}

function startTest1() {
  if (isRunning) {
    return;
  }
  isRunning = true;
  if (numTests1 === 0) {
    startTestTime = new Date();
  }
  numTests1++;
  setArrow1()
  showCross()
}

function startTest2() {
  if (isRunning) {
    return;
  }
  isRunning = true;
  if (numTests2 === 0) {
    startTestTime = new Date();
  }
  numTests2++;
  setArrow2()
  showCross()
  setTimeout(playAlert, Math.random() * 2500 + 500)
  initialTime = new Date();
}

function endTest() {
  let endTime = 0;
  hideArrow();
  isRunning = false;
 
  if (numTests1 > 0){ 
    endTime = 90000; //1er test dure 1min30
  } else { 
    endTime = 180000; //2ème test dure 3min
  }
  if (new Date() - startTestTime < endTime) {
    if (numTests1 > 0) {
      startTest1();
    } 
    if (numTests2 > 0) {
      startTest2();
    }
  } else {
      numTests1 = 0;
      numTests2 = 0;
      showResults();
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
      timeCodes: timeCodes
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

function sendResult(reactionTime, timeCode) {
  fetch('/result', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      reactionTime: reactionTime,
      timeCode: timeCode
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
  resultsElement.textContent = `Vos temps de réaction sont : ${results.join(', ')}`;
}

document.addEventListener("keydown", function(event) {

  if (!isRunning) {
    return;
  }
  if ((event.key === 'ArrowLeft') || (event.key === 'ArrowRight')) {
    if ((event.key === 'ArrowLeft' && direction === 'left') || (event.key === 'ArrowRight' && direction === 'right')) {
      reactionTime = new Date() - startTime;
      reactionTimes.push(reactionTime);
      timeCodes.push(new Date() - initialTime)
      sendResults()
      endTest()
    } 
    
    else {
      reactionTimes.push(-1)
      endTest()
    }
  }
})
