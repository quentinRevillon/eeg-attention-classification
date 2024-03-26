document.getElementById('login-form').addEventListener('submit', function(event) {
    var email = document.getElementById('email').value;
    if (!isValidEmail(email)) {
        var errorMessage = document.getElementById('error-message');
        errorMessage.textContent = 'Adresse e-mail invalide';
        event.preventDefault(); // Empêche l'envoi du formulaire
    }
});

function isValidEmail(email) {
    // Utilisez une expression régulière pour valider l'adresse e-mail
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}
