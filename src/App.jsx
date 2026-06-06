import { useState } from "react";
import "./App.css";

function App() {

  const [age, setAge] = useState("");
  const [sex, setSex] = useState("");
  const [bp, setBP] = useState("");
  const [cholesterol, setCholesterol] = useState("");
  const [maxhr, setMaxhr] = useState("");

  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {

    setLoading(true);
    setResult("");

    try {

      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          Age: Number(age),
          Sex: Number(sex),
          ChestPainType: 1,
          RestingBP: Number(bp),
          Cholesterol: Number(cholesterol),
          FastingBS: 0,
          RestingECG: 1,
          MaxHR: Number(maxhr),
          ExerciseAngina: 0,
          Oldpeak: 1,
          ST_Slope: 1
        })
      });

      const data = await response.json();

      if (data.result === 1) {
        setResult("High Risk ⚠️");
      } else {
        setResult("Low Risk ✅");
      }

    } catch (error) {

      console.error("Error:", error);
      setResult("Server Error ❌");

    }

    setLoading(false);
  };

  return (

    <div className="main-container">

      <div className="title-box">
        <h1>Heart Failure Prediction System</h1>
      </div>

      <div className="card">

        <input
          type="number"
          placeholder="Age"
          value={age}
          onChange={(e) => setAge(e.target.value)}
        />

        <input
          type="number"
          placeholder="Sex (1=Male, 0=Female)"
          value={sex}
          onChange={(e) => setSex(e.target.value)}
        />

        <input
          type="number"
          placeholder="Resting Blood Pressure"
          value={bp}
          onChange={(e) => setBP(e.target.value)}
        />

        <input
          type="number"
          placeholder="Cholesterol"
          value={cholesterol}
          onChange={(e) => setCholesterol(e.target.value)}
        />

        <input
          type="number"
          placeholder="Max Heart Rate"
          value={maxhr}
          onChange={(e) => setMaxhr(e.target.value)}
        />

        <button onClick={handlePredict}>
          {loading ? "Predicting..." : "Predict"}
        </button>

        {result && (
          <h2 className="result">
            {result}
          </h2>
        )}

      </div>

    </div>
  );
}

export default App;