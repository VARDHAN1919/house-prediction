function predictPrice() {
    let area = document.getElementById("area").value;
    let bedrooms = document.getElementById("bedrooms").value;
    let bathrooms = document.getElementById("bathrooms").value;
    let parking = document.getElementById("parking").value;
    let location = document.getElementById("location").value;

    if (!area || !bedrooms || !bathrooms || !parking) {
        alert("Please fill all fields");
        return;
    }

    document.getElementById("result").innerHTML = "⏳ Predicting...";

    fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            area: area,
            bedrooms: bedrooms,
            bathrooms: bathrooms,
            parking: parking,
            location: location
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById("result").innerHTML = data.error;
            return;
        }

        document.getElementById("result").innerHTML =
            "💰 Predicted Price: ₹ " + data.price.toLocaleString();

        let row = document.getElementById("history").insertRow(1);
        row.insertCell(0).innerHTML = area;
        row.insertCell(1).innerHTML = "₹ " + data.price.toLocaleString();

        document.getElementById("explain").innerHTML =
            `<b>Explainable AI</b><br>
            Area: ${data.explanation.Area}<br>
            Bedrooms: ${data.explanation.Bedrooms}<br>
            Bathrooms: ${data.explanation.Bathrooms}<br>
            Parking: ${data.explanation.Parking}`;
    })
    .catch(err => {
        document.getElementById("result").innerHTML = "Error predicting price";
        console.error(err);
    });
}
