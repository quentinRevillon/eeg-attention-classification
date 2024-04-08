import React, { useState, useEffect } from 'react';

function SentenceGame() {
    const [sentence, setSentence] = useState('This is a test sentence');
    const [userInput, setUserInput] = useState('');
    const [isCorrect, setIsCorrect] = useState(null);

    useEffect(() => {
        const timer = setTimeout(() => {
            setSentence(null);
        }, 5000); // hide sentence after 5 seconds

        return () => clearTimeout(timer); // clear timer on component unmount
    }, []);

    const handleSubmit = (event) => {
        event.preventDefault();
        setIsCorrect(userInput === sentence);
    };

    const handleChange = (event) => {
        setUserInput(event.target.value);
    };

    return (
        <div>
            {sentence && <p>{sentence}</p>}
            <form onSubmit={handleSubmit}>
                <input type="text" value={userInput} onChange={handleChange} />
                <button type="submit">Submit</button>
            </form>
            {isCorrect !== null && (
                <p>{isCorrect ? 'Correct!' : 'Incorrect, try again.'}</p>
            )}
        </div>
    );
}

export default SentenceGame;