import React, { useState, useCallback, useRef } from 'react'
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  // Removed Node, Edge, typeConnection, NodeTypes, EdgeTypes as they cause the SyntaxError in JS/JSX
} from 'reactflow'
import 'reactflow/dist/style.css'

// Importing icons/utilities
import { MessageCircle, Save } from 'lucide-react'

import ComponentLibrary from './workflow/ComponentLibrary'
import { createWorkflow, validateAndSaveWorkflow } from '../api'
import toast from 'react-hot-toast'
import UserQueryNode from './workflow/nodes/UserQueryNode'
import KnowledgeBaseNode from './workflow/nodes/KnowledgeBaseNode'
import LLMNode from './workflow/nodes/LLMNode'
import OutputNode from './workflow/nodes/OutputNode'


const CustomNodeTypes = {
  userQuery: UserQueryNode,
  knowledgeBase: KnowledgeBaseNode,
  llm: LLMNode,
  output: OutputNode,
};


const WorkflowBuilder = ({ stack, workflow, onWorkflowSaved, onChatWithStack }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [selectedNode, setSelectedNode] = useState(null)
  const reactFlowWrapper = useRef(null)
  const [reactFlowInstance, setReactFlowInstance] = useState(null)

  // --- Handlers ---
  const onConnect = useCallback(
   (params) => setEdges((eds) => addEdge(params, eds)),
   [setEdges]
   );

  const onDragOver = useCallback((event) => {
    event.preventDefault()
    event.dataTransfer.dropEffect = 'move'
  }, [])

  const onDrop = useCallback(
    (event) => {
      event.preventDefault()

      const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect()
      const type = event.dataTransfer.getData('application/reactflow')

      if (typeof type === 'undefined' || !type) {
        return
      }

      // Ensure reactFlowInstance is initialized before calling project
      if (!reactFlowInstance) return;

      const position = reactFlowInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      })

      const newNode = {
        id: `${type}-${Date.now()}`,
        type,
        position,
        data: { label: `${type} Node` },
      }

      setNodes((nds) => nds.concat(newNode))
    },
    [reactFlowInstance, setNodes]
  )

  const onNodeClick = useCallback((event, node) => {
    setSelectedNode(node)
  }, [])

  const onPaneClick = useCallback(() => {
    setSelectedNode(null)
  }, [])

  const [isBuilding, setIsBuilding] = useState(false)

  const handleBuildStack = async () => {
    const hasUserQuery = nodes.some(node => node.type === 'userQuery')
    const hasLLM = nodes.some(node => node.type === 'llm')
    const hasOutput = nodes.some(node => node.type === 'output')

    if (!hasUserQuery || !hasLLM || !hasOutput) {
      toast.error('Workflow must include User Query, LLM, and Output components')
      return
    }
    if (!stack?.id) {
      toast.error('No stack selected. Create a stack first.')
      return
    }

    setIsBuilding(true)
    try {
      if (workflow?.id) {
        await validateAndSaveWorkflow(workflow.id, nodes, edges)
        toast.success('Stack updated successfully')
      } else {
        const { data } = await createWorkflow({
          stack_id: stack.id,
          name: stack.name || 'Workflow',
          description: stack.description || '',
          nodes,
          edges
        })
        onWorkflowSaved?.(data)
        toast.success('Stack built successfully. You can now chat!')
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to build stack')
    } finally {
      setIsBuilding(false)
    }
  }

  return (
    <div className="flex h-screen">
      {/* Component Library (Left Panel) */}
      <div className="w-80 bg-white border-r border-gray-200 p-4">
        <ComponentLibrary />
      </div>

      {/* Main Canvas (Center Panel) */}
      <div className="flex-1 relative" ref={reactFlowWrapper}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onInit={setReactFlowInstance}
          onDrop={onDrop}
          onDragOver={onDragOver}
          onNodeClick={onNodeClick}
          onPaneClick={onPaneClick}
          nodeTypes={CustomNodeTypes}
          fitView
        >
          <Controls />
          <MiniMap />
          <Background variant="dots" gap={12} size={1} />
        </ReactFlow>

        {/* Execution Controls (Bottom Right) */}
        <div className="absolute bottom-4 right-4 flex space-x-2">
          <button
            onClick={handleBuildStack}
            disabled={isBuilding}
            className="bg-primary-500 text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition-colors flex items-center space-x-2 shadow-md disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            <span>{isBuilding ? 'Building...' : 'Build Stack'}</span>
          </button>
          
          <button
            onClick={onChatWithStack}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors flex items-center space-x-2 shadow-md"
          >
            <MessageCircle className="w-4 h-4" />
            <span>Chat with Stack</span>
          </button>
        </div>
      </div>
      
      {/* Right Configuration Panel (Placeholder) */}
      {/* You will add the ConfigPanel component here */}
    </div>
  )
}

export default WorkflowBuilder