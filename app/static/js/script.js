$(document).ready(function() {
    // Desaparecer a mensagem de alerta após 3 segundos
    setTimeout(function () {
        $("#message").alert('close');
    }, 3000);

    // Inicializar o plugin select2
    $('.select2').select2();
});