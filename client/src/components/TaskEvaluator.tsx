'use client'

import { useState } from 'react'

type Task = {
  code: string
  description: string
  main_flow: string
  alt_flow: string
}

type Evaluation = {
  score: number
  comment: string | null
}

type ApiResponse = {
  task: Task
  evaluation: Evaluation
}

export default function TaskEvaluator() {
  const [code, setCode] = useState('')
  const [data, setData] = useState<ApiResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'

  async function evaluate() {
    setLoading(true)
    setData(null)
    setError(null)

    try {
      const res = await fetch(`${API_URL}/task_evaluate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      })

      if (!res.ok) {
        throw new Error('Failed to evaluate task')
      }

      const json: ApiResponse = await res.json()
      setData(json)

    } catch (err: any) {
      setError(err.message || 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="bg-white rounded-xl shadow-lg border border-red-100 p-6 max-w-3xl mx-auto">
      <h2 className="text-xl font-bold text-red-900 mb-4">Evaluate User Story</h2>

      {/* Input */}
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Enter task code e.g. P001"
          className="flex-1 px-3 py-2 border border-red-200 rounded-md focus:outline-none focus:ring-2 focus:ring-red-400"
        />
        <button
          onClick={evaluate}
          disabled={!code || loading}
          className="px-4 py-2 bg-red-700 text-white font-semibold rounded-md hover:bg-red-800 disabled:bg-red-300"
        >
          {loading ? 'Evaluating...' : 'Evaluate'}
        </button>
      </div>

      {/* Error */}
      {error && (
        <p className="text-red-600 font-medium mb-4">{error}</p>
      )}

      {/* Result */}
      {data && (
        <div className="space-y-6">
          {/* Task Info */}
          <div className="border border-red-200 rounded-lg p-4 bg-red-50">
            <h3 className="font-bold text-red-800 mb-2">Task Information</h3>
            <p><b>Code:</b> {data.task.code}</p>
            <p><b>Description:</b> {data.task.description}</p>

            <div className="mt-2">
              <h4 className="font-semibold text-red-700">Main Flow:</h4>
              <pre className="bg-white p-2 rounded border border-red-100 whitespace-pre-wrap break-words">
                {data.task.main_flow}
              </pre>
            </div>

            <div className="mt-2">
              <h4 className="font-semibold text-red-700">Alternative Flow:</h4>
              <pre className="bg-white p-2 rounded border border-red-100 whitespace-pre-wrap break-words">
                {data.task.alt_flow}
              </pre>
            </div>
          </div>

          {/* Evaluation */}
          <div className="border border-red-200 rounded-lg p-4 bg-red-50">
            <h3 className="font-bold text-red-800 mb-2">Evaluation</h3>
            <p>
              <b>Score:</b>{' '}
              <span className={`font-bold ${
                data.evaluation.score === 10
                  ? 'text-green-600'
                  : data.evaluation.score >= 5
                  ? 'text-yellow-600'
                  : 'text-red-600'
              }`}>
                {data.evaluation.score}
              </span>
            </p>

            <p className="mt-2">
              <b>Comment:</b> {data.evaluation.comment || 'No comment provided'}
            </p>
          </div>
        </div>
      )}
    </section>
  )
}
