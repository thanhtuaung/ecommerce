var updateBtns = document.getElementsByClassName('update-cart')

for(i=0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        var qty = parseInt(this.dataset.qty)
        
        console.log('productId:', productId, 'Action:', action)
		console.log(user)

        // if(action == 'add') {
        //     qty += 1
        // } else if(action == 'remove') {
        //     qty -= 1
        // }


		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		} else {
			updateUserOrder(productId, action)
		}

        document.getElementById('cart-total').innerHTML = qty

    })
}

function addCookieItem(productId, action) {

    if(action == 'add') {
        if(cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}
        } else {
            cart[productId]['quantity'] += 1
            console.log('Hello')
        }
    } else if (action == 'remove') {
        cart[productId]['quantity'] -= 1
        
    }

    console.log('Cart:', cart)
    
    if(cart[productId]['quantity'] <= 0) {
        delete cart[productId]
    }

    delete document.cookie['cart']

    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}


function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data....')

    var url = '/update-item/'

    fetch(url, {
        method: "POST",
        headers : {
            "Content-Type": "application/json",
            "X-CSRFTOKEN": csrftoken,
        },
        body: JSON.stringify({'product': productId, 'action': action})
    })
    .then((response)=> {
        return response.json()
    })
    .then((data) => {
        console.log('data', data)
        location.reload()
    })
}
