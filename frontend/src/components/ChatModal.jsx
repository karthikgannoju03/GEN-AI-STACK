import React, { useState, useRef, useEffect } from 'react'
import { X, Send, Building, Sparkles } from 'lucide-react'
import { createConversation, sendChatMessage } from '../api'
import toast from 'react-hot-toast'

const ChatModal = ({ onClose, stack, workflow }) => {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (workflow?.id && !conversationId) {
      createConversation(workflow.id)
        .then(({ data }) => setConversationId(data.id))
        .catch(() => toast.error('Failed to start conversation'))
    }
  }, [workflow?.id])

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!inputMessage.trim() || isLoading) return
    if (!conversationId) {
      toast.error('Please wait for conversation to initialize')
      return
    }

    const userContent = inputMessage.trim()
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: userContent,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const { data } = await sendChatMessage(conversationId, userContent)
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: data.response,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, aiMessage])
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to get response'
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        type: 'ai',
        content: `Error: ${errorMsg}`,
        timestamp: new Date()
      }])
      toast.error('Failed to send message')
    } finally {
      setIsLoading(false)
    }
  }

  const formatMessage = (content) => {
    // Simple markdown-like formatting for bold text
    return content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl h-5/6 flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-sm">ai</span>
            </div>
            <span className="text-lg font-semibold text-gray-900">GenAI Stack Chat</span>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {!workflow?.id ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mb-4">
                <Building className="w-8 h-8 text-amber-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Build Your Stack First</h3>
              <p className="text-gray-600">Click &quot;Build Stack&quot; to save your workflow, then you can chat with your AI assistant.</p>
            </div>
          ) : messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mb-4">
                <Sparkles className="w-8 h-8 text-primary-500" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">GenAI Stack Chat</h3>
              <p className="text-gray-600">Start a conversation to test your stack</p>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-3xl px-4 py-3 rounded-lg ${
                    message.type === 'user'
                      ? 'bg-blue-100 text-blue-900'
                      : 'bg-white border border-gray-200 text-gray-900'
                  }`}
                >
                  {message.type === 'user' && (
                    <div className="flex items-center space-x-2 mb-2">
                      <Building className="w-4 h-4 text-blue-600" />
                      <span className="text-xs font-medium text-blue-600">You</span>
                    </div>
                  )}
                  {message.type === 'ai' && (
                    <div className="flex items-center space-x-2 mb-2">
                      <Sparkles className="w-4 h-4 text-primary-500" />
                      <span className="text-xs font-medium text-primary-600">AI Assistant</span>
                    </div>
                  )}
                  <div
                    dangerouslySetInnerHTML={{
                      __html: formatMessage(message.content)
                    }}
                    className="text-sm"
                  />
                </div>
              </div>
            ))
          )}

          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-3xl px-4 py-3 rounded-lg bg-gray-100">
                <div className="flex items-center space-x-2">
                  <Sparkles className="w-4 h-4 text-primary-500" />
                  <span className="text-xs font-medium text-primary-600">AI Assistant</span>
                </div>
                <div className="mt-2 flex items-center space-x-1">
                  <span className="text-sm text-gray-600">Thinking</span>
                  <div className="flex space-x-1">
                    <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-4 border-t border-gray-200">
          <form onSubmit={handleSendMessage} className="flex space-x-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder={workflow?.id ? 'Send a message' : 'Build stack first...'}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              disabled={isLoading || !workflow?.id}
            />
            <button
              type="submit"
              disabled={!inputMessage.trim() || isLoading || !workflow?.id}
              className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default ChatModal
