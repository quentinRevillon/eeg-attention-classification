$(document).ready(function() {
    $("#leaderboard-table").tablesorter();

    document.getElementById('backToMenu').addEventListener('click', function() {
        window.location.href = "/testSelectionPanel";
    });
});
