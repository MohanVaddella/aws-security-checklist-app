document.addEventListener("DOMContentLoaded", function () {

    
    const searchInput = document.getElementById("searchInput");
    const tableRows = document.querySelectorAll("#checklistTable tbody tr");
    const noResultsMessage = document.createElement("tr");
    noResultsMessage.innerHTML = "<td colspan='100%' style='text-align: center;'>No results found</td>";
    noResultsMessage.style.display = "none";
    document.querySelector("#checklistTable tbody").appendChild(noResultsMessage);

    
    function debounce(func, delay) {
        let debounceTimer;
        return function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => func.apply(this, arguments), delay);
        };
    }

    function filterTable() {
        const searchTerm = searchInput.value.toLowerCase();
        let visibleCount = 0;

        tableRows.forEach(function (row) {
            const rowText = row.textContent.toLowerCase();
            if (rowText.includes(searchTerm)) {
                row.style.display = ""; 
                visibleCount++;
            } else {
                row.style.display = "none"; 
            }
        });

        
        if (visibleCount === 0) {
            noResultsMessage.style.display = ""; 
        } else {
            noResultsMessage.style.display = "none"; 
        }
    }

    
    searchInput.addEventListener("keyup", debounce(filterTable, 300));

    
    const tableBody = document.querySelector("#checklistTable tbody");

    tableBody.addEventListener("click", function (e) {
        if (e.target && e.target.nodeName === "TD") {
            const row = e.target.closest("tr");

            
            tableRows.forEach(function (r) {
                r.classList.remove("highlight");
            });

        
            row.classList.add("highlight");
        }
    });

    
    const showMoreButton = document.getElementById("showMoreBtn");
    let rowsToShow = 10; 

    function showRows() {
        let visibleCount = 0;
        tableRows.forEach(function (row, index) {
            if (index < rowsToShow) {
                row.style.display = ""; 
                visibleCount++;
            } else {
                row.style.display = "none"; 
            }
        });
        
        if (visibleCount >= tableRows.length) {
            showMoreButton.disabled = true;
            showMoreButton.textContent = "All rows are visible";
        } else {
            showMoreButton.disabled = false;
            showMoreButton.textContent = "Show More";
        }
    }

    
    showRows();

    
    showMoreButton.addEventListener("click", function () {
        rowsToShow += 10;
        showRows();
    });

});
