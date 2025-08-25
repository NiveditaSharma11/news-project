<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>News Summarizer</title>
  <style>
    body {
      background-color: #121212;
      color: #e0e0e0;
      font-family: Arial, sans-serif;
      text-align: center;
      padding: 20px;
    }

    h1 {
      font-size: 2.5em;
      color: #39ff14; /* Neon Green */
      text-shadow: 0 0 10px #39ff14, 0 0 20px #39ff14, 0 0 30px #39ff14;
      margin-bottom: 20px;
    }

    textarea {
      width: 80%;
      height: 120px;
      background-color: #1e1e1e;
      color: #fff;
      border: 1px solid #333;
      border-radius: 8px;
      padding: 10px;
      font-size: 1em;
      resize: none;
      margin-bottom: 15px;
    }

    select, button {
      background-color: #1e1e1e;
      color: #fff;
      border: 1px solid #39ff14;
      border-radius: 8px;
      padding: 10px 15px;
      margin: 5px;
      cursor: pointer;
      font-size: 1em;
      transition: 0.3s;
    }

    button:hover, select:hover {
      background-color: #39ff14;
      color: #121212;
    }

    #outputBox {
      margin-top: 20px;
      padding: 15px;
      border: 2px solid #39ff14;
      border-radius: 8px;
      background-color: #1e1e1e;
      width: 80%;
      margin-left: auto;
      margin-right: auto;
      color: #fff;
      min-height: 60px;
    }
  </style>
</head>
<body>

  <h1>📰 News Summarizer</h1>

  <textarea id="newsInput" placeholder="Paste your news text here..."></textarea><br/>

  <label for="toneSelect">Choose Summary Tone:</label>
  <select id="toneSelect">
    <option value="neutral">Neutral</option>
    <option value="formal">Formal</option>
    <option value="casual">Casual</option>
  </select><br/>

  <button onclick="getSummary()">Get Summary</button>
  <button onclick="getBias()">Check Bias</button>

  <div id="outputBox">📝 Output will appear here.</div>

  <script>
    async function getSummary() {
      const text = document.getElementById("newsInput").value;
      const tone = document.getElementById("toneSelect").value;

      if (!text.trim()) {
        document.getElementById("outputBox").innerText = "⚠️ Please enter news content.";
        return;
      }

      try {
        const response = await fetch("https://news-project-i5qv.onrender.com/summary", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ text: text, tone: tone })
        });

        if (!response.ok) {
          throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        if (data.summary) {
          document.getElementById("outputBox").innerText = "📄 Summary: " + data.summary;
        } else {
          document.getElementById("outputBox").innerText = "⚠️ Unexpected response from server.";
        }
      } catch (err) {
        console.error("Summary error:", err);
        document.getElementById("outputBox").innerText = "❌ Error: Could not fetch summary.";
      }
    }

    async function getBias() {
      const text = document.getElementById("newsInput").value;

      if (!text.trim()) {
        document.getElementById("outputBox").innerText = "⚠️ Please enter news content.";
        return;
      }

      try {
        const response = await fetch("https://news-project-i5qv.onrender.com/bias", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
          throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        if (data.bias && data.confidence) {
          document.getElementById("outputBox").innerText =
            `🧠 Bias: ${data.bias} (Confidence: ${data.confidence})`;
        } else {
          document.getElementById("outputBox").innerText = "⚠️ Unexpected response from server.";
        }
      } catch (err) {
        console.error("Bias error:", err);
        document.getElementById("outputBox").innerText = "❌ Error: Could not fetch bias.";
      }
    }
  </script>

</body>
</html>
