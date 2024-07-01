$(document).ready(function() {
    // Desaparecer a mensagem de alerta apÃ³s 3 segundos
    setTimeout(function () {
        $("#message").alert('close');
    }, 3000);

    // Inicializar o plugin select2
    $('.select2').select2();
});