import React, { useState } from "react";
import Card from "./Card";
import { cardsData } from "../cards_deck";

function Memory() {
  // states
  let [cardsState, setCardsState] = useState(cardsData);
  let [gameStarted, setGameStarted] = useState(false);
  let [gameReady, setGameReady] = useState(false);
  let [cardsFlipped, setCardsFlipped] = useState(false);

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

  const startGame = () => {
    // Reset all states to their initial values
    setCardsState(cardsData);
    setGameStarted(true);
    setGameReady(false);
    setCardsFlipped(false);
    setFirstCard(null);
    setSecondClick(false);
    setWait(false);
    setGameReady(true);
    setGameStarted(true);
  } //Instructions for starting the game


  return (
    <section className="memory-game">
      {!gameReady ? (
        <button onClick={startGame}>Start Game</button>
      ) : (
        cardsState?.map((card) => {
          return (
            <Card
              key={card.id}
              card={cardsFlipped || card.isFlipped ? {...card, isFlipped: true} : card}
              onClick={(e) => handleClick(e, card)}
            />
          );
        })
      )}
    </section>
  );
} //Memory game component

export default Memory;