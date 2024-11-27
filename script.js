// Function to handle product submission
async function addProduct() {
    // Get values from the form fields
    const productUrl = document.getElementById("product_url").value;
    const email = document.getElementById("email").value;

    // Validate form input
    if (!productUrl || !email) {
        displayAlert("Please fill out all fields.", "error");
        return;
    }

    // Send the data to the backend API
    try {
        const response = await fetch('http://localhost:5000/add_product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_url: productUrl,
                email: email
            })
        });


        const result = await response.json(); // Parse the response

        // Handle the response from the server
        if (response.ok) {
            displayAlert("Product added successfully!", "success");
            document.getElementById("product_url").value = "";
            document.getElementById("email").value = "";
        } else {
            // Display specific error message from the server
            displayAlert(result.error || "An error occurred. Please try again.", "error");
        }
    } catch (error) {
        displayAlert("An unexpected error occurred. Please try again.", "error");
    }
}

// Function to display alerts
function displayAlert(message, type) {
    const alertBox = document.getElementById("alertBox");
    alertBox.innerText = message;
    alertBox.className = type === "success" ? "alert success" : "alert error";
}
