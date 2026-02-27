import React, { useState } from 'react'
import { Toaster } from 'react-hot-toast'
import Header from './components/Header'
import WorkflowBuilder from './components/WorkflowBuilder'
import ChatModal from './components/ChatModal'
import MyStacks from './components/MyStacks'
import CreateStackModal from './components/CreateStackModal'

// --- CRITICAL FIX: Import ReactFlowProvider ---
// This is necessary to resolve the crash when WorkflowBuilder tries to render.
import { ReactFlowProvider } from 'reactflow'; 
// ----------------------------------------------

function App() {
  const [currentView, setCurrentView] = useState('stacks') // 'stacks' or 'builder'
  const [showChatModal, setShowChatModal] = useState(false)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [currentStack, setCurrentStack] = useState(null)
  const [currentWorkflow, setCurrentWorkflow] = useState(null)

  const handleCreateStack = (stackData) => {
    setShowCreateModal(false)
    setCurrentStack(stackData)
    setCurrentWorkflow(null)
    setCurrentView('builder')
  }

  const handleEditStack = (stack) => {
    setCurrentStack(stack)
    setCurrentWorkflow(null)
    setCurrentView('builder')
  }

  const handleChatWithStack = () => {
    setShowChatModal(true)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        onNewStack={() => setShowCreateModal(true)}
        currentView={currentView}
        onViewChange={setCurrentView}
      />
      
      <main className="container mx-auto px-4 py-6">
        {currentView === 'stacks' && (
          <MyStacks 
            onEditStack={handleEditStack}
            onCreateNew={() => setShowCreateModal(true)}
          />
        )}
        
        {/* --- ReactFlowProvider WRAPS THE WORKFLOW BUILDER --- */}
        {currentView === 'builder' && (
          <ReactFlowProvider>
            <WorkflowBuilder 
              stack={currentStack}
              workflow={currentWorkflow}
              onWorkflowSaved={setCurrentWorkflow}
              onChatWithStack={handleChatWithStack}
            />
          </ReactFlowProvider>
        )}
      </main>

      {showCreateModal && (
        <CreateStackModal 
          onClose={() => setShowCreateModal(false)}
          onCreate={handleCreateStack}
        />
      )}

      {showChatModal && (
        <ChatModal 
          onClose={() => setShowChatModal(false)}
          stack={currentStack}
          workflow={currentWorkflow}
        />
      )}

      <Toaster position="top-right" />
    </div>
  )
}

export default App
