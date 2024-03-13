const arrow = document.getElementById('arrow');
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

function setArrow() {
  arrow.style.left = `${Math.random() * (window.innerWidth - 50)}px`;
  arrow.style.top = `${Math.random() * (window.innerHeight - 50)}px`;
  direction = Math.random() < 0.5 ? 'left' : 'right';
  arrow.textContent = direction === 'left' ? '←' : '→';
}

function showArrow() {
  arrow.style.opacity = 1
}

function hideArrow() {
  arrow.style.opacity = 0
}

function showCross() {
  cross.style.left = arrow.style.left;
  cross.style.top = arrow.style.top;
  cross.style.opacity = 1;
}

function startTest() {
  if (isRunning) {
    return;
  }
  isRunning = true;
  setArrow()
  showCross()
  setTimeout(showArrow, Math.random() * 5000 + 500)
  startTime = new Date();
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
