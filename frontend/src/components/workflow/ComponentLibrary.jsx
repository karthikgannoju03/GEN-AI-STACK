import React from 'react'
import { User, Brain, BookOpen, ArrowRight, GripVertical } from 'lucide-react'

const ComponentLibrary = () => {
  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', nodeType)
    event.dataTransfer.effectAllowed = 'move'
  }

  const components = [
    {
      type: 'userQuery',
      name: 'User Query',
      icon: User,
      description: 'Enter point for queries',
      color: 'bg-blue-500'
    },
    {
      type: 'knowledgeBase',
      name: 'Knowledge Base',
      icon: BookOpen,
      description: 'Let LLM search info in your file',
      color: 'bg-purple-500'
    },
    {
      type: 'llm',
      name: 'LLM Engine (OpenAI)',
      icon: Brain,
      description: 'Process queries using GPT + optional web search',
      color: 'bg-green-500'
    },
    {
      type: 'output',
      name: 'Output',
      icon: ArrowRight,
      description: 'Output of the result nodes as text',
      color: 'bg-orange-500'
    }
  ]

  return (
    <div>
      <div className="flex items-center space-x-2 mb-6">
        <div className="w-6 h-6 bg-gray-100 rounded flex items-center justify-center">
          <span className="text-gray-600 text-sm">📁</span>
        </div>
        <h2 className="text-lg font-semibold text-gray-900">Chat With AI</h2>
      </div>

      <div className="mb-4">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Components</h3>
        <div className="space-y-2">
          {components.map((component) => {
            const IconComponent = component.icon
            return (
              <div
                key={component.type}
                className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg cursor-move hover:bg-gray-100 transition-colors"
                draggable
                onDragStart={(event) => onDragStart(event, component.type)}
              >
                <div className={`w-8 h-8 ${component.color} rounded-lg flex items-center justify-center`}>
                  <IconComponent className="w-4 h-4 text-white" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900">{component.name}</p>
                  <p className="text-xs text-gray-500">{component.description}</p>
                </div>
                <GripVertical className="w-4 h-4 text-gray-400" />
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default ComponentLibrary
