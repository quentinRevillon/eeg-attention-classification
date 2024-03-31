//<img src="croix.webp" width="950" height="120" id="monimage" />
 

// Un tableau qui va contenir toutes tes images.
var images1 = [
    "clown.jpeg",
    "redvelvet.jpeg",
    "ballon.jpeg"
];

var images2 = [
    "clown.jpeg",
    "redvelvet.jpeg",
    "ballon.jpeg"
];

var Answers = [0,1,0]; // 0 if the image is seen 1 if unknown

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

 
setTimeout("ChangerImage1()", 1000)
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

function endGame(){
    alert("End of game! Your score is :" + score);
}

