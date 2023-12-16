
function submitForm() {
    var price = document.getElementById("price").value;
    var num_of_months = document.getElementById("num_of_months").value;
    var interest_rate = document.getElementById("interest_rate").value;
    var housing_inflation = document.getElementById("housing_inflation").value;
    var rent_month = document.getElementById("rent_month").value;
    var initial_expenses = document.getElementById("initial_expenses").value;
    var rent_increase = document.getElementById("rent_increase").value;

    // Make an AJAX request to the server
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'price=' + encodeURIComponent(price) + '&num_of_months=' + encodeURIComponent(num_of_months)
            + '&interest_rate=' + encodeURIComponent(interest_rate)
            + '&housing_inflation=' + encodeURIComponent(housing_inflation)
            + '&rent_month=' + encodeURIComponent(rent_month)
            + '&initial_expenses=' + encodeURIComponent(initial_expenses)
            + '&rent_increase=' + encodeURIComponent(rent_increase),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            displayTable(data.table);
            displayText(data.rent_txt, data.sell_txt);
        }
    });
}

// Function to display the table
function displayTable(tableData) {
    var resultDiv = document.getElementById("result");
    resultDiv.innerHTML = ''; // Clear previous content

    // Create a table element
    var tableHTML = '<table>'

    // Add headers to the table
    var headers = tableData[0];
    tableHTML += '<tr>';
    for (var i = 0; i < headers.length; i++) {
        tableHTML += '<th>' + headers[i] + '</th>';
    }
    tableHTML += '</tr>';

    // Add data rows to the table with alternating colors
    for (var i = 1; i < tableData.length; i++) {
        var rowColor = i % 2 === 0 ? 'even-row' : 'odd-row';
        tableHTML += '<tr class="' + rowColor + '">';
        for (var j = 0; j < tableData[i].length; j++) {
            var value = tableData[i][j];
            var formattedValue = value % 1 !== 0 ? parseFloat(value).toFixed(3) : value;
            tableHTML += '<td>' + formattedValue + '</td>';
        }
        tableHTML += '</tr>';
    }

    // Close the table
    tableHTML += '</table>';

    // Set the table HTML as the content of the resultDiv
    resultDiv.innerHTML = tableHTML;
}

function displayText(text1, text2) {
    var textDiv1 = document.createElement("div");
    textDiv1.id = 'text1';
    var textElm1 = document.createElement('p');
    textElm1.textContent = text1;
    textDiv1.appendChild(textElm1);
    textDiv1.style.position = 'absolute';
    textDiv1.style.top = '100px'; // Adjust the top position as needed
    textDiv1.style.right = '300px'; // Adjust the left position as needed
    document.body.appendChild(textDiv1);
    var textDiv2 = document.createElement("div");
    textDiv2.id = 'text2';
    var textElm2 = document.createElement('p');
    textElm2.textContent = text2;
    textDiv2.appendChild(textElm2);
    textDiv2.style.position = 'absolute';
    textDiv2.style.top = '200px'; // Adjust the top position as needed
    textDiv2.style.right = '300px'; // Adjust the left position as needed
    document.body.appendChild(textDiv2);
}