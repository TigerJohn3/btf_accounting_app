/**
 * Sorts an HTML table
 * From dcode YouTube channel tutorial (Sort HTML Tables - Web Dev)
 * For now, can only support single HTML tbody element 
 *      Can modify this if you want to (tBodies[0] line)
 * 
 * @param {HTMLTableElement} table The table to sort
 * @param {number} column The index of the column to sort 
 * @param {boolean} asc Determines if the table will be in ascending order 
 */

function sortTableByColumn(table, column, asc = true) {
    const dirModifier = asc ? 1 : -1;
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.querySelectorAll("tr"));


    // Sort each row
    const sortedRows = rows.sort((a, b) => {
        const aColText = a.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();
        const bColText = b.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();
    
        return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier)
    });

    // Remove all existing TRs from the table
    while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
    }

    // Readd the newly sorted rows
    // The below code passes in each row back into the tbody element
    tbody.append(...sortedRows);

    // Remember how column is currently sorted
    table.querySelectorAll("th").forEach(thead => thead.classList.remove("th-sort-asc", "th-sort-desc"));
    table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle("th-sort-asc", asc);
    table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle("th-sort-desc", !asc);
}

// Passes in every table header element within a table that is sortable
document.querySelectorAll(".table-sortable th").forEach(headerCell => {
    headerCell.addEventListener("click", () => {
        const tableElement = headerCell.parentElement.parentElement.parentElement;
        const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
        const currentIsAscending = headerCell.classList.contains("th-sort-asc");
    
        sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
    });
});