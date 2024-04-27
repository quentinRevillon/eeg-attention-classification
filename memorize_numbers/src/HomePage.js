import React from 'react';
import { useNavigate } from 'react-router-dom';
import './assets/css/index.css';

const HomePage = () => {
  const navigate = useNavigate();

  const navigateToGame1 = () => {
    navigate('/game1');
  }

  const navigateToGame2 = () => {
    navigate('/game2');
  }

  return (
    <div className="game-container">
      <button onClick={navigateToGame1}>Play Memorize Numbers</button>
      <button onClick={navigateToGame2}>Play Memory Game</button>
    </div>
  );
}//HomePage component

export default HomePage;