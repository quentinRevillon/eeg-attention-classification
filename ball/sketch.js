let ballX = 0;
let ballY = 0;
let ballSpeedX = 0;
let ballSpeedY = 0;
let squareSize = 400;
let rebounds = 0;
let gameStarted = false;
let gameEnded = false;
let timer = 60;

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
  timer = 10;
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
