// Создаем распознаватель
var recognizer = new webkitSpeechRecognition();

//считывание без остоновки
//recognizer.continuous = true;

// Ставим опцию, чтобы распознавание началось ещё до того, как пользователь закончит говорить
recognizer.interimResults = true;

// Какой язык будем распознавать?
recognizer.lang = 'ru-Ru';

var text;
var synth = window.speechSynthesis;
var stop_per = 0;
var toggle = 0;

// Используем колбек для обработки результатов
recognizer.onresult = function (event) {
    var result = event.results[event.resultIndex];
    if (result.isFinal) {
        console.log('Конечный разультат: ', result[0].transcript);
        text = result[0].transcript;
        talk();
    }
}

recognizer.onend = function () {
    if (stop_per != 1)
    {
        wait();
    }
    stop_per = 0;

}

function stop() {
    stop_per = 1;
    if recognizer.s
    recognizer.abort();
}

function wait() {
    interval = setInterval(function () {
        if (synth.speaking === false) {
            clearInterval(interval);
            speech();
        }
    }, 500);
}

function speech() {
// Начинаем слушать микрофон и распознавать голос
    recognizer.start();
}

function talk() {

    var utterance = new SpeechSynthesisUtterance(text);
    synth.speak(utterance);


}

function toggler() {
    if (toggle === 0)
    {
        speech();
        toggle = 1;
    }
    else
    {
        stop();
        toggle = 0;
    }

}
