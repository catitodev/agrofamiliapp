import React from 'react'

const quickActions = [
  { label: 'ATER', icon: '🌱', description: 'Technical assistance' },
  { label: 'CRÉDITO', icon: '💰', description: 'Rural credit' },
  { label: 'MERCADO', icon: '📦', description: 'Market & sales' },
  { label: 'CLIMA', icon: '☁️', description: 'Weather forecast' },
  { label: 'DOCS', icon: '📋', description: 'Documentation' },
  { label: 'TERRITÓRIO', icon: '🗺️', description: 'Rural services' },
]

export default function Sidebar({ open, setOpen }) {
  return (
    <aside className={`${open ? 'w-64' : 'w-0'} transition-all duration-300 overflow-hidden bg-white dark:bg-gray-800 border-r dark:border-gray-700`}>
      <div className="p-4">
        <h2 className="text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase mb-3">Ações Rápidas</h2>
        <div className="space-y-2">
          {quickActions.map((action) => (
            <button
              key={action.label}
              className="w-full flex items-center gap-3 p-3 rounded-lg hover:bg-green-50 dark:hover:bg-gray-700 transition text-left"
              onClick={() => {}}
            >
              <span className="text-2xl">{action.icon}</span>
              <div>
                <div className="font-medium text-sm">{action.label}</div>
                <div className="text-xs text-gray-500 dark:text-gray-400">{action.description}</div>
              </div>
            </button>
          ))}
        </div>

        <div className="mt-6 p-4 bg-green-50 dark:bg-gray-700 rounded-lg">
          <h3 className="font-semibold text-green-700 dark:text-green-400 mb-2">Dica</h3>
          <p className="text-xs text-gray-600 dark:text-gray-300">
            Pergunte em voz ou texto. Ex: "Quando planto milho no Sertão?"
          </p>
        </div>
      </div>
    </aside>
  )
}