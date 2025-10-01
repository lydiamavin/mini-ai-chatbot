import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [history, setHistory] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    try {
      const res = await axios.post('http://localhost:8000/ask', { question });
      const newAnswer = res.data.answer;
      setAnswer(newAnswer);
      setHistory(prev => [...prev.slice(-9), { q: question, a: newAnswer }]);
      setQuestion('');
    } catch (error) {
      setAnswer('Error: Could not connect to backend.');
    }
  };

  const clearHistory = () => {
    setHistory([]);
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-header">
          <h1>Mini AI Chatbot</h1>
        </div>
        <div className="chat-messages">
          {history.map((item, index) => (
            <div key={index}>
              <div className="message user-message">
                <div className="message-content">{item.q}</div>
              </div>
              <div className="message bot-message">
                <div className="message-content">{item.a}</div>
              </div>
            </div>
          ))}
          {answer && !history.some(h => h.a === answer) && (
            <div className="message bot-message">
              <div className="message-content">{answer}</div>
            </div>
          )}
        </div>
        <div className="chat-input">
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a professional question..."
            />
            <button type="submit">Send</button>
          </form>
          {history.length > 0 && <button className="clear-btn" onClick={clearHistory}>Clear Chat</button>}
        </div>
      </div>
    </div>
  );
}

export default App;