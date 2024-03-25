import React, { useState, useEffect } from 'react';
import './MemorizeNumbersGame.css';
import './index.css';

function MemorizeNumbersGame() {
  const [sequence, setSequence] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [showSequence, setShowSequence] = useState(false);
  const [gameStarted, setGameStarted] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [message, setMessage] = useState("");
  const [countdown, setCountdown] = useState(5); // 5 seconds countdown
  const [sequenceLength, setSequenceLength] = useState(5); // New state for sequence length


  function generateSequence() {
    const newSequence = [];
    for (let i = 0; i < sequenceLength; i++) { // Use sequenceLength instead of 5
      newSequence.push(Math.floor(Math.random() * 10));
    }
    setSequence(newSequence);
    setShowSequence(true);
    setCountdown(5); // Start the countdown here
  }

  const increaseSequenceLength = () => {
    setSequenceLength(prevLength => prevLength + 1);
  }
  const decreaseSequenceLength = () => {
    setSequenceLength(prevLength => prevLength - 1);
  }

  useEffect(() => {
    let timer;
    if (countdown > 0) {
      timer = setInterval(() => {
        setCountdown(countdown - 1);
      }, 1000);
    } else {
      clearInterval(timer);
      setShowSequence(false); // Hide the sequence when the countdown reaches 0
    }
    return () => clearInterval(timer);
  }, [countdown]);

  function handleInputChange(e) {
    setUserInput(e.target.value);
  }

  function checkAnswer() {
    if (sequence.join('') === userInput) {
      setMessage('Correct!');
    } else {
      setMessage('Incorrect. Try again.');
    }
    setGameOver(true);
  }

  function startGame() {
    setGameStarted(true);
    setGameOver(false);
    setMessage("");
    generateSequence();
  }

  return (
    <div className="game-container">
      {!gameStarted || gameOver ? (
        <div>
          <button onClick={startGame}>Start Game</button>
          <p>Current Sequence Length: {sequenceLength}</p> {/* Display the current sequence length */}
          <button variant="contained" color="primary" onClick={increaseSequenceLength}>
        Increase Sequence Length</button>
          <button variant="contained" color="primary" onClick={decreaseSequenceLength}>
        Decrease Sequence Length </button>
        
          <p>{message}</p>
        </div>
      ) : showSequence ? (
        <div>
          {sequence}
          <div>Countdown: {countdown}</div> {/* Display the countdown with the sequence */}
        </div>
      ) : (
        <div>
          <input type="text" value={userInput} onChange={handleInputChange} />
          <button onClick={checkAnswer}>Enter</button>
      
        </div>
      )}
    </div>
  );
}

export default MemorizeNumbersGame;