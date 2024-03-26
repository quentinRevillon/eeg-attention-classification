import React, { useState, useEffect } from "react";
import Card from "./Card";
import { cardsData } from "../cards_deck";

function Memory() {
  // states
  let [cardsState, setCardsState] = useState(cardsData);
  let [gameStarted, setGameStarted] = useState(false);
  let [gameReady, setGameReady] = useState(false);

  // kep first card info
  let [firstCard, setFirstCard] = useState(null);
  // is it first click?
  let [secondClick, setSecondClick] = useState(false);
  // set flag to wait for 1500ms
  let [wait, setWait] = useState(false);

  // functions
  const checker = async (card) => {
    if (card.name === firstCard.name) {
      console.log("hellooo");
      card["passed"] = true;
      firstCard["passed"] = true;
      changeCardStatusHandler(card);
      changeCardStatusHandler(firstCard);
    } else {
      setWait(true);
      setTimeout(() => {
        changeCardStatusHandler(card);
        changeCardStatusHandler(firstCard);
        setWait(false);
      }, 1500);
    }
  };

  const changeCardStatusHandler = async (clickedCard) => {
    if (!clickedCard.passed) clickedCard.isFlipped = !clickedCard.isFlipped;
    let index = cardsState.findIndex((card) => card.id === clickedCard.id);
    let newState = [...cardsState];
    newState.splice(index, 1, clickedCard);
    await setCardsState(newState);
  };

  const handleClick = async (e, clickedCard) => {
    if (wait) {
      return;
    }
    if (!secondClick) {
      await setFirstCard(clickedCard);
      await setSecondClick(true);
      changeCardStatusHandler(clickedCard);
    } else {
      await setSecondClick(false);
      changeCardStatusHandler(clickedCard);
      checker(clickedCard);
      setFirstCard(null);
    }
  };

   // Show all cards for 2 seconds before the game starts
   useEffect(() => {
    if (gameReady) {
      let newCardsState = cardsState.map(card => ({ ...card, isFlipped: true }));
      setCardsState(newCardsState);
  
      const timer = setTimeout(() => {
        setGameStarted(true);
        newCardsState = newCardsState.map(card => ({ ...card, isFlipped: false }));
        setCardsState(newCardsState);
      }, 2);
      return () => clearTimeout(timer); // This will clear the timer when the component unmounts
    }
  }, [gameReady]);

  const startGame = () => {
    setGameReady(true);
    const timer = setTimeout(() => {
      setGameStarted(true);
      cardsState.forEach(card => {
        card.isFlipped = false;
      });
      setCardsState([...cardsState]);
    }, 2000);
    return () => clearTimeout(timer); // This will clear the timer when the component unmounts
  }

  return (
    <section className="memory-game">
      {!gameReady ? (
        <button onClick={startGame}>Start Game</button>
      ) : (
        cardsState?.map((card) => {
          return (
            <Card
              key={card.id}
              card={card.isFlipped || !gameStarted ? card : {...card, isFlipped: true}}
              onClick={(e) => handleClick(e, card)}
            />
          );
        })
      )}
    </section>
  );
}

export default Memory;