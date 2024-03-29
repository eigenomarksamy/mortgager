
function submitForm() {
    var price = document.getElementById("price").value;
    var num_of_months = document.getElementById("num_of_months").value;
    var interest_rate = document.getElementById("interest_rate").value;
    var housing_inflation = document.getElementById("housing_inflation").value;
    var rent_month = document.getElementById("rent_month").value;
    var overbidding = document.getElementById("overbidding").value;
    var property_fixup = document.getElementById("property_fixup").value;
    var realtor_fee = document.getElementById("realtor_fee").value;
    var rent_increase = document.getElementById("rent_increase").value;
    var is_first_estate = document.getElementById("is_first_estate").checked;
    var older_than_35 = document.getElementById("older_than_35").checked;
    var rent_return_month = document.getElementById("rent_return_month").value;
    var rental_term = document.getElementById("rental_term").value;

    // Make an AJAX request to the server
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'price=' + encodeURIComponent(price)
            + '&num_of_months=' + encodeURIComponent(num_of_months)
            + '&interest_rate=' + encodeURIComponent(interest_rate)
            + '&housing_inflation=' + encodeURIComponent(housing_inflation)
            + '&rent_month=' + encodeURIComponent(rent_month)
            + '&overbidding=' + encodeURIComponent(overbidding)
            + '&property_fixup=' + encodeURIComponent(property_fixup)
            + '&realtor_fee=' + encodeURIComponent(realtor_fee)
            + '&rent_increase=' + encodeURIComponent(rent_increase)
            + '&is_first_estate=' + encodeURIComponent(is_first_estate)
            + '&older_than_35=' + encodeURIComponent(older_than_35)
            + '&rent_return_month=' + encodeURIComponent(rent_return_month)
            + '&rental_term=' + encodeURIComponent(rental_term),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            if ('table' in data) {
                displayTable(data.table);
            } else {
                clearTable();
            }
            displayBreakevenData(data.rent_be_value, data.sell_be_value, data.rent_out_be_value);
        }
    });
}

function clearTable() {
    var resultDiv = document.getElementById("result");
    resultDiv.innerHTML = 'NA'; // Clear the table content
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

function displayBreakevenData(beValue1, beValue2, beValue3) {
    document.getElementById('textAValue').textContent = 'NA';
    document.getElementById('textBValue').textContent = 'NA';
    document.getElementById('textCValue').textContent = 'NA';
    if (beValue1 >= 0) {
        document.getElementById('textAValue').textContent = beValue1;
    }
    if (beValue2 >= 0) {
        document.getElementById('textBValue').textContent = beValue2;
    }
    if (beValue3 >= 0) {
        document.getElementById('textCValue').textContent = beValue3;
    }
}