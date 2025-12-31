'use client';

import { useEffect, useState } from 'react';

export default function Home() {
  const [tables, setTables] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`)
      .then(res => res.json())
      .then(data => setTables(data.tables));
  }, []);

  return (
    <div>
      <h1>Tabelas do Banco:</h1>
      <ul>
        {tables.map(nome => (
          <li key={nome}>{nome}</li>
        ))}
      </ul>
    </div>
  );
}