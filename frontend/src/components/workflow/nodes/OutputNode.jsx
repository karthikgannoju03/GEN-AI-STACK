import React, { useState } from 'react'
import { Handle, Position } from 'reactflow'
import { ArrowRight, Settings } from 'lucide-react'

const OutputNode = ({ data, isConnectable }) => {
  const [output, setOutput] = useState(data.output || '')

  const handleOutputChange = (e) => {
    setOutput(e.target.value)
    data.onChange?.({ ...data, output: e.target.value })
  }

  return (
    <div className="bg-white border-2 border-gray-200 rounded-lg shadow-lg min-w-80">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-6 h-6 bg-orange-500 rounded flex items-center justify-center">
              <ArrowRight className="w-4 h-4 text-white" />
            </div>
            <span className="font-semibold text-gray-900">Output</span>
          </div>
          <button className="text-gray-400 hover:text-gray-600">
            <Settings className="w-4 h-4" />
          </button>
        </div>
        <p className="text-sm text-gray-500 mt-1">Output of the result nodes as text</p>
      </div>

      <div className="p-4">
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Output Text
            </label>
            <textarea
              value={output}
              onChange={handleOutputChange}
              placeholder="Output will be generated based on query"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none"
              rows={4}
              readOnly
            />
          </div>
        </div>
      </div>

      <Handle
        type="target"
        position={Position.Left}
        id="output"
        style={{ background: '#10B981', width: 12, height: 12 }}
        isConnectable={isConnectable}
      />
    </div>
  )
}

export default OutputNode
