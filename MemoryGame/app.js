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

var pointeur1 = 0;

var pointeur2 = 0;
 
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
 

function ChangerImage2(){
    document.getElementById("monimage2").src = images2[pointeur2];
     
    if(pointeur2 < images2.length - 1){
    pointeur2++;
    }
    
    else{
    //pointeur = 0;
    console.log('end of Phase 2');
    return 'end of Phase 2';
    }
    
     
    setTimeout("ChangerImage2()", 1000)
    }

// Define your sequence of strings
var sequence = ["String 1", "String 2", "String 3", "String 4"];

// Get a reference to the container element
var sequenceContainer = document.getElementById("sequenceContainer");
/*
function ChangeSequence(){
// Loop through the sequence array and create HTML elements for each string
sequence.forEach(function(string,index) {
    setTimeout(function(){
    // Create a new paragraph element
    var paragraph = document.createElement("p");
    // Set the text content of the paragraph to the current string
    paragraph.textContent = string;
    // Append the paragraph to the container element
    sequenceContainer.appendChild(paragraph);
    }, index * 2000);
});
}
*/


var pointeur_seq = 0;
function ChangeSequence(){
    console.log('start');
     var paragraph = document.createElement("p");
     paragraph.textContent = sequence[pointeur_seq];
     while (sequenceContainer.firstChild) {
        sequenceContainer.removeChild(sequenceContainer.firstChild);
    }
     sequenceContainer.appendChild(paragraph);

    if(pointeur_seq < sequence.length - 1){
        pointeur_seq++;
        setTimeout(ChangeSequence, 1000);
    }
    
    else{
        var nextPhaseButton = document.getElementById("secondsequence")
        secondsequenceButton.style.display = "block";
        secondsequenceButton.style.margin = "0 auto";
        document.getElementById("firstsequence").style.display = "none";
        document.getElementById("secondsequence").style.display = "block";
        console.log('end of Phase 1/firstsequence');

        return pointeur_seq = 0;
    }
    }

    function checkSequence(){
        var correctSequence = sequence[pointeur_seq];
        var userInput = document.getElementById("userInput").value;
        var resultMessage = document.getElementById("resultMessage");

        if (userInput == correctSequence){
            resultMessage.textContent = "Correct sequence!";
        } else {
            resultMessage.textContent = "Incorrect Sequence";
        }
        if (pointeur_seq < sequence.length - 1){
            pointeur_seq++;
            setTimeout(CheckSequence, 1000);

        }
        else{
            console.log("end of Phase 2");
        }


    } 

