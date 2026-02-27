import React, { useState } from 'react'
import { Handle, Position } from 'reactflow'
import { BookOpen, Settings, Upload, Trash2, Eye, EyeOff } from 'lucide-react'

const KnowledgeBaseNode = ({ data, isConnectable }) => {
  const [config, setConfig] = useState({
    file: data.file || null,
    embeddingModel: data.embeddingModel || 'text-embedding-3-large',
    apiKey: data.apiKey || '',
    showApiKey: false
  })

  const handleFileUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      setConfig(prev => ({ ...prev, file }))
      data.onChange?.({ ...data, file })
    }
  }

  const handleRemoveFile = () => {
    setConfig(prev => ({ ...prev, file: null }))
    data.onChange?.({ ...data, file: null })
  }

  const handleConfigChange = (field, value) => {
    setConfig(prev => ({ ...prev, [field]: value }))
    data.onChange?.({ ...data, [field]: value })
  }

  const toggleApiKeyVisibility = () => {
    setConfig(prev => ({ ...prev, showApiKey: !prev.showApiKey }))
  }

  return (
    <div className="bg-white border-2 border-gray-200 rounded-lg shadow-lg min-w-80">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-6 h-6 bg-purple-500 rounded flex items-center justify-center">
              <BookOpen className="w-4 h-4 text-white" />
            </div>
            <span className="font-semibold text-gray-900">Knowledge Base</span>
          </div>
          <button className="text-gray-400 hover:text-gray-600">
            <Settings className="w-4 h-4" />
          </button>
        </div>
        <p className="text-sm text-gray-500 mt-1">Let LLM search info in your file</p>
      </div>

      <div className="p-4">
        <div className="space-y-4">
          {/* File Upload */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              File for Knowledge Base
            </label>
            {config.file ? (
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                <span className="text-sm text-gray-700">{config.file.name}</span>
                <button
                  onClick={handleRemoveFile}
                  className="text-red-500 hover:text-red-700"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="border-2 border-dashed border-gray-300 rounded-md p-4 text-center">
                <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                <button
                  onClick={() => document.getElementById('file-upload').click()}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  Upload File
                </button>
                <input
                  id="file-upload"
                  type="file"
                  accept=".pdf,.txt,.doc,.docx"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </div>
            )}
          </div>

          {/* Embedding Model */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Embedding Model
            </label>
            <select
              value={config.embeddingModel}
              onChange={(e) => handleConfigChange('embeddingModel', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="text-embedding-3-large">text-embedding-3-large</option>
              <option value="text-embedding-3-small">text-embedding-3-small</option>
              <option value="text-embedding-ada-002">text-embedding-ada-002</option>
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
                placeholder="Enter your API key"
                className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
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
        type="source"
        position={Position.Bottom}
        id="context"
        style={{ background: '#8B5CF6', width: 12, height: 12 }}
        isConnectable={isConnectable}
      />
    </div>
  )
}

export default KnowledgeBaseNode
