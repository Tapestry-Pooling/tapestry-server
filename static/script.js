function formToJson(fd) {
    let jo = {};
    for (const [k, v] of fd.entries()) {
            jo[k] = v;
    }
    return JSON.stringify(jo);
}

window.authToken = ""; // to be used in header X-Auth
window.phone = ""; // to be used in header X-Mob

function genericSuccessHandler(event) { alert(event.target.responseText);}
function genericErrorHandler(event) {alert( 'Oops! Something went wrong.' );}
function setPhone(event) {
        var j = JSON.parse(event.target.responseText);
        window.phone = j.phone;
}
function setAuthToken(event) {
        var j = JSON.parse(event.target.responseText);
        console.log(j)
        window.authToken = j.token;
        window.phone = j.phone;
}

function formPostHandler(elementName, url, success, error) {
    function sendData(form, url) {
            const XHR = new XMLHttpRequest();
            XHR.addEventListener( "load", (success) ? success : genericSuccessHandler);
            XHR.addEventListener( "error", ( error ) ? error : genericErrorHandler );
            XHR.open( "POST", url );
            XHR.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            XHR.send( formToJson(new FormData( form )) );
    }
    // Access the form element...
    let form = document.getElementById( elementName );
    form.addEventListener( "submit", function ( event ) {
            event.preventDefault();
            sendData(form, url);
    } );
}
document.getElementById("TestUpload").addEventListener("click", function(){
        if (window.authToken && window.phone) {
                const XHR = new XMLHttpRequest();
                XHR.open( "POST", "/test_data" );
                XHR.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                XHR.setRequestHeader("X-Auth", window.authToken);
                XHR.setRequestHeader("X-Mob", window.phone);
                XHR.send(JSON.stringify([0.1, 0.1, 0.1, 0.1, 0, 0.1, 0.2, 0.3, 0.1, 0.1, 0.1, 0.1, 0, 0.1, 0.2, 0.3]));
        }
        else {
                alert("Inavlid auth Token, validate OTP first")
        }
      });
window.addEventListener( "load", () => formPostHandler("reqOtp", "/request_otp", setPhone));
window.addEventListener( "load", () => formPostHandler("valOtp", "/validate_otp", setAuthToken));