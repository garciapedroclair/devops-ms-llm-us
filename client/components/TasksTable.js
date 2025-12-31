import { useState, useEffect } from "react";

export default function TasksTable() {
  const [tasks, setTasks] = useState([]);
  const [filters, setFilters] = useState({
    code: "",
    group: "",
    task_id: "",
    llm: "all",
  });
  const [expanded, setExpanded] = useState({});

  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    fetch(`${API_URL}/tasks`)
      .then((res) => res.json())
      .then((data) => setTasks(data))
      .catch((err) => console.error("Erro ao buscar tasks:", err));
  }, [API_URL]);

  const toggleExpand = (id) => {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const handleFilterChange = (field, value) => {
    setFilters((prev) => ({ ...prev, [field]: value }));
  };

  // Filtragem por coluna
  const filteredTasks = tasks.filter((task) => {
    const codeMatch = task.code.toLowerCase().includes(filters.code.toLowerCase());
    const groupMatch = task.group.toLowerCase().includes(filters.group.toLowerCase());
    const taskIdMatch = task.task_id.toLowerCase().includes(filters.task_id.toLowerCase());

    const llmMatch =
      filters.llm === "all" ||
      (filters.llm === "yes" && task.llm) ||
      (filters.llm === "no" && !task.llm);

    return codeMatch && groupMatch && taskIdMatch && llmMatch;
  });

  return (
    <div className="w-full">
      <table className="min-w-full border border-gray-400 bg-white text-gray-900">
        <thead className="bg-gray-200">
          <tr>
            <th className="px-4 py-2 border border-gray-400">Code</th>
            <th className="px-4 py-2 border border-gray-400">Group</th>
            <th className="px-4 py-2 border border-gray-400">Task ID</th>
            <th className="px-4 py-2 border border-gray-400">LLM</th>
            <th className="px-4 py-2 border border-gray-400">Time (min)</th>
            <th className="px-4 py-2 border border-gray-400">Grade (Mean)</th>
            <th className="px-4 py-2 border border-gray-400">Actions</th>
          </tr>

          {/* Filtros por coluna */}
          <tr className="bg-gray-100">
            {/* Code */}
            <th className="px-2 py-1 border border-gray-400">
              <input
                type="text"
                placeholder="Filtrar Code"
                className="p-1 border border-gray-400 rounded w-full text-black bg-gray-100"
                value={filters.code}
                onChange={(e) => handleFilterChange("code", e.target.value)}
              />
            </th>

            {/* Group */}
            <th className="px-2 py-1 border border-gray-400">
              <input
                type="text"
                placeholder="Filtrar Group"
                className="p-1 border border-gray-400 rounded w-full text-black bg-gray-100"
                value={filters.group}
                onChange={(e) => handleFilterChange("group", e.target.value)}
              />
            </th>

            {/* Task ID */}
            <th className="px-2 py-1 border border-gray-400">
              <input
                type="text"
                placeholder="Filtrar Task ID"
                className="p-1 border border-gray-400 rounded w-full text-black bg-gray-100"
                value={filters.task_id}
                onChange={(e) => handleFilterChange("task_id", e.target.value)}
              />
            </th>

            {/* LLM */}
            <th className="px-2 py-1 border border-gray-400">
              <select
                className="p-1 border border-gray-400 rounded w-full text-black bg-gray-100"
                value={filters.llm}
                onChange={(e) => handleFilterChange("llm", e.target.value)}
              >
                <option value="all">Todos</option>
                <option value="yes">Yes</option>
                <option value="no">No</option>
              </select>
            </th>

            {/* Time (sem filtro) */}
            <th className="px-2 py-1 border border-gray-400"></th>

            {/* Grade (sem filtro) */}
            <th className="px-2 py-1 border border-gray-400"></th>

            {/* Actions */}
            <th className="px-2 py-1 border border-gray-400"></th>
          </tr>
        </thead>

        <tbody>
          {filteredTasks.map((task) => {
            const key = `${task.code}-${task.task_id}`;
            return (
              <tr key={key} className="hover:bg-gray-100 even:bg-gray-50">
                <td className="px-4 py-2 border border-gray-400">{task.code}</td>
                <td className="px-4 py-2 border border-gray-400">{task.group}</td>
                <td className="px-4 py-2 border border-gray-400">{task.task_id}</td>
                <td className="px-4 py-2 border border-gray-400">
                  {task.llm ? <span className="font-bold text-red-600">Yes</span> : "No"}
                </td>
                <td className="px-4 py-2 border border-gray-400">{task.time}</td>
                <td className="px-4 py-2 border border-gray-400">{task.grad_mean}</td>
                <td className="px-4 py-2 border border-gray-400">
                  <button
                    className="px-2 py-1 bg-gray-700 text-white rounded hover:bg-gray-900 transition-colors"
                    onClick={() => toggleExpand(key)}
                  >
                    {expanded[key] ? "Hide" : "Show"}
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {/* Detalhes da task */}
      {filteredTasks.map((task) => {
        const key = `${task.code}-${task.task_id}`;
        return (
          expanded[key] && (
            <div
              key={key}
              className="p-4 mt-2 border border-gray-400 rounded bg-gray-50 text-gray-900"
            >
              <p><strong>Description:</strong> {task.description}</p>
              <p><strong>Main Flow:</strong> {task.main_flow}</p>
              <p><strong>Alt Flow:</strong> {task.alt_flow}</p>
              <p>
                <strong>Grades:</strong> PhD1 {task.grad_phd_01}, PhD2 {task.grad_phd_02}, Mean {task.grad_mean}, LLM {task.grade_llm}
              </p>
              <p><strong>Notes:</strong> {task.note_llm || "N/A"}</p>
            </div>
          )
        );
      })}
    </div>
  );
}
