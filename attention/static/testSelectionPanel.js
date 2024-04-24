const startButton1 = document.getElementById('startButton1');
const startButton2 = document.getElementById('startButton2');
const startButton3 = document.getElementById('startButton3');

function redirectGame1() {
    window.location.href = "/congruentTest";
}

function redirectGame2() {
    window.location.href = "/nonCongruentTest";
}

function redirectGame3() {
    window.location.href = "/ballTest";
}

startButton1.addEventListener('click', redirectGame1);
startButton2.addEventListener('click', redirectGame2);
startButton3.addEventListener('click', redirectGame3);