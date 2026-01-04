'use client';

import { useEffect, useState } from 'react';
import KnowledgeHeatmap from '@/components/KnowledgeHeatmap';
import PositiveSankey from '@/components/PositiveSankey';
import NegativeSankey from '@/components/NegativeSankey';

export default function Home() {
  const [tables, setTables] = useState([]);
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then(res => res.json())
      .then(data => setTables(data.tables))
      .catch(err => console.error("Error fetching tables:", err));
  }, [API_URL]);

  return (
    <main className="min-h-screen bg-red-50 p-8 font-sans text-slate-900">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="border-b border-red-200 pb-4">
          <h1 className="text-3xl font-bold text-red-900">LLM Research Dashboard</h1>
          <p className="text-red-700 font-medium">User Stories & Knowledge Analysis</p>
        </header>

        {/* Database Section */}
        <section className="bg-white rounded-xl shadow-md border border-red-100 p-6">
          <h2 className="text-sm uppercase tracking-wider text-red-600 font-bold mb-4">Database Structure (Tables)</h2>
          <div className="flex flex-wrap gap-3">
            {tables.length > 0 ? (
              tables.map(name => (
                <div 
                  key={name} 
                  className="px-4 py-2 bg-red-100 text-red-800 rounded-lg text-sm font-semibold border border-red-200 hover:bg-red-200 transition-colors"
                >
                  {name}
                </div>
              ))
            ) : (
              <p className="text-red-400 text-sm italic">Loading tables...</p>
            )}
          </div>
        </section>

        {/* Heatmap Section */}
        <section className="bg-white rounded-xl shadow-lg border border-red-100 p-6">
          <div className="mb-6 border-l-4 border-red-600 pl-4">
            <h2 className="text-xl font-bold text-red-900">Knowledge Distribution</h2>
            <p className="text-sm text-red-600">Percentage of participants by proficiency level</p>
          </div>
          <div className="overflow-hidden rounded-lg bg-white p-4">
             <KnowledgeHeatmap />
          </div>
        </section>
        
        {/* Grid for Sankey Charts */}
         <section className="bg-white rounded-xl shadow-lg border border-red-100 p-6">
          <div className="mb-6 border-l-4 border-red-600 pl-4">
            <h2 className="text-xl font-bold text-red-900">Critical Risks & Adoption Barriers</h2>
            <p className="text-sm text-red-600">Identifying concerns regarding reliability and learning impact</p>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <PositiveSankey />
            <NegativeSankey />
          </div>
        </section>
      </div>
    </main>
  );
}