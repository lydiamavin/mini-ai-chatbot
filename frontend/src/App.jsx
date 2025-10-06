import { useState } from 'react'
import axios from 'axios'

function App() {
  const [question, setQuestion] = useState('')
  const [history, setHistory] = useState([])

  const askQuestion = async () => {
    if (!question.trim()) return

    try {
      const response = await axios.post('/ask', { question })
      const newEntry = { question, answer: response.data.answer }
      setHistory(prev => [...prev, newEntry].slice(-9)) // Keep last 9, oldest first
      setQuestion('')
    } catch (error) {
      console.error('Error asking question:', error)
    }
  }

  return (
    <div className="app">
      <h1>Mini AI Chatbot</h1>
       <div className="chat-container">
        <div className="history">
          {history.flatMap((entry, index) => [
            <div key={`question-${index}`} className="message user">{entry.question}</div>,
            <div key={`answer-${index}`} className="message bot">{entry.answer}</div>
          ])}
        </div>
         <div className="input-section">
           <input
             type="text"
             value={question}
             onChange={(e) => setQuestion(e.target.value)}
             placeholder="Ask a professional question..."
             onKeyPress={(e) => e.key === 'Enter' && askQuestion()}
           />
           <button onClick={askQuestion}>Send</button>
         </div>
       </div>
    </div>
  )
}

export default App