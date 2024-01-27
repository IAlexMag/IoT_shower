const checkbox = document.querySelectorAll('input[type="checkbox');

checkbox.forEach((checkbox => {
    checkbox.addEventListener('change', () => {
        if(checkbox.checked) {
            const valor_seleccionado = checkbox.value;
            console.log("Chackbox seleccionado", valor_seleccionado)
        }
    });
}));