const startButton1 = document.getElementById('startButton1');
const startButton2 = document.getElementById('startButton2');
const startButton3 = document.getElementById('startButton3');
const leaderboardBtn = document.getElementById('leaderboardButton');
const logoutButton = document.getElementById('logoutButton');

function redirectGame1() {
    window.location.href = "/congruentTest";
}

function redirectGame2() {
    window.location.href = "/nonCongruentTest";
}

function redirectGame3() {
    window.location.href = "/ballTest";
}

function redirectLeaderboard() {
    window.location.href = "/leaderboard";
}

function redirectPrisha() {
    window.location.href = "/memoryPrisha";
}

function redirectManon() {
    window.location.href = "/memoryManon";
}

function logout() {
    window.location.href = "/logout";
}



startButton1.addEventListener('click', redirectGame1);
startButton2.addEventListener('click', redirectGame2);
startButton3.addEventListener('click', redirectGame3);
leaderboardBtn.addEventListener('click', redirectLeaderboard);
startButtonPrisha.addEventListener('click', redirectPrisha);
startButtonManon.addEventListener('click', redirectManon);
logoutButton.addEventListener('click', logout);
