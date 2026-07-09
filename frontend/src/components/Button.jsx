function Button({ text, onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        backgroundColor: "#2563eb",
        color: "white",
        border: "none",
        borderRadius: "12px",
        padding: "18px 44px",
        fontSize: "1rem",
        fontWeight: "600",
        cursor: "pointer",
        transition: "all 0.2s ease",
        boxShadow: "0 10px 25px rgba(37,99,235,0.20)",
      }}
      onMouseEnter={(e) => {
        e.target.style.backgroundColor = "#1d4ed8";
        e.target.style.transform = "translateY(-2px)";
      }}
      onMouseLeave={(e) => {
        e.target.style.backgroundColor = "#2563eb";
        e.target.style.transform = "translateY(0)";
      }}
    >
      {text}
    </button>
  );
}

export default Button;
