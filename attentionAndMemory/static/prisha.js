//<img src="./images/croix.webp" width="950" height="120" id="monimage" />
var I = "./Prisha/images/";


// Un tableau qui va contenir toutes tes images.
var images1 = [
    I + "clown.jpeg",
    I + "redvelvet.jpeg",
    I + "ballon.jpeg",
    I + "abricots.jpg",
    I + "animalArbre.jpg",
    I + "animalBresil.webp",
    I + "animalCouleur.jpg",
    I + "arbrePommes.jpg",
    I + "bateau.jpeg",
    I + "cerise.jpg",
    I+ "cheval.jpg",
    I + "chevalBlanc.jpeg",
    I + "fruitsExotiques.webp",
    I + "gateauDamier.jpg",
    I + "livre.png",
    I + "myrtillier.jpg",
    I + "oiseaufleurs.jpg",
    I + "paysageFleurs.jpg",
    I+ "poire.jpg",
    I + "pommier.jpg",
    I + "tigre.jpg"
];

var images2 = [
    I + "clown.jpeg",
    I + "redvelvet.jpeg",
    I + "ballon.jpeg",
    I + "arbrePommier.jpg", 
    I + "arbres.jpg",
    I + "abricots.jpg",
    I + "animalArbre.jpg",
    I + "animalBresil.webp",
    I + "animalCouleur.jpg",
    I + "arbrePommes.jpg",
    I + "arbrePommier.jpg",
    I + "arbres.jpg",
    I + "bateau.jpeg",
    I + "cerise.jpg",
    I + "cheval.jpg",
    I + "chevalBlanc.jpeg",
    I + "chevalBlanc2.jpeg",
    I + "crocodile.avif",
    I + "fleursviolettes.jpg",
    I + "fruitsEtLegumes.jpg",
    I + "fruitsExotiques.webp",
    I + "gateauDamier.jpg",
    I + "gateauFraise.jpeg",
    I + "lacMontagne.jpg",
    I + "layercake.webp",
    I + "legumes.jpg",
    I + "lion.png",
    I + "livre.png",
    I + "livrerouge.jpg",
    I + "loup.jpg",
    I + "myrtillier.jpg",
    I + "nature.jpg",
    I + "oiseaufleurs.jpg",
    I + "oiseauxColorés.jpg",
    I + "oranges.webp",
    I + "panda.jpg",
    I + "paysageFleurs.jpg",
    I + "peche.webp",
    I + "poire.jpg",
    I + "poires.webp",
    I + "poirier.jpg",
    I + "pommes.jpg",
    I + "pommier.jpg",
    I + "redvelvet.jpeg",
    I + "tigre.jpg",
    I + "zebre.jpg"
];


var Answers = [
    1,
    1,
    1,
    0,
    0,
    1,
    1,
    1,
    1,
    1,
    0,
    0,
    1,
    1,
    1,
    1,
    0,
    0,
    0,
    0,
    1,
    1,
    0,
    0,
    0,
    0,
    0,
    1,
    0,
    1,
    1,
    0,
    1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    0,
    0,
    1,
    0
]; // 0 if the image is seen 1 if unknown

var pointeur1 = 0;

var currentImageIndex = -1;

var score = 0;
 
function ChangerImage1(){
document.getElementById("monimage").src = images1[pointeur1];
 
if(pointeur1 < images1.length - 1){
pointeur1++;
}

else{
//pointeur = 0;
var nextPhaseButton = document.getElementById("nextPhase")
nextPhaseButton.style.display = "block";
nextPhaseButton.style.margin = "0 auto";
document.getElementById("phase1").style.display = "none";
document.getElementById("phase2").style.display = "block";
console.log('end of Phase 1');
return 'end of Phase 1';
}

 
setTimeout("ChangerImage1()", 2500)
}

function displayFirstImage(){
    currentImageIndex = -1;
    score = 0;
    console.log(currentImageIndex);
    displayNextImage();
}
function displayNextImage(){
    currentImageIndex++;
    if (currentImageIndex < images2.length){
        var currentImageElement = document.getElementById("currentImage");
        currentImageElement.src = images2[currentImageIndex];
    }
    else{
        endGame();
    }

}


    function IncrementScoreSeen(){
        if (Answers[currentImageIndex] == 0){
            score ++;
        }
        displayNextImage();
    }

    function IncrementScoreUnknown(){
        if (Answers[currentImageIndex] == 1){
            score++;
        }
        displayNextImage();
    }

function sendScore(score, gameId){
    fetch('/sendScorePrisha', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({score: score, gameId: gameId}),
    })

}

function endGame(){
    alert("End of game! Your score is :" + score);
    sendScore(score, 1);

}

const sentenceElement = document.getElementById('sentence');
const formElement = document.getElementById('form');
const inputElement = document.getElementById('input');
const resultElement = document.getElementById('result');
const submitButton = document.querySelector('#form button');
const numWordsElement = document.getElementById('numWords');

let words = ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog', 'dog', 'cat', 'car', 'tree', 'book', 'phone', 'computer', 'city', 'bird', 'flower', 'river', 'mountain', 'cloud', 'ocean', 'star', 'forest', 'street', 'island', 'sun', 'moon', 'run', 'jump', 'swim', 'fly', 'read', 'write', 'think', 'dream', 'sing', 'dance', 'laugh', 'cry', 'see', 'hear', 'feel', 'smile', 'frown', 'speak', 'listen', 'walk'];
let sentence;
let currentSentenceIndex = 0;
let score2 = 0;


numWordsElement.addEventListener('change', () => {
    sentence = generateSentences(5, words, Number(numWordsElement.value)); // generate 5 sentences from the words, each sentence is as long as the user wants theme to be
    let currentSentenceIndex = 0;
    currentSentenceIndex = 0;
    score = 0;
    displayNextSentence();
});

function generateSentences(numSentences, words, wordsPerSentence) {
    let sentences = [];
    for (let i = 0; i < numSentences; i++) {
        let sentenceWords = [];
        for (let j = 0; j < wordsPerSentence; j++) {
            let randomIndex = Math.floor(Math.random() * words.length);
            sentenceWords.push(words[randomIndex]);
        }
        sentences.push(sentenceWords.join(' '));
    }
    return sentences;
}


function displayNextSentence() {
    document.getElementById("submissionPhase").style.display = "none";
    if (currentSentenceIndex < sentence.length) {
        submitButton.disabled = false;
        sentenceElement.textContent = sentence[currentSentenceIndex];
        currentSentenceIndex++;
        setTimeout(submissionPhase, 5000); // display next sentence after 5 seconds
    } else {
        sentenceElement.textContent = '';
        endGame2();
    }
}
function submissionPhase(){
    sentenceElement.textContent = '';
    document.getElementById("submissionPhase").style.display = "block";
setTimeout(displayNextSentence, 15000); // hide sentence after 5 seconds
}

// displayNextSentence();

formElement.addEventListener('submit', (event) => {
    event.preventDefault();
    submitButton.disabled = true;
    if (inputElement.value === sentence[currentSentenceIndex - 1]) {
        resultElement.textContent = 'Correct!';
        score2++;
    } else {
        resultElement.textContent = 'Incorrect, try again.';
    }
});

function endGame2(){
    alert("End of game! Your score is :" + score2);
    sendScore(score2, 2);
}

