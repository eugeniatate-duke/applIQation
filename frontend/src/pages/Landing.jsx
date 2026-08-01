import Header from "../components/Header";
import UploadCard from "../components/UploadCard";

function Landing() {
  return (
    <main
      style={{
        width: "100%",
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "30px 20px",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "1200px",
        }}
      >
        <Header />
        <UploadCard />
        <p
          style={{
            textAlign: "center",

            marginTop: "35px",

            marginBottom: "60px",

            fontSize: "0.9rem",

            color: "#9ca3af",

            letterSpacing: "0.08em",
          }}
        >
          Powered by DistilBERT • FLAN-T5 • LoRA • FastAPI • React
        </p>
      </div>
    </main>
  );
}

export default Landing;
