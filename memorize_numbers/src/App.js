import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import MemorizeNumbersGame from './MemorizeNumbersGame';
import Memory from './components/Game';
import './assets/css/index.css';
import { Link } from 'react-router-dom';


const App = () => {
  return (
    <Router>
      <Link to="/"><button className="home-button">Home</button></Link>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/MemorizeNumbersGame" element={<MemorizeNumbersGame />} />
        <Route path="/game1" element={<MemorizeNumbersGame />} /> {/* Game1 is the component for your first game */}
        <Route path="/game2" element={<Memory />} /> {/* Game2 is the component for your second game */}
      </Routes>
    </Router>
  );
}

export default App;