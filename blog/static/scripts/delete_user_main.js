function delete_user(user_id, c_user_type) {
    let result = confirm("Deleting this user will wipe all of his data. Are you sure?");
    if (result) {
        delete_user_card(user_id, c_user_type);
    } else {
        return;
    }
}


function delete_user_card(user_id, c_user_type) {
    // if the current user is not a super_admin
    if (c_user_type === 0) {
        alert("Method is not allowed");
        reutrn;
    }
    let article = document.getElementsByClassName(`media content-section ${user_id}`);
    for (let i = 0; i < article.length; i++) {
        article[i].hidden = true;
    }
    console.log("User card and posts are deleted successfully")
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