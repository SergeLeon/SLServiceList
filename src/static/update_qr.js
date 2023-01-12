let img = document.getElementById("qrcode")
let form = document.forms[0]
async function updateQR() {
    let form_data = Object.values(form).reduce((obj,field) => { obj[field.name] = field.value; return obj }, {})

    let request = new Request(
        "",
        {headers: {'X-CSRFToken': form_data["csrfmiddlewaretoken"]}}
    );

    let response = await fetch(request, {
         method: 'POST',
         mode: 'same-origin',
         body: new FormData(form),
    });

    data = await response.blob();
    if (data.size) {
        img.src = URL.createObjectURL(data)
    }
    else{
        alert("Too much data for a QR code")
    }
}
form.addEventListener('change', updateQR);
updateQR()