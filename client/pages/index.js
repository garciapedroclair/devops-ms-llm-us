import BoxPlot from "../components/BoxPlot";

export default function Home() {
  return (
    <div style={{ padding: "20px", background: "#fff", minHeight: "100vh" }}>
      <h1 style={{ textAlign: "center", marginBottom: "40px" }}>
        LLM for User Stories - Dashboard
      </h1>
      <BoxPlot />
    </div>
  );
}
