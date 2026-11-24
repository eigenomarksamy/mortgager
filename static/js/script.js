// Where calculations run. By default the form posts to Flask's /calculate
// (app.py). The static build (build_static.py) sets window.MORTGAGER so the
// same Python in src/ runs in the browser with Pyodide, without a server.
var CONFIG = window.MORTGAGER || { backend: 'server' };

// The fields src/api.py parses, by element id. Checkboxes are sent as
// "true" or "false", and every other value as a string, the way an HTML form
// would send it.
var FIELDS = [
    'price', 'num_of_months', 'interest_rate', 'housing_inflation',
    'rent_month', 'overbidding', 'property_fixup', 'realtor_fee',
    'rent_increase', 'is_first_estate', 'older_than_35',
    'rent_return_month', 'rental_term',
];

var AMOUNT = new Intl.NumberFormat('en-GB', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
});

function readForm() {
    var form = {};
    for (var i = 0; i < FIELDS.length; i++) {
        var element = document.getElementById(FIELDS[i]);
        form[FIELDS[i]] = element.type === 'checkbox' ? String(element.checked) : element.value;
    }
    return form;
}

function submitForm(event) {
    if (event) {
        event.preventDefault();
    }
    var button = document.getElementById('calculate');
    showError(null);
    setStatus(CONFIG.backend === 'browser' && !pythonReady
        ? 'Loading Python in your browser. The first calculation takes a few seconds.'
        : 'Calculating…', true);
    button.disabled = true;
    document.querySelector('.results').setAttribute('aria-busy', 'true');

    requestCalculation(readForm())
    .then(function (data) {
        if (data.error) {
            showError(data.error);
            setStatus('', false);
            return;
        }
        displayBreakevenData(data.rent_be_value, data.sell_be_value, data.rent_out_be_value);
        if ('table' in data) {
            displayTable(data.table);
            setStatus('Calculated ' + (data.table.length - 1) + ' months.', false);
        } else {
            clearTable();
            setStatus('', false);
        }
    })
    .catch(function (error) {
        console.error(error);
        showError('The calculation failed: ' + error.message);
        setStatus('', false);
    })
    .finally(function () {
        button.disabled = false;
        document.querySelector('.results').removeAttribute('aria-busy');
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
    .then(function (response) { return response.json(); });
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
    const api = await loadPython();
    return JSON.parse(api.calculate_json(JSON.stringify(form)));
}

function setStatus(text, loading) {
    var status = document.getElementById('status');
    status.textContent = text;
    status.classList.toggle('loading', loading);
}

function showError(message) {
    var error = document.getElementById('error');
    error.textContent = message || '';
    error.hidden = !message;
}

function clearTable() {
    var resultDiv = document.getElementById('result');
    var note = document.createElement('p');
    note.textContent = 'No schedule for these inputs: the price is above the limit for a first home.';
    resultDiv.replaceChildren(note);
}

// The first column is the month, and every other column is an amount in euros.
function displayTable(tableData) {
    var table = document.createElement('table');

    var head = table.createTHead().insertRow();
    var headers = tableData[0];
    for (var i = 0; i < headers.length; i++) {
        var th = document.createElement('th');
        th.scope = 'col';
        th.textContent = headers[i];
        head.appendChild(th);
    }

    var body = table.createTBody();
    for (var r = 1; r < tableData.length; r++) {
        var row = body.insertRow();
        for (var c = 0; c < tableData[r].length; c++) {
            var value = tableData[r][c];
            var cell;
            if (c === 0) {
                cell = document.createElement('th');
                cell.scope = 'row';
                cell.textContent = value;
                row.appendChild(cell);
            } else {
                cell = row.insertCell();
                cell.textContent = AMOUNT.format(value);
                if (value < 0) {
                    cell.className = 'negative';
                }
            }
        }
    }

    document.getElementById('result').replaceChildren(table);
}

// A breakeven month of -1 means it isn't reached within the term.
function displayBreakevenData(beValue1, beValue2, beValue3) {
    showBreakeven('textAValue', beValue1);
    showBreakeven('textBValue', beValue2);
    showBreakeven('textCValue', beValue3);
}

function showBreakeven(id, month) {
    var element = document.getElementById(id);
    if (!(month >= 0)) {
        element.textContent = 'none';
        var none = document.createElement('small');
        none.textContent = 'not within the term';
        element.appendChild(none);
        return;
    }
    element.textContent = 'month ' + month;
    var years = Math.floor(month / 12);
    var months = month % 12;
    var parts = [];
    if (years) {
        parts.push(years + (years === 1 ? ' year' : ' years'));
    }
    if (months) {
        parts.push(months + (months === 1 ? ' month' : ' months'));
    }
    var span = document.createElement('small');
    span.textContent = parts.join(', ');
    element.appendChild(span);
}

document.getElementById('mortgage-form').addEventListener('submit', submitForm);

if (CONFIG.backend === 'browser') {
    // Start downloading Python while the form is being filled in. A failure here
    // is retried, and reported, when Calculate is clicked.
    loadPython().catch(console.error);
}
