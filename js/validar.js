//criando os objetos dos elementos de texto do form

var nome = document.querySelector("#inputName");
var nomeHelp = document.querySelector("#inputNameHelp");
var ano = document.querySelector("#inputYear");
var anoHelp = document.querySelector("#inputYearHelp");
var email = document.querySelector("#inputEmail");
var emailHelp = document.querySelector("#inputEmailHelp");
var senha = document.querySelector("#inputPassword");
var senhaHelp = document.querySelector("#inputPasswordHelp");
var formResult = document.querySelector("#inputResult");
var meter = document.querySelector("#passStrengthMeter");
var submitButton = document.querySelector("#submitButton");


/*declarando o evento listener para o campos de texto do form. 
Uma vez o foco do campo inputName mude, será chamada a função validarNome*/
nome.addEventListener('focusout', validarNome);
nome.addEventListener('focusout', validarSenha);

function validarNome(){ 
    formResult.textContent = "";
    const regexNome = /^[A-Z][a-z]+$/;
    
    if(!nome.value.trim().match(regexNome) || nome.value.length <= 6){
        nomeHelp.textContent = "Formato de nome inválido"; 
        nomeHelp.style.color="red";
        return false;
    }
    else{
        nomeHelp.textContent = "";
        return true;
    }       
}

ano.addEventListener('focusout', validarAno);
ano.addEventListener('focusout', validarSenha);

function validarAno(e) {
    formResult.textContent = "";
    const regexAno = /^[0-9]{4}$/;

    const anoTrimado = ano.value.trim();

    if(anoTrimado.match(regexAno)==null){
        anoHelp.textContent = "Formato de ano inválido";
        anoHelp.style.color="red";
        return false;
    }
    else{
        var maxYear = 2022;
        var minYear = 1900;
        
        if( parseInt(anoTrimado) > maxYear ){
            anoHelp.textContent = `Ano inválido. O ano não pode ser maior que ${maxYear}.`;
            anoHelp.style.color="red";
            return false;
        }
        else if( parseInt(anoTrimado) < minYear ){
            anoHelp.textContent = `Ano inválido. O ano não pode ser menor que ${minYear}.`;
            anoHelp.style.color="red";
            return false;
        }
        else{
            anoHelp.textContent="";
            return true;
        }        
    }
}

email.addEventListener('focusout', validarEmail);

function validarEmail(e) {
    formResult.textContent = "";

    const regexEmail = /^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.(br|com|net|org)$/;
    if (!email.value.trim().match(regexEmail)) {
        emailHelp.textContent = "Formato de email inválido";
        emailHelp.style.color = "red";
        return false;
    } else {
        emailHelp.textContent = "";
        return true;
    }
}

senha.addEventListener('focusout', validarSenha);

function validarSenha(e) {
    formResult.textContent = "";

    const regexSenha = /^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[@#%&!+*])[a-zA-Z0-9@#%&!+*]{6,20}$/;
    const firstName = nome.value.trim().split(' ')[0];
    const anoVal = ano.value.trim();

    if (senha.value.trim().length == 0) {
        senhaHelp.textContent = "Senha inválida.";
        senhaHelp.style.color = "red";
        meter.value = 0;
        return false;
    }

    if (!senha.value.match(regexSenha)) {
        senhaHelp.textContent = "Senha inválida. Senha deve conter pelo menos 6 caracteres, 1 número, 1 caractere especial e 1 letra maiúscula.";
        senhaHelp.style.color = "red";
        meter.value = 0;
        return false;
    } else {
        nomeHelp.style.color="red";
        if((firstName == undefined) || (anoVal.length == 0)){
            if ((firstName == undefined)){
                nomeHelp.textContent = "Nome é obrigatório";
            }
            if (anoVal.length == 0){
                anoHelp.textContent = "Ano é obrigatório";
            } 
        } else if (senha.value.includes(firstName) || senha.value.includes(anoVal)) {
            senhaHelp.textContent = "Senha inválida. Senha não pode conter nome, sobrenome ou ano de nascimento.";
            meter.value = 0;
            return false;
        }

        const numEspeciais = (senha.value.match(/[@#%&!+*]/g) || []).length;
        const numNumeros = (senha.value.match(/[0-9]/g) || []).length;
        const numMaiusculas = (senha.value.match(/[A-Z]/g) || []).length;
        const totalCaracteres = senha.value.length;

        if (totalCaracteres > 12 && numEspeciais > 1 && numNumeros > 1 && numMaiusculas > 1){
            senhaHelp.style.color = "gray";
            senhaHelp.textContent = 'Senha forte';
            meter.value = 30;
        } else if (totalCaracteres > 8){
            senhaHelp.textContent = 'Senha moderada';
            senhaHelp.style.color = "gray";
            meter.value = 20;
        } else {
            senhaHelp.textContent = 'Senha fraca';
            senhaHelp.style.color = "gray";
            meter.value = 10;
        }
        return true;
    }
}

submitButton.addEventListener('click', validarForm);

function validarForm(e) {
    e.preventDefault();
    var senhaValida = validarSenha();
    var nomeValido = validarNome();
    var anoValido = validarAno();
    var emailValido = validarEmail();

    if (senhaValida && nomeValido && anoValido && emailValido) {
        formResult.textContent = "Dados registrados com sucesso!";
        formResult.style.color = "green";
    } else {
        formResult.textContent = "Formulário inválido!";
        formResult.style.color = "red";
    }
}