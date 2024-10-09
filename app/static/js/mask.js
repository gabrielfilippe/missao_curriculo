$(document).ready(function() {
    $('#id_data_de_nascimento').mask('00/00/0000');
    $('#id_rg').mask('00.000.000-0');
    $('#id_cpf').mask('000.000.000-00');
    $('#id_telefone').mask('(00) 00000-0000');
    $('#id_email').mask('A', {
        translation: {
            'A': { pattern: /[a-z0-9\.\-@]/, recursive: true }
        }
    });
    $('#id_cep').mask('00000-000');
    // $('.date-field').mask('00/00/0000');
});