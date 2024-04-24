const startButton1 = document.getElementById('startButton1');
const startButton2 = document.getElementById('startButton2');

function redirectGame1() {
    window.location.href = "/congruentTest";
}

function redirectGame2() {
    window.location.href = "/nonCongruentTest";
}

startButton1.addEventListener('click', redirectGame1);
startButton2.addEventListener('click', redirectGame2);