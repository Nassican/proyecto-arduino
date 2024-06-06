const keyboardDiv = document.getElementById('keyboard');
const dataTable = document.getElementById('data').querySelector('tbody');

const keys = [
    '1', '2', '3', 'A',
    '4', '5', '6', 'B',
    '7', '8', '9', 'C',
    '*', '0', '#', 'D'
];

keys.forEach(key => {
    const button = document.createElement('button');
    button.textContent = key;
    button.className = 'key';
    button.id = `key-${key}`;
    keyboardDiv.appendChild(button);
});

function updateData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            dataTable.innerHTML = '';
            data.forEach(note => {
                const row = dataTable.insertRow();
                row.innerHTML = `
                    <td>${note.tecla}</td>
                    <td>${note.decibelios.toFixed(1)} dB</td>
                    <td>${note.nota_detectada}</td>
                    <td>${note.nota_tecla}</td>
                    <td>${new Date(note.timestamp).toLocaleString()}</td>
                `;
                
                // Resaltar la tecla correspondiente
                const key = document.getElementById(`key-${note.tecla}`);
                key.classList.add('active');
                setTimeout(() => key.classList.remove('active'), 300);
            });
        });
}

setInterval(updateData, 500);  // Actualizar cada 500ms