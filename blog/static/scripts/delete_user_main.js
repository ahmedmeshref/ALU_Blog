function delete_user(user_id, c_user) {
    let result = confirm("Deleting this user will wipe all of his data. Are you sure?");
    if (result) {
        delete_user_card(user_id, c_user);
    } else {
        return;
    }
}


function delete_user_card(user_id, c_user) {
    // if the current user is not a super_admin
    console.log("I am inside");
    if (c_user != 2) {
        alert("Method is not allowed");
        reutrn;
    }
    console.log("I am inside");
    let article = document.getElementsByClassName(`media content-section ${user_id}`);
    for (let i = 0; i < article.length; i++) {
        article[i].hidden = true;
    }
    console.log("I deleted article");
    fetch(`${window.origin}/delete_user`, {
        method: "POST",
        body: JSON.stringify({
            "user_id": user_id
        }),
        headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(resVal => console.log(`username: ${resVal['username']}, email: ${resVal['email']} `))
        .catch(err => console.log(err))
}