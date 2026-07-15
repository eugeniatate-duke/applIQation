import { useState } from "react";
import { analyzeResume } from "../services/api";
import Button from "./Button";
import RecommendationCard from "./RecommendationCard";

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

                  ?.scrollIntoView({
                    behavior: "smooth",

                    block: "start",
                  });
              }, 200);
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
            <div
              style={{
                textAlign: "center",
                marginBottom: "35px",
              }}
            >
              <h2
                style={{
                  marginBottom: "22px",
                }}
              >
                Career Readiness Assessment
              </h2>

              <h1
                style={{
                  margin: "0",
                  fontSize: "2rem",
                  color:
                    results.label === "Ready"
                      ? "#15803d"
                      : results.label === "Ready with Short Ramp-Up"
                        ? "#ca8a04"
                        : "#b91c1c",
                }}
              >
                {results.label}
              </h1>

              <p
                style={{
                  marginTop: "18px",
                  color: "#6b7280",
                  fontSize: "0.95rem",
                }}
              >
                Confidence: {results.confidence}%
              </p>

              <p
                style={{
                  color: "#9ca3af",
                  fontSize: "0.85rem",
                  marginTop: "8px",
                }}
              >
                Prediction generated by the fine-tuned DistilBERT model.
              </p>
            </div>

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
                      <RecommendationCard
                        key={resource.id}
                        resource={resource}
                      />
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
