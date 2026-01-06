'use client';

import React, { useState } from 'react';
import SkillBoxPlot from './SkillBoxPlot';

const skills = ["sw_project_mgmt", "requirements", "agile_methods", "llm_usage"];

const SkillBoxPlotSection: React.FC = () => {
  const [selectedSkill, setSelectedSkill] = useState(skills[0]);

  // Função para traduzir skill para título amigável
  const skillLabel = (skill: string) => {
    switch (skill) {
      case "sw_project_mgmt": return "Software Project Management";
      case "requirements": return "Requirements";
      case "agile_methods": return "Agile Methods";
      case "llm_usage": return "LLM Usage";
      default: return skill;
    }
  };

  return (
    <section className="bg-white rounded-xl shadow-lg border border-red-100 p-6">
      {/* Header */}
      <div className="mb-6 border-l-4 border-red-600 pl-4">
        <h2 className="text-xl font-bold text-red-900">Task Analysis by Skill</h2>
        <p className="text-sm text-red-600">
          Compare time and grades by participant knowledge level (LLM tasks only)
        </p>
      </div>

      {/* Dropdown */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-red-700 mb-1">
          Select Skill:
        </label>
        <select
          className="border border-red-300 rounded-lg p-2 text-sm text-red-900 focus:outline-none focus:ring-2 focus:ring-red-500"
          value={selectedSkill}
          onChange={(e) => setSelectedSkill(e.target.value)}
        >
          {skills.map((s) => (
            <option key={s} value={s}>
              {skillLabel(s)}
            </option>
          ))}
        </select>
      </div>

      {/* BoxPlots Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <SkillBoxPlot
          skill={selectedSkill}
          type="time"
          xLabels={["Low", "Medium", "High"]}
          title="Execution Time (minutes)"
        />
        <SkillBoxPlot
          skill={selectedSkill}
          type="grade"
          xLabels={["Low", "Medium", "High"]}
          title="Grades"
        />
      </div>
    </section>
  );
};

export default SkillBoxPlotSection;
