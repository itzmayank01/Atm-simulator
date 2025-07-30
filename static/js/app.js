document.addEventListener('DOMContentLoaded', () => {
    const historyTable = document.getElementById('history-table');
    if (historyTable) {
        fetch('/history')
            .then(resp => resp.json())
            .then(data => {
                const tbody = historyTable.querySelector('tbody');
                if (!Array.isArray(data) || data.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">No transactions yet.</td></tr>';
                    return;
                }
                tbody.innerHTML = '';
                data.forEach(txn => {
                    const tr = document.createElement('tr');

                    const dateTd = document.createElement('td');
                    dateTd.textContent = new Date(txn.timestamp).toLocaleString();
                    tr.appendChild(dateTd);

                    const typeTd = document.createElement('td');
                    typeTd.textContent = txn.type.charAt(0).toUpperCase() + txn.type.slice(1);
                    tr.appendChild(typeTd);

                    const amountTd = document.createElement('td');
                    amountTd.textContent = txn.amount.toFixed(2);
                    amountTd.classList.add('text-end');
                    tr.appendChild(amountTd);

                    tbody.appendChild(tr);
                });
            })
            .catch(err => console.error(err));
    }
});