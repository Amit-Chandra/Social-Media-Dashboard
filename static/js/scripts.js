
document.addEventListener('DOMContentLoaded', function() {
    var loginButton = document.getElementById('login-button');
    if (loginButton) {
        loginButton.addEventListener('click', function(event) {
            console.log('Login button clicked!');
        });
    }
});
