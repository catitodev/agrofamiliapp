import React, { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import NavBar from './components/NavBar'
import Sidebar from './components/Sidebar'

function App() {
  const [darkMode, setDarkMode] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-200">
        <NavBar darkMode={darkMode} setDarkMode={setDarkMode} />

        <div className="flex">
          <Sidebar
            open={sidebarOpen}
            setOpen={setSidebarOpen}
          />

          <main className="flex-1 p-4">
            <div className="max-w-4xl mx-auto">
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
                <ChatInterface />
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}

export default App