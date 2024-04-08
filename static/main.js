// Получаем элементы
var modal = document.getElementById("myModal");
var btn = document.getElementById("openModal");
var span = document.getElementsByClassName("close")[0];
var generateButton = document.getElementById("generateButton");
var modalForm = document.getElementById("modalForm");
var errorMessageElement = document.getElementById("error-message");
var inputs = document.querySelectorAll('input[type="text"]');

function downloadFile() {
  window.location.href = "/download";
}

function updateImage(imageUrl) {
  var imageElement = document.getElementById("plot-image");
  if (imageElement) {
    imageElement.src = "data:image/png;base64," + imageUrl;
  }
}

function generatePlot(l1, l2, l3, l4, l5, n1, n2, n3, n4, n5) {
  // Создаем экземпляр XMLHttpRequest
  var xhr = new XMLHttpRequest();

  // Устанавливаем метод и URL-адрес запроса
  xhr.open("POST", "/generate_plot", true);

  // Устанавливаем заголовок Content-Type
  xhr.setRequestHeader("Content-Type", "application/json");

  // Определяем функцию, которая будет вызвана при успешном завершении запроса
  xhr.onload = function () {
    if (xhr.status === 200) {
      // Обрабатываем успешный ответ от сервера
      var response = JSON.parse(xhr.responseText);
      updateImage(response.plot_img_url);
    } else {
      // Обрабатываем ошибку, если сервер вернул код ответа, отличный от 200
      console.log("Произошла ошибка: " + xhr.statusText);
    }
  };

  // Определяем функцию, которая будет вызвана в случае ошибки запроса
  xhr.onerror = function () {
    console.log("Произошла ошибка запроса");
  };

  // Преобразуем параметры в формат JSON и отправляем их на сервер
  var data = JSON.stringify({
    l1,
    l2,
    l3,
    l4,
    l5,
    n1,
    n2,
    n3,
    n4,
    n5,
  });
  xhr.send(data);
}

// Функция открытия модального окна
btn.onclick = function () {
  modal.style.display = "block";
};

// Функция закрытия модального окна
span.onclick = function () {
  modal.style.display = "none";
};

// Закрытие модального окна при клике вне его
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

// Привязываем функцию generatePlot() к кнопке
generateButton.onclick = function () {
  validateForm();
};

function clearAllInputs() {
  inputs.forEach(function (input) {
    input.value = ""; // Очистка значения инпута
  });
}

// Функция для генерации графика
function sendForm() {
  // Получаем значения из инпутов
  var values = [];
  var inputs = document.getElementsByClassName("modal-input");
  for (var i = 0; i < inputs.length; i++) {
    values.push(Number(inputs[i].value));
  }

  generatePlot(...values);
  clearAllInputs();
  modal.style.display = "none";
  errorMessageElement.textContent = "";
}

function validateForm() {
  var numInputs = 5;

  for (var i = 1; i <= numInputs; i++) {
    var λ = document.getElementById("λ" + i);
    var n = document.getElementById("n" + i);

    if (λ.value === "") {
      λ.classList.add("error");
    } else {
      λ.classList.remove("error");
    }

    if (n.value === "") {
      n.classList.add("error");
    } else {
      n.classList.remove("error");
    }
  }

  var anyEmpty = document.querySelectorAll(".error").length > 0;

  if (anyEmpty) {
    showErrorMessage("Пожалуйста, заполните все поля");
  } else {
    sendForm();
  }
}

function showErrorMessage(message) {
  errorMessageElement.textContent = message;
}
