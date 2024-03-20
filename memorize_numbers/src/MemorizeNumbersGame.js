import React, { useState, useEffect } from 'react';
import './MemorizeNumbersGame.css';

function MemorizeNumbersGame() {
  const [sequence, setSequence] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [showSequence, setShowSequence] = useState(false);
  const [gameStarted, setGameStarted] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [message, setMessage] = useState("");
  const [countdown, setCountdown] = useState(5); // 5 seconds countdown

  function generateSequence() {
    const newSequence = [];
    for (let i = 0; i < 5; i++) {
      newSequence.push(Math.floor(Math.random() * 10));
    }
    setSequence(newSequence);
    setShowSequence(true);
    setCountdown(5); // Start the countdown here
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