function sayHello() {
    now = new Date().toLocaleString();
    alert(now);
}

var mess = document.getElementById("mess");
setTimeout(function () {
    mess.style.display = 'none';
}, 3000);