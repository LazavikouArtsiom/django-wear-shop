checkout_button.onclick = function(){
    let checkout = document.getElementsByClassName("checkout")[0]
    checkout.style.display = 'block'

    form = document.getElementById('orderForm')
    li = form.querySelectorAll('li')
    input = form.querySelectorAll('input')
    captcha_0 = document.getElementById('id_captcha_0')
    captcha_1 = document.getElementById('id_captcha_1')

    for (var i = 0; i < li.length; i++){
        if (i > 6 && i != 14 && i != 15){
           li[i].style.display = 'none'
        }
    }

    captcha_0 = document.getElementById('id_captcha_0')
    captcha_1 = document.getElementById('id_captcha_1')
}

id_payment.onclick = function(){
    let option = document.getElementById('id_payment')
    index = option.options.selectedIndex
    form = document.getElementById('orderForm')
    li = form.querySelectorAll('li')
    if (index == 8  && i != 14){
        for (var i = 0; i < li.length; i++){
            if (i > 6){
               li[i].style.display = 'block'
               input = li[i].querySelectorAll('input')[0]
               input.required = true
            }
        }
    }
    else{
        for (var i = 0; i < li.length; i++){
            if (i > 6  && i != 14 && i != 15){
               li[i].style.display = 'none'
               input = li[i].querySelectorAll('input')[0]
               input.required = false
            }
        }
    }

}

