import Button from "./Button";

function Header() {
  return (
    <header
      style={{
        textAlign: "center",
        marginBottom: "35px",
      }}
    >
      <h1
        style={{
          fontSize: "4rem",
          fontWeight: "700",
          marginBottom: "20px",
        }}
      >
        ApplIQation
      </h1>

      <h2
        style={{
          fontWeight: "400",
          color: "#2563eb",
          marginBottom: "25px",
        }}
      >
        Know Before You Apply.
      </h2>

      <p
        style={{
          maxWidth: "750px",
          margin: "0 auto",
          fontSize: "1.2rem",
          lineHeight: "1.8",
          color: "#4b5563",
        }}
      >
        Compare your resume against any job description using machine learning,
        NLP, and transformer models before submitting your application.
      </p>
      <div
        style={{
          marginTop: "45px",
        }}
      >
        {/* <Button text="Analyze My Resume" onClick={() => {}} /> */}
      </div>

    </header>
  );
}

export default Header;
