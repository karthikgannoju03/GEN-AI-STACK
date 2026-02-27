import React from 'react'
import { Plus } from 'lucide-react'
import { Toaster, toast } from 'react-hot-toast' // Added toast for user feedback

const MyStacks = ({ onEditStack, onCreateNew }) => {
  // NOTE: Mock data is REMOVED to force the clean landing page.
  // In the real app, you would fetch the stack data here.
  const stacks = [] // Force empty array to show the create view

  // If there are actual stacks, we would typically display them here.
  // For the assignment's initial clean state, we focus on the central prompt.

  // --- Render the central Create Stack call to action ---
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-120px)] p-6">
      
      {/* Professional Message */}
      <div className="text-center mb-10">
        <h1 className="text-4xl font-extrabold text-gray-800 mb-4">
          Start Building Your GenAI Stack
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Unleash the power of AI by designing custom workflows with our intuitive 
          drag-and-drop builder—the **low-code/no-code way** to innovate.
        </p>
      </div>

      {/* Central Create Stack Button */}
      <button
        onClick={onCreateNew} // This triggers the CreateStackModal in App.jsx
        className="bg-primary-500 text-white px-10 py-5 rounded-xl shadow-xl 
                   hover:bg-primary-600 transition-colors duration-300 
                   flex items-center space-x-3 text-2xl font-bold
                   transform hover:scale-105"
      >
        <Plus className="w-8 h-8" />
        <span>Create New Stack</span>
      </button>
      
      {/* Optional: Add a simple message if the user wants to see the list view later */}
      {/* {stacks.length > 0 && (
          <div className="mt-8">
              <h2 className="text-lg font-semibold text-gray-700">Your Existing Stacks:</h2>
              // ... Display small stack cards here
          </div>
      )} */}
    </div>
  )
}

export default MyStacks
