import React, { useState, useRef, useEffect } from 'react'

const AGENTS = {
  ater: { label: 'ATER', color: 'bg-green-500', icon: '🌱' },
  credito: { label: 'Crédito', color: 'bg-blue-500', icon: '💰' },
  mercado: { label: 'Mercado', color: 'bg-yellow-500', icon: '📦' },
  clima: { label: 'Clima', color: 'bg-sky-500', icon: '☁️' },
  docs: { label: 'Documentos', color: 'bg-purple-500', icon: '📋' },
  territorio: { label: 'Território', color: 'bg-orange-500', icon: '🗺️' },
}

export default function ChatInterface() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [currentAgent, setCurrentAgent] = useState(null)
  const messagesEndRef = useRef(null)
  const mediaRecorderRef = useRef(null)
  const inputRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (text) => {
    if (!text.trim()) return

    const userMessage = { role: 'user', content: text, agent: null }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsTyping(true)

    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text,
          user_id: 'web-user-' + Date.now()
        })
      })
      const data = await res.json()
      setCurrentAgent(data.agent)
      const agentInfo = AGENTS[data.agent] || AGENTS.ater
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response,
        agent: data.agent,
        agentLabel: agentInfo.label,
        agentIcon: agentInfo.icon,
        confidence: data.confidence
      }])
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Desculpe, houve um erro de conexão. Tente novamente.',
        agent: null
      }])
    } finally {
      setIsTyping(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    sendMessage(input)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage(input)
    }
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorderRef.current = new MediaRecorder(stream)
      mediaRecorderRef.current.start()
      setIsRecording(true)
    } catch (err) {
      console.error('Microphone access denied:', err)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  return (
    <div className="flex flex-col h-[600px]">
      <div className="p-4 border-b dark:border-gray-700 bg-gray-50 dark:bg-gray-900 flex items-center justify-between">
        <div>
          <h2 className="font-semibold text-lg">Assistente Agroecológico</h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Powered by AMD MI300X + Llama 3.1
          </p>
        </div>
        {currentAgent && (
          <span className="px-3 py-1 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded-full text-sm">
            {AGENTS[currentAgent]?.icon} {AGENTS[currentAgent]?.label}
          </span>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center py-8 text-gray-500 dark:text-gray-400">
            <div className="text-5xl mb-4">🌱</div>
            <p className="font-medium">Bem-vindo ao AgroFamíliApp!</p>
            <p className="text-sm mt-2">Como posso ajudar na sua propriedade hoje?</p>
            <div className="mt-4 flex flex-wrap justify-center gap-2">
              {['Quando planto milho?', 'Como obter PRONAF?', 'Como certificar produto orgânico?'].map((q) => (
                <button
                  key={q}
                  onClick={() => sendMessage(q)}
                  className="px-3 py-1 text-sm bg-green-50 dark:bg-gray-700 rounded-full hover:bg-green-100 dark:hover:bg-gray-600 transition"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} fade-in`}
          >
            <div className={`chat-message p-3 rounded-2xl ${
              msg.role === 'user'
                ? 'bg-primary-500 text-white rounded-br-sm'
                : 'bg-gray-100 dark:bg-gray-700 rounded-bl-sm'
            }`}>
              {msg.role === 'assistant' && msg.agent && (
                <div className="text-xs mb-1 opacity-70">
                  {msg.agentIcon} {msg.agentLabel}
                </div>
              )}
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex justify-start fade-in">
            <div className="chat-message p-3 rounded-2xl bg-gray-100 dark:bg-gray-700 rounded-bl-sm">
              <div className="typing-indicator flex gap-1">
                <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
                <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
                <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t dark:border-gray-700">
        <div className="flex gap-2">
          <button
            type="button"
            onClick={isRecording ? stopRecording : startRecording}
            className={`p-3 rounded-full transition ${isRecording ? 'bg-red-500 text-white animate-pulse' : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'}`}
            title={isRecording ? 'Stop recording' : 'Start voice recording'}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </button>

          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Digite sua pergunta ou fale..."
            className="flex-1 p-3 border rounded-xl dark:bg-gray-700 dark:border-gray-600 resize-none"
            rows={1}
          />

          <button
            type="submit"
            disabled={!input.trim() && !isRecording}
            className="px-6 py-3 bg-green-500 text-white rounded-xl hover:bg-green-600 disabled:opacity-50 transition font-medium"
          >
            Enviar
          </button>
        </div>
        <p className="text-xs text-gray-400 mt-2 text-center">
          Pressione Enter para enviar, Shift+Enter para nova linha
        </p>
      </form>
    </div>
  )
}