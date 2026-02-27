import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' }
})

export const createStack = (data) => api.post('/api/stacks', data)
export const getStack = (id) => api.get(`/api/stacks/${id}`)
export const createWorkflow = (data) => api.post('/api/workflows', data)
export const validateAndSaveWorkflow = (workflowId, nodes, edges) =>
  api.post(`/api/workflows/${workflowId}/validate_and_save`, { nodes, edges })
export const createConversation = (workflowId) =>
  api.post('/api/chat/conversations', { workflow_id: workflowId })
export const sendChatMessage = (conversationId, message) =>
  api.post(`/api/chat/conversations/${conversationId}/send`, { message })
