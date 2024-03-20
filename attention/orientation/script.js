const arrow = document.getElementById('arrow');
const arrowLeft1 = document.getElementById('arrow-left1');
const arrowLeft2 = document.getElementById('arrow-left2');
const arrowRight1 = document.getElementById('arrow-right1');
const arrowRight2 = document.getElementById('arrow-right2');
const indicator = document.getElementById('indicator');
const cross = document.getElementById('cross');
const resultsElement = document.getElementById('results');
const startButton = document.getElementById('start');

let direction;
let startTime;
let reactionTime;
let results = [];
let isRunning = false;
let numArrows = 0;

startButton.addEventListener('click', startTest);

function negOrPos() {
  return Math.random() < 0.5 ? -1 : 1;
}

function setArrow() {
  var coef = negOrPos();
  arrow.style.left = `${window.innerWidth / 2 - 25}px`;
  arrow.style.top = `${window.innerHeight / 2 - 5 + 35*coef}px`;
  arrowLeft1.style.top = arrow.style.top
  arrowLeft2.style.top = arrow.style.top
  arrowRight1.style.top = arrow.style.top
  arrowRight2.style.top = arrow.style.top
  direction = Math.random() < 0.5 ? 'left' : 'right';
  arrow.textContent = direction === 'left' ? '←' : '→';
  arrowLeft1.textContent = Math.random() < 0.5 ? '←' : '→';
  arrowLeft2.textContent = Math.random() < 0.5 ? '←' : '→';
  arrowRight1.textContent = Math.random() < 0.5 ? '←' : '→';
  arrowRight2.textContent = Math.random() < 0.5 ? '←' : '→';
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

function showIndicator() {
  indicator.textContent = '*'
  indicator.style.left = `${window.innerWidth / 2 - 10}px`
  indicator.style.top = arrow.style.top
  indicator.style.opacity = 1;
  setTimeout(hideIndicator, 200)
}

function hideIndicator() {
  indicator.style.opacity = 0
  showArrow()
}

function showCross() {
  cross.textContent = 'X'
  cross.style.left = `${window.innerWidth / 2 - 15}px`;
  cross.style.top = `${window.innerHeight / 2}px`;
  cross.style.opacity = 1;
}

function startTest() {
  if (isRunning) {
    return;
  }
  isRunning = true;
  setArrow()
  showCross()
  setTimeout(showIndicator, Math.random() * 2500 + 500)
}

function endTest() {
  hideArrow();
  isRunning = false;
  numArrows++;
  if (numArrows < 5) {
    startTest();
  } else {
    showResults();
  }
}

function showResults() {
  resultsElement.textContent = `Vos temps de réaction sont : ${results.join(', ')}`;
}

document.addEventListener("keydown", function(event) {

  if (!isRunning) {
    return;
  }
  if ((event.key === 'ArrowLeft') || (event.key === 'ArrowRight')) {
    if ((event.key === 'ArrowLeft' && direction === 'left') || (event.key === 'ArrowRight' && direction === 'right')) {
      reactionTime = new Date() - startTime;
      results.push(reactionTime);
      endTest()
    } 
    
    else {
      results.push(-1)
      endTest()
    }
  }
})
