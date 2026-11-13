function login(e) {
    e.preventDefault();
    $.ajax(
    {
        url: '/signin',
        method: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({
            email: this.email.value,
            password: this.password.value
        }),
        success: function (data) {
            localStorage.setItem(
                "user_name", data.user_name
            );
            localStorage.setItem(
                "access_token", data.access_token
            );
            localStorage.setItem(
                "refresh_token", data.refresh_token
            );
            localStorage.setItem(
                "token_type", data.token_type
            );
            // document.cookie="access_token=Bearer " + localStorage.getItem('access_token') + "; domain=test.test";
            document.cookie="access_token=Bearer " + localStorage.getItem('access_token');
            window.location.assign('/cases')

        },
        // success: function (data) {
        //     // cookie уже поставлена сервером (HttpOnly) — JS её не видит и не трогает
        //     localStorage.setItem("user_name", data.user_name);   // можно оставить только это
        //     window.location.assign('/cases');
        // },
//        error: function (data) {
//            alert("user or password invalid")
//            window.location.assign('/login')
//        }
        error: function (data) {
            if (data.responseJSON.detail === "user or password invalid") {
                let loginForm = document.getElementById("loginForm")
                let emailLabel = document.getElementById("emailLabel")
                emailLabel.innerHTML = "User or Password Invalid";
                loginForm.email.className = "form-control border-warning"
            }
            else {
                alert("user or password invalid")
                window.location.assign('/login')
                }
        }
    })
}

$("#loginForm").on("submit", login)

function register(e) {
    e.preventDefault();
    $.ajax(
    {
        url: '/signup',
        method: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(
        {
            email: this.login.value,
            password: this.password.value,
            confirm_password: this.conf_password.value
        }),
        success: function (data) {
            window.location.assign('/login')
        },
        error: function (data) {
            alert("something wrong")
            window.location.assign('/register')
        }
    })
}

$("#registerForm").on("submit", register)

function Form(e) {
    e.preventDefault();
    $.ajax(
    {
        url: '/api/v1/cases',
        method: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(
        {
            title: this.title.value,
            body: this.body.value,
            category: this.category.value
            }),
        success: function(data) {
            console.log(data)
            alert("Case Added!");
            window.location = "/cases/list/";
        }
        })
    }

function FormC(e) {
    e.preventDefault();
    pathname = window.location.pathname;
    caseID = pathname.split('/')[3]
    $.ajax(
    {
        url: '/api/v1/cases/' + caseID + '/comment',
        method: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(
        {
            text: this.text.value
            }),
        success: function(data) {
            console.log(data)
            alert("Comment Added!");
            window.location = "/cases/list/" + caseID;
        }
        })
    }

$("#CommentForm").on("submit", FormC)
$("#CaseForm").on("submit", Form)

function myFunction() {
  var x = document.getElementById("password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function myFunctionConf() {
  var x = document.getElementById("conf_password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}