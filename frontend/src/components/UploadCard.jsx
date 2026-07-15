import { useState } from "react";
import { analyzeResume } from "../services/api";
import Button from "./Button";

function UploadCard() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [results, setResults] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  return (
    <div
      style={{
        backgroundColor: "white",
        borderRadius: "20px",
        padding: "40px",
        maxWidth: "900px",
        margin: "40px auto",
        boxShadow: "0 12px 35px rgba(0,0,0,0.08)",
      }}
    >
      <h2
        style={{
          marginBottom: "30px",
          textAlign: "center",
        }}
      >
        Upload Your Resume
      </h2>
      {/* Resume Upload */}
      <div
        onClick={() => document.getElementById("resume-upload").click()}
        style={{
          border: "2px dashed #cbd5e1",
          borderRadius: "16px",
          padding: "25px",
          textAlign: "center",
          marginBottom: "35px",
          cursor: "pointer",
          transition: "0.2s",
        }}
      >
        <input
          id="resume-upload"
          type="file"
          accept=".pdf,.doc,.docx,.txt"
          style={{ display: "none" }}
          onChange={(e) => setResume(e.target.files[0])}
        />

        <div
          style={{
            fontSize: "3rem",
            marginBottom: "15px",
          }}
        >
          📄
        </div>

        <p
          style={{
            fontSize: "1.1rem",
            marginBottom: "10px",
          }}
        >
          {resume ? resume.name : "Drag & Drop or Click to Upload"}
        </p>

        <p
          style={{
            color: "#6b7280",
          }}
        >
          Supports PDF • DOCX • TXT
        </p>
      </div>

      {/* Job Description */}
      <textarea
        placeholder="Paste the job description here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        rows="5"
        style={{
          width: "100%",
          borderRadius: "12px",
          border: "1px solid #d1d5db",
          padding: "18px",
          fontSize: "1rem",
          resize: "vertical",
          marginBottom: "30px",
        }}
      />
      {/* Analyze Button */}
      <div
        style={{
          display: "flex",

          flexDirection: "column",

          alignItems: "center",

          marginTop: "10px",
        }}
      >
        <Button
          text="Analyze Resume"
          onClick={async () => {
            if (!resume || !jobDescription) {
              alert("Please upload a resume and paste a job description.");
              return;
            }

            setLoading(true);
            setError("");

            try {
              const result = await analyzeResume(resume, jobDescription);

              setResults(result);
              setTimeout(() => {
                document
                  .getElementById("results-section")
                  ?.scrollIntoView({ behavior: "smooth" });
              }, 100);
            } catch (err) {
              setError("Unable to analyze resume.");
            } finally {
              setLoading(false);
            }
          }}
        />
        {loading && (
          <p
            style={{
              marginTop: "20px",
              color: "#2563eb",
            }}
          >
            Analyzing resume...
          </p>
        )}

        {error && (
          <p
            style={{
              marginTop: "20px",
              color: "red",
            }}
          >
            {error}
          </p>
        )}

        {results && (
          <div
            id="results-section"
            style={{
              marginTop: "40px",
              padding: "25px",
              border: "1px solid #e5e7eb",
              borderRadius: "16px",
              backgroundColor: "#f9fafb",
            }}
          >
            <h2>Career Readiness Assessment</h2>

            <h3>{results.label}</h3>

            <p>
              AI Confidence: <strong>{results.confidence}%</strong>
            </p>

            <p
              style={{
                color: "#6b7280",

                marginTop: "10px",

                fontSize: "0.95rem",
              }}
            >
              Prediction based on the fine-tuned DistilBERT model.
            </p>

            <hr style={{ margin: "20px 0" }} />

            <h3>
              ✓ Skill Match ({results.matched_count}/{results.required_count})
            </h3>

            <ul>
              {results.matched_skills.length === 0 ? (
                <li>No direct matches found.</li>
              ) : (
                results.matched_skills.map((skill) => (
                  <li key={skill}>{skill}</li>
                ))
              )}
            </ul>

            <hr style={{ margin: "20px 0" }} />

            <h3>⚠ Missing Skills ({results.missing_skills.length})</h3>

            <ul>
              {results.missing_skills.length === 0 ? (
                <li>
                  No required technical skills were missing based on keyword
                  matching.
                </li>
              ) : (
                results.missing_skills.map((skill) => (
                  <li key={skill}>{skill}</li>
                ))
              )}
            </ul>

            <hr style={{ margin: "20px 0" }} />

            {/* <h3>📚 Learning Roadmap</h3>

            <ul>
              {results.roadmap.map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ul> */}
            <h3>📚 Learning Roadmap</h3>

            <ul>
              {results.roadmap.map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ul>

            {results.recommended_resources &&
              results.recommended_resources.length > 0 && (
                <>
                  <hr style={{ margin: "25px 0" }} />

                  <h3>🎯 Personalized Learning Recommendations</h3>

                  <p
                    style={{
                      color: "#6b7280",
                      fontSize: "0.95rem",
                      lineHeight: "1.6",
                      marginBottom: "20px",
                    }}
                  >
                    These resources are recommended based on your missing skills
                    and target job description, with diversity across learning
                    formats.
                  </p>

                  <div
                    style={{
                      display: "grid",
                      gap: "16px",
                    }}
                  >
                    {results.recommended_resources.map((resource) => (
                      <div
                        key={resource.id}
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
                          {resource.provider} • {resource.format} •{" "}
                          {resource.difficulty} • {resource.duration_hours} hrs
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
                    ))}
                  </div>
                </>
              )}
          </div>
        )}
      </div>
    </div>
  );
}

export default UploadCard;
