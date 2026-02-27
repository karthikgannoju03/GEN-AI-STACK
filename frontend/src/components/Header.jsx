import React from 'react'
import { Plus, Settings } from 'lucide-react'

const Header = ({ onNewStack, currentView, onViewChange }) => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-sm">ai</span>
            </div>
            <span className="text-xl font-bold text-gray-900">GenAI Stack</span>
          </div>
          
          {currentView === 'builder' && (
            <nav className="ml-8">
              <button
                onClick={() => onViewChange('stacks')}
                className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                My Stacks
              </button>
            </nav>
          )}
        </div>

        <div className="flex items-center space-x-4">
          <button
            onClick={onNewStack}
            className="bg-primary-500 text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition-colors flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>New Stack</span>
          </button>
          
          <button className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
            <span className="text-white font-bold text-sm">S</span>
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header
