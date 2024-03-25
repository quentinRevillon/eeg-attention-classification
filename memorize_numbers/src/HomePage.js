import React from 'react';
import { useNavigate } from 'react-router-dom';
import './index.css';

const HomePage = () => {
  const navigate = useNavigate();

  const navigateToGame1 = () => {
    navigate('/game1');
  }

  const navigateToGame2 = () => {
    navigate('/game2');
  }

  return (
    <div>
      <button onClick={navigateToGame1}>Play Game 1</button>
      <button onClick={navigateToGame2}>Play Game 2</button>
    </div>
  );
}

export default HomePage;