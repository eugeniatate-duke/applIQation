function RecommendationCard({ resource }) {
  return (
    <div
      style={{
        backgroundColor: "white",
        border: "1px solid #e5e7eb",
        borderRadius: "14px",
        padding: "18px",
        boxShadow: "0 6px 18px rgba(0,0,0,0.04)",
      }}
    >
      <h4
        style={{
          marginBottom: "8px",
          color: "#111827",
        }}
      >
        {resource.title}
      </h4>

      <p
        style={{
          margin: "0 0 10px 0",
          color: "#6b7280",
          fontSize: "0.9rem",
        }}
      >
        {resource.provider} • {resource.format} • {resource.difficulty} •{" "}
        {resource.duration_hours} hrs
      </p>

      <p
        style={{
          marginBottom: "12px",
          color: "#374151",
          lineHeight: "1.5",
        }}
      >
        {resource.reason}
      </p>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "8px",
          marginBottom: "14px",
        }}
      >
        {resource.skills.slice(0, 4).map((skill) => (
          <span
            key={skill}
            style={{
              backgroundColor: "#eff6ff",
              color: "#2563eb",
              borderRadius: "999px",
              padding: "5px 10px",
              fontSize: "0.8rem",
              fontWeight: "600",
            }}
          >
            {skill}
          </span>
        ))}
      </div>

      <a
        href={resource.url}
        target="_blank"
        rel="noreferrer"
        style={{
          color: "#2563eb",
          fontWeight: "600",
          textDecoration: "none",
        }}
      >
        Open Resource →
      </a>
    </div>
  );
}

export default RecommendationCard;
