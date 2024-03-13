const arrow = document.getElementById('arrow');
const message = document.getElementById('message');
const time = document.getElementById('time');
const startButton = document.getElementById('start');

let direction;
let startTime;
let reactionTime;
let results = [];
let isRunning = false;

startButton.addEventListener('click', startTest);

function hideArrow() {
  arrow.style.opacity = 0
}


function startTest() {
  if (isRunning) {
    return;
  }
  isRunning = true;
  message.textContent = '';
  time.textContent = '';
  direction = Math.random() < 0.5 ? 'left' : 'right';
  arrow.style.left = `${Math.random() * (window.innerWidth - 50)}px`;
  arrow.style.top = `${Math.random() * (window.innerHeight - 50)}px`;
  arrow.textContent = direction === 'left' ? '←' : '→';
  arrow.style.opacity = 1;
  startTime = new Date();
}

document.addEventListener("keydown", function(event) {

  if (!isRunning) {
    message.textContent = "Il n'y a aucune flèche";
    return;
  }
  if ((event.key === 'ArrowLeft' && direction === 'left') || (event.key === 'ArrowRight' && direction === 'right')) {
    reactionTime = new Date() - startTime;
    time.textContent = `Votre temps de réaction est de ${reactionTime} ms`;
    hideArrow();
    results.push(reactionTime);
    setTimeout(startTest, Math.random() * 5000 + 500);
    isRunning = false;

  } else {
    message.textContent = 'Mauvaise flèche !';
    hideArrow();
    setTimeout(startTest, Math.random() * 5000 + 500);
    isRunning = false;
  }
})
