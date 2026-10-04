
// Where calculations run. By default the form posts to Flask's /calculate
// (app.py). The static build (build_static.py) sets window.MORTGAGER so the
// same Python in src/ runs in the browser with Pyodide, without a server.
var CONFIG = window.MORTGAGER || { backend: 'server' };

function submitForm() {
    // Every value is sent as a string, the way an HTML form would send it.
    var form = {
        price: document.getElementById("price").value,
        num_of_months: document.getElementById("num_of_months").value,
        interest_rate: document.getElementById("interest_rate").value,
        housing_inflation: document.getElementById("housing_inflation").value,
        rent_month: document.getElementById("rent_month").value,
        overbidding: document.getElementById("overbidding").value,
        property_fixup: document.getElementById("property_fixup").value,
        realtor_fee: document.getElementById("realtor_fee").value,
        rent_increase: document.getElementById("rent_increase").value,
        is_first_estate: String(document.getElementById("is_first_estate").checked),
        older_than_35: String(document.getElementById("older_than_35").checked),
        rent_return_month: document.getElementById("rent_return_month").value,
        rental_term: document.getElementById("rental_term").value,
    };

    requestCalculation(form)
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
    })
    .catch(error => {
        console.error(error);
        alert('Calculation failed: ' + error.message);
    });
}

function requestCalculation(form) {
    if (CONFIG.backend === 'browser') {
        return calculateInBrowser(form);
    }
    return fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(form),
    })
    .then(response => response.json());
}

var pythonApi = null;
var pythonReady = false;

// Loads Pyodide and the project's Python sources once; later calls reuse them.
function loadPython() {
    if (!pythonApi) {
        pythonApi = (async () => {
            const pyodide = await loadPyodide();
            pyodide.FS.mkdirTree('/home/pyodide/src');
            for (const name of CONFIG.pythonFiles) {
                const response = await fetch('src/' + name);
                if (!response.ok) {
                    throw new Error('Could not load src/' + name);
                }
                pyodide.FS.writeFile('/home/pyodide/src/' + name, await response.text());
            }
            const api = pyodide.pyimport('src.api');
            pythonReady = true;
            return api;
        })().catch(error => {
            pythonApi = null; // allow a retry on the next click
            throw error;
        });
    }
    return pythonApi;
}

async function calculateInBrowser(form) {
    if (!pythonReady) {
        document.getElementById("result").textContent = 'Loading Python (first run only)...';
    }
    const api = await loadPython();
    return JSON.parse(api.calculate_json(JSON.stringify(form)));
}

if (CONFIG.backend === 'browser') {
    // Start downloading Python while the form is being filled in. A failure here
    // is retried, and reported, when Calculate is clicked.
    loadPython().catch(console.error);
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