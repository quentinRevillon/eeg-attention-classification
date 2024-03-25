import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import MemorizeNumbersGame from './MemorizeNumbersGame';
import './index.css';
// import Game2 from './Game2'; // Uncomment this when you have a second game

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/MemorizeNumbersGame" element={<MemorizeNumbersGame />} />
        <Route path="/game1" element={<MemorizeNumbersGame />} /> {/* Game1 is the component for your first game */}
        <Route path="/game2" element={<MemorizeNumbersGame />} /> {/* Game2 is the component for your second game */}
      </Routes>
    </Router>
  );
}

export default App;