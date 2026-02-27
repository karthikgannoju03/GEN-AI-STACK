import React, { useState } from 'react'
import { Handle, Position } from 'reactflow'
import { Brain, Settings, Eye, EyeOff, ChevronUp, ChevronDown } from 'lucide-react'

const LLMNode = ({ data, isConnectable }) => {
  const [config, setConfig] = useState({
    model: data.model || 'gpt-4o-mini',
    apiKey: data.apiKey || '',
    prompt: data.prompt || 'You are a helpful assistant. Use the provided context to answer the user query.\n\nContext: {context}\nUser Query: {query}',
    temperature: data.temperature || 0.75,
    webSearchEnabled: data.webSearchEnabled || false,
    serpApiKey: data.serpApiKey || '',
    showApiKey: false,
    showSerpApiKey: false
  })

  const handleConfigChange = (field, value) => {
    setConfig(prev => ({ ...prev, [field]: value }))
    data.onChange?.({ ...data, [field]: value })
  }

  const toggleApiKeyVisibility = () => {
    setConfig(prev => ({ ...prev, showApiKey: !prev.showApiKey }))
  }

  const toggleSerpApiKeyVisibility = () => {
    setConfig(prev => ({ ...prev, showSerpApiKey: !prev.showSerpApiKey }))
  }

  const adjustTemperature = (direction) => {
    const newTemp = direction === 'up'
      ? Math.min(2, config.temperature + 0.1)
      : Math.max(0, config.temperature - 0.1)
    handleConfigChange('temperature', newTemp)
  }

  return (
    <div className="bg-white border-2 border-gray-200 rounded-lg shadow-lg min-w-80">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-6 h-6 bg-green-500 rounded flex items-center justify-center">
              <Brain className="w-4 h-4 text-white" />
            </div>
            <span className="font-semibold text-gray-900">LLM Engine (OpenAI)</span>
          </div>
          <button className="text-gray-400 hover:text-gray-600">
            <Settings className="w-4 h-4" />
          </button>
        </div>
        <p className="text-sm text-gray-500 mt-1">Answers from PDF context via GPT. Toggle web search for fallback.</p>
      </div>

      <div className="p-4">
        <div className="space-y-4">
          {/* Model Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Model
            </label>
            <select
              value={config.model}
              onChange={(e) => handleConfigChange('model', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value="gpt-4o-mini">GPT 4o - Mini</option>
              <option value="gpt-4o">GPT 4o</option>
              <option value="gpt-3.5-turbo">GPT 3.5 Turbo</option>
              <option value="gpt-4">GPT 4</option>
            </select>
          </div>

          {/* API Key */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              API Key
            </label>
            <div className="relative">
              <input
                type={config.showApiKey ? 'text' : 'password'}
                value={config.apiKey}
                onChange={(e) => handleConfigChange('apiKey', e.target.value)}
                placeholder="Enter your OpenAI API key"
                className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={toggleApiKeyVisibility}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {config.showApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Prompt */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Prompt
            </label>
            <textarea
              value={config.prompt}
              onChange={(e) => handleConfigChange('prompt', e.target.value)}
              placeholder="Enter your prompt template"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none"
              rows={4}
            />
          </div>

          {/* Temperature */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Temperature
            </label>
            <div className="flex items-center space-x-2">
              <button
                type="button"
                onClick={() => adjustTemperature('down')}
                className="p-1 text-gray-400 hover:text-gray-600"
              >
                <ChevronDown className="w-4 h-4" />
              </button>
              <input
                type="number"
                value={config.temperature}
                onChange={(e) => handleConfigChange('temperature', parseFloat(e.target.value))}
                min="0"
                max="2"
                step="0.1"
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => adjustTemperature('up')}
                className="p-1 text-gray-400 hover:text-gray-600"
              >
                <ChevronUp className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Web Search Tool */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-sm font-medium text-gray-700">
                Web Search Fallback (SerpAPI)
              </label>
              <button
                type="button"
                onClick={() => handleConfigChange('webSearchEnabled', !config.webSearchEnabled)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${config.webSearchEnabled ? 'bg-green-500' : 'bg-gray-200'
                  }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${config.webSearchEnabled ? 'translate-x-6' : 'translate-x-1'
                    }`}
                />
              </button>
            </div>

            {config.webSearchEnabled && (
              <div className="mt-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  SERP API
                </label>
                <div className="relative">
                  <input
                    type={config.showSerpApiKey ? 'text' : 'password'}
                    value={config.serpApiKey}
                    onChange={(e) => handleConfigChange('serpApiKey', e.target.value)}
                    placeholder="Enter your SERP API key"
                    className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                  <button
                    type="button"
                    onClick={toggleSerpApiKeyVisibility}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {config.showSerpApiKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <Handle
        type="target"
        position={Position.Left}
        id="query"
        style={{ background: '#3B82F6', width: 12, height: 12 }}
        isConnectable={isConnectable}
      />
      <Handle
        type="target"
        position={Position.Left}
        id="context"
        style={{ background: '#8B5CF6', width: 12, height: 12, top: 40 }}
        isConnectable={isConnectable}
      />
      <Handle
        type="source"
        position={Position.Bottom}
        id="output"
        style={{ background: '#10B981', width: 12, height: 12 }}
        isConnectable={isConnectable}
      />
    </div>
  )
}

export default LLMNode
