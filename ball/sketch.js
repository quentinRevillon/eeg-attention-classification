let ballX = 0;
let ballY = 0;
let ballSpeedX = 0;
let ballSpeedY = 0;
let squareSize = 400;
let rebounds = 0;
let gameStarted = false;
let gameEnded = false;
let timer = 10;
let difficultMode = false;
let additionalBalls = [];

function setup() {
  const container = document.querySelector('.sketch-container');
  const canvas = createCanvas(400, 400);
  canvas.parent(container);

  // Positionner la balle au centre du carré
  ballX = (width - squareSize) / 2 + squareSize / 2;
  ballY = (height - squareSize) / 2 + squareSize / 2;

}

function draw() {
  background(220);

  if (gameStarted && !gameEnded) {
    // Dessiner le carré
    fill(0);
    rect((width - squareSize) / 2, (height - squareSize) / 2, squareSize, squareSize);

    // Dessiner la balle
    fill(255);
    ellipse(ballX, ballY, 20, 20);

    // Déplacer la balle
    ballX += ballSpeedX;
    ballY += ballSpeedY;

    if (difficultMode) {
        updateAdditionalBalls();
        drawAdditionalBalls();
      }

    // Vérifier les collisions avec les bords du carré
    if (
      (ballX - 10 < (width - squareSize) / 2 && ballSpeedX < 0) ||
      (ballX + 10 > (width + squareSize) / 2 && ballSpeedX > 0)
    ) {
      ballSpeedX *= -1;
      rebounds++;
    }

    if (
      (ballY - 10 < (height - squareSize) / 2 && ballSpeedY < 0) ||
      (ballY + 10 > (height + squareSize) / 2 && ballSpeedY > 0)
    ) {
      ballSpeedY *= -1;
      rebounds++;
    }

    // Compte à rebours
    timer -= deltaTime / 1000;
    if (timer <= 0) {
      gameEnded = true;
    }
  } else if (gameEnded) {
    // Afficher le message de fin et demander le nombre de rebonds
    document.querySelector(".result-container").style.display = "block";

  }
}

function startGame() {
  gameStarted = true;
  timer = 60;
  rebounds = 0;

  // Réinitialiser la position de la balle et générer une nouvelle direction aléatoire
  ballX = (width - squareSize) / 2 + squareSize / 2;
  ballY = (height - squareSize) / 2 + squareSize / 2;
  generateRandomSpeed();
  document.querySelector("#start-button").style.display = "none";

}

function checkAnswer() {
    const userAnswer = document.querySelector('.input-field').value;
    const resultContainer = document.querySelector('.result-container');
    const resultText = document.querySelector('.result-text');
  
    log(rebounds)

    if (parseInt(userAnswer) === rebounds) {
      resultText.textContent = "Bonne réponse !";
      resultText.style.color = "#008000";
    } else {
      resultText.textContent = "Mauvaise réponse !";
      resultText.style.color = "#ff0000";
    }
  
    resultContainer.style.display = "block";
    noLoop();
  }

function generateRandomSpeed() {
  // Générer une vitesse aléatoire entre 1 et 5
  let speed = floor(random(6, 12));

  // Générer un angle aléatoire entre 0 et 2π (360 degrés)
  let angle = random(TWO_PI);

  // Calculer les composantes x et y de la vitesse à partir de l'angle et de la vitesse
  ballSpeedX = speed * cos(angle);
  ballSpeedY = speed * sin(angle);
}
function toggleDifficultMode() {
    difficultMode = !difficultMode;
    if (difficultMode) {
      generateAdditionalBalls();
    }
  }
  
  function generateAdditionalBalls() {
    for (let i = 0; i < 10; i++) {
      const x = random(width);
      const y = random(height);
      const speedX = random(-5, 5);
      const speedY = random(-5, 5);
      const ballColor = color(random(255), random(255), random(255)); // Renommer la variable en ballColor
      additionalBalls.push({ x, y, speedX, speedY, ballColor }); // Mettre à jour la propriété de l'objet en ballColor
    }
  }
  
  
  function updateAdditionalBalls() {
    for (let i = 0; i < additionalBalls.length; i++) {
      const ball = additionalBalls[i];
      ball.x += ball.speedX;
      ball.y += ball.speedY;
  
      if (
        (ball.x - 10 < 0 && ball.speedX < 0) ||
        (ball.x + 10 > width && ball.speedX > 0)
      ) {
        ball.speedX *= -1;
      }
  
      if (
        (ball.y - 10 < 0 && ball.speedY < 0) ||
        (ball.y + 10 > height && ball.speedY > 0)
      ) {
        ball.speedY *= -1;
      }
    }
  }
  
  function drawAdditionalBalls() {
    for (const ball of additionalBalls) {
        fill(ball.ballColor); // Utiliser ball.ballColor au lieu de ball.color
      ellipse(ball.x, ball.y, 20, 20);
    }
  }