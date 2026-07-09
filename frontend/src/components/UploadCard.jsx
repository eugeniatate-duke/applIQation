import { useState } from "react";
import { analyzeResume } from "../services/api";
import Button from "./Button";

function UploadCard() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");

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

            try {
              const result = await analyzeResume(resume, jobDescription);

              console.log(result);
            } catch (error) {
              console.error(error);
              alert("Backend connection failed.");
            }
          }}
        />
      </div>
    </div>
  );
}

export default UploadCard;
