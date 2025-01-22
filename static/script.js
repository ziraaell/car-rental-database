async function fetchModels(ID){
    try{
        const response = await fetch(`/get_models/${ID}`);
        const data = await response.json();
        document.getElementById('rental_model_id').innerHTML = '<option value="" disabled selected>Wybierz model</option>';

        data.forEach(elem=> {
            const option = document.createElement('option');
            option.value = elem.id_model;
            option.textContent = elem.nazwa_model;
            document.getElementById('rental_model_id').appendChild(option)
        });
        document.getElementById('rental_model_id').disabled = false
    }
    catch(error){
        console.error("Blad podczas pobierania marek", error);
    }
}

// document.getElementsByClassName("close")[0].onclick =  function closeDialog(){
//     document.getElementById('flash-messages').style.display = 'none';
// }

if(document.getElementById('rental_brand_id'))
{
    document.getElementById('rental_brand_id').addEventListener('change', function (){
        const brand_id = this.value;
        fetchModels(brand_id)
    })
}

if(document.getElementsByClassName("close")[0]){
document.getElementsByClassName("close")[0].onclick =  function closeDialog(){
    document.getElementById('flash-messages').style.display = 'none';
}
}

if(document.getElementById('clientInput')){
document.getElementById('clientInput').addEventListener('input', function () {
    const inputValue = this.value; // Wartość wpisana przez użytkownika
    const datalist = document.getElementById('clients');
    const selectedOption = Array.from(datalist.options).find(option => option.value === inputValue);

    if (selectedOption) {
        const clientId = selectedOption.getAttribute('data-id'); // Pobranie data-id
        document.getElementById('clientId').value = clientId; // Ustawienie ukrytego pola
    } else {
        document.getElementById('clientId').value = ''; // Wyczyść, jeśli brak dopasowania
    }
});
}




