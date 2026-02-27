import React, { useState } from 'react'
import { Handle, Position } from 'reactflow'
import { User, Settings } from 'lucide-react'

const UserQueryNode = ({ data, isConnectable }) => {
  const [query, setQuery] = useState(data.query || '')

  const handleQueryChange = (e) => {
    setQuery(e.target.value)
    data.onChange?.({ ...data, query: e.target.value })
  }

  return (
    <div className="bg-white border-2 border-gray-200 rounded-lg shadow-lg min-w-80">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-6 h-6 bg-blue-500 rounded flex items-center justify-center">
              <User className="w-4 h-4 text-white" />
            </div>
            <span className="font-semibold text-gray-900">User Query</span>
          </div>
          <button className="text-gray-400 hover:text-gray-600">
            <Settings className="w-4 h-4" />
          </button>
        </div>
        <p className="text-sm text-gray-500 mt-1">Enter point for queries</p>
      </div>

      <div className="p-4">
        <div className="space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              User Query
            </label>
            <textarea
              value={query}
              onChange={handleQueryChange}
              placeholder="Write your query here"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows={3}
            />
          </div>
        </div>
      </div>

      <Handle
        type="source"
        position={Position.Bottom}
        id="query"
        style={{ background: '#3B82F6', width: 12, height: 12 }}
        isConnectable={isConnectable}
      />
    </div>
  )
}

export default UserQueryNode
