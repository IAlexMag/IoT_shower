// declara vairables

var tipoSeleccionado;
var temperature;
var duracion;

// función para activar o desactivar elementos dependiendo del tipo del baño
function acti(){
    tipoSeleccionado = document.getElementById("tipo_bano").value;
    if (tipoSeleccionado ==="fast" || tipoSeleccionado ==="ahorro" || tipoSeleccionado === "smart"){
        document.getElementById("duracion").disabled = true;
    } else {
        document.getElementById("duracion").disabled = false;
    }
}

// envía los datos por JSON hacía la ruta del backend por método post
function tipoBano(){
    if (tipoSeleccionado ==="fast"){
        temperature = document.getElementById("mislider").value;
        duracion = 8;
    } else if (tipoSeleccionado === "ahorro") {
        temperature = document.getElementById("mislider").value;
        duracion = 5;
    } else{
        temperature = document.getElementById("mislider").value;
        duracion = document.getElementById('duracion').value;
    }
    console.log(temperature, tipoSeleccionado, duracion)
    var data = {
        'tipo_bano': tipoSeleccionado,
        'temperature': temperature,
        'duracion': duracion
    };

    fetch('/pro_bano', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Succes', data);
    })
    .catch((error) => {
        console.error('Error', error)
    })
}
