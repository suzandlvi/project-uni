function showRegisterFormError(status, res) {
    let formMessage = $('#form-message')
    if (formMessage.length !== 0) {
        formMessage.remove()
    }
    $('#submit-register-btn').after(`<p class='text-${status}' id="form-message">${res.message}</p>`)
}


let registerForm = $('#register-form');
registerForm.submit(function (e) {
    e.preventDefault()
    $.ajax({
        method: "POST",
        url: e.target.action,
        data: registerForm.serialize(),
        success: function (res) {
            if (res.status === 'success') {
                showRegisterFormError('success', res)
                setTimeout(() => {
                    location.replace('/accounts/login')
                }, 2000)
            } else if (res.status === 'error') {
                showRegisterFormError('danger', res)
            }
        },
        error: function (res) {
            showNotification({message:'لطفا از اتصال اینترنت خود اطمینان حاصل فرمایید', status:'error'}, 'شکست')
        }
    })
})

// {#var frm = $('#register-form');#}
// {#frm.submit(function (e) {#}
// {#    e.preventDefault()#}
// {#    var formData = new FormData(this);#}
// {#    let cookie = document.cookie#}
// {#    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)#}
// {#    $.ajax({#}
// {#        async: true,#}
// {#        type: frm.attr('method'),#}
// {#        url: frm.attr('action'),#}
// {#        data: formData,#}
// {#        cache: false,#}
// {#        processData: false,#}
// {#        contentType: false,#}
// {#        headers: {#}
// {#            'X-CSRFToken': csrfToken#}
// {#        },#}
// {#        success: function (res) {#}
// {#            if (res.status === 'success') {#}
// {#                $('#submit-register-btn').after(`<p class='text-danger'>${res.message}</p>`)#}
// {#            } else if (res.status === 'failed') {#}
// {#                $('#submit-register-btn').after(`<p class='text-danger'>${res.message}</p>`)#}
// {#            }#}
// {#        },#}
// {#        error: function (res) {#}
// {#            console.log('not okab')#}
// {#        }#}
// {#    })})#}

