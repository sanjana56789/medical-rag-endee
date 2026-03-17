// async function upload() {
//     let file = document.getElementById("file").files[0];

//     if (!file) {
//         alert("Select file");
//         return;
//     }

//     let formData = new FormData();
//     formData.append("file", file);

//     await fetch("/upload", {
//         method: "POST",
//         body: formData
//     });

//     alert("Uploaded!");
// }

// async function ask() {
//     let q = document.getElementById("question").value;

//     if (!q) {
//         alert("Enter question");
//         return;
//     }

//     document.getElementById("loading").style.display = "block";

//     try {
//         let res = await fetch("/query", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({ question: q })
//         });

//         let data = await res.json();

//         document.getElementById("loading").style.display = "none";

//         document.getElementById("result").innerHTML =
//             "<b>Answer:</b><br>" + data.answer;

//     } catch (e) {
//         document.getElementById("loading").style.display = "none";
//         document.getElementById("result").innerHTML = "Error: " + e;
//     }
// }


async function upload() {
    const file = document.getElementById("file").files[0];
    const status = document.getElementById("uploadStatus");

    if (!file) {
        alert("Please select a file first.");
        return;
    }

    status.innerHTML = "⏳ Uploading...";
    status.style.color = "#667eea";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        if (data.error) {
            status.innerHTML = "❌ " + data.error;
            status.style.color = "red";
        } else {
            status.innerHTML = "✅ " + data.message;
            status.style.color = "green";
        }

    } catch (e) {
        status.innerHTML = "❌ Upload failed: " + e;
        status.style.color = "red";
    }
}

async function ask() {
    const q = document.getElementById("question").value.trim();
    const resultDiv = document.getElementById("result");
    const loading = document.getElementById("loading");

    if (!q) {
        alert("Please enter a question.");
        return;
    }

    loading.style.display = "block";
    resultDiv.innerHTML = "";

    try {
        const res = await fetch("/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: q })
        });

        const data = await res.json();
        loading.style.display = "none";

        const answer = data.answer || "No answer returned.";

        const formatted = answer
            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
            .replace(/\n/g, "<br>");

        let sourcesHTML = "";
        if (data.sources && data.sources.length > 0) {
            const items = data.sources.map((s, i) =>
                `<div class="source-chunk"><b>Excerpt ${i + 1}:</b><br>${s}</div>`
            ).join("");
            sourcesHTML = `
                <details class="sources">
                    <summary>📄 View source excerpts from your report</summary>
                    ${items}
                </details>`;
        }

        resultDiv.innerHTML = `
            <div class="answer-box">
                <div class="answer-text">${formatted}</div>
                ${sourcesHTML}
            </div>`;

    } catch (e) {
        loading.style.display = "none";
        resultDiv.innerHTML = `<div style="color:red;margin-top:16px">❌ Error: ${e}</div>`;
    }
}