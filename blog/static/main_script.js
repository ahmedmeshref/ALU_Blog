
// add new post form
document.getElementById("new_post").onsubmit = function (e) {
    e.preventDefault();
    const title = document.getElementById("title");
    const title_val = title.value;
    const description = document.getElementById("description");
    const description_val = description.value;
    let invalid_title = document.getElementById("invalid_title");
    let invalid_description = document.getElementById("invalid_description");
    let success = true;
    if (title_val.length > 50 || title_val.length < 3) {
        title.className = "form-control is-invalid";
        invalid_title.innerHTML = "title should be between 3 to 50 characters long";
        success = false;
    }
    if (description_val.length > 500 || description_val.length < 10) {
        description.className = "form-control is-invalid";
        invalid_description.innerHTML = "description should be between 10 to 500 characters long";
        success = false;
    }
    if (success) {
        fetch("/new_post/", {
            method: "POST",
            body: JSON.stringify({
                'title': title_val,
                'description': description_val
            }),
            headers: {
                'Content-type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(resVal => {
            console.log(resVal)
        })
    }
}