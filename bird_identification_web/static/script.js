/* 
(C) Hynek V. Svobodny, 2024

This script contains the common code for all pages
*/


// Sets the language and submits the language form
function submitLangForm(form, lang) {
    form['language'].value = lang;
    form.submit();
}

document.getElementsByClassName('lang-change').forEach(element => {
    element.addEventListener('click', submitLangForm)
});
