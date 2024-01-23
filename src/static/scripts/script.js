
/*la accion del movimiento */
   const list = document.querySelectorAll('.list');
        function activeLink(){
            list.forEach((item)=>item.classList.remove('active'));
            this.classList.add('active');
        }
        list.forEach((item)=>item.addEventListener('click',activeLink));
        /**/
  document.getElementById('menu-icon').addEventListener('click', function () {
    var nav = document.querySelector('nav');
    var submenu = document.getElementById('submenu');
    nav.classList.toggle('active');
    submenu.classList.toggle('active');
    submenu.style.display = (submenu.style.display === 'block') ? 'none' : 'block';
  });
  


   /*PERFIL*/
   function cancelar() {
    alert("Formulario cancelado");
}

function guardar() {
    var usuario = document.getElementById("usuario").value;
    var nombre = document.getElementById("nombre").value;
    var apellidoPaterno = document.getElementById("apellidoPaterno").value;
    var apellidoMaterno = document.getElementById("apellidoMaterno").value;

    alert("Datos guardados:\nUsuario: " + usuario + "\nNombre: " + nombre + "\nApellido Paterno: " + apellidoPaterno + "\nApellido Materno: " + apellidoMaterno);
}
/*informacion */
function toggleDescription(product) {
    const textBox = product.querySelector('.text-box');
    textBox.style.display = (textBox.style.display === 'none' || textBox.style.display === '') ? 'block' : 'none';
}
function toggleDescription(texto) {
    const textBox = texto.querySelector('.text-box');
    textBox.style.display = (textBox.style.display === 'none' || textBox.style.display === '') ? 'block' : 'none';
}
/*botones de Baño
function toggleButton(buttonId) {
            var button = document.getElementById(buttonId);
            button.classList.toggle('selected');
            resetOtherButtons(buttonId);
        }

        function resetOtherButtons(selectedButtonId) {
            var buttons = document.querySelectorAll('button:not(#' + selectedButtonId + ')');
            buttons.forEach(function(button) {
                button.classList.remove('selected');
            });
        }

  document.addEventListener('DOMContentLoaded', function() {
    let slider = document.getElementById('slider');
    let thumb = slider.querySelector('.thumb');
    let percentageLabel = document.getElementById('percentage');

    thumb.onmousedown = function(event) {
        event.preventDefault();

        let shiftX = event.clientX - thumb.getBoundingClientRect().left;

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);

        function onMouseMove(event) {
            let newLeft = event.clientX - shiftX - slider.getBoundingClientRect().left;

            if (newLeft < 0) {
                newLeft = 0;
            }
            let rightEdge = slider.offsetWidth - thumb.offsetWidth;
            if (newLeft > rightEdge) {
                newLeft = rightEdge;
            }

            thumb.style.left = newLeft + 'px';

            // Calculate and display the percentage
            let percentage = (newLeft / rightEdge) * 100;
            percentageLabel.textContent = `${Math.round(percentage)}%`;

            // Set the color to white (255, 255, 255)
            thumb.style.backgroundColor = 'rgb(255, 255, 255)';
        }

        function onMouseUp() {
            document.removeEventListener('mouseup', onMouseUp);
            document.removeEventListener('mousemove', onMouseMove);
        }
    };

    thumb.ondragstart = function() {
        return false;
    };
});
*/