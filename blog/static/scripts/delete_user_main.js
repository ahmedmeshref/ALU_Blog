

document.getElementById("delete_user_btn").onclick =
    function (){
    let result = confirm("Are you sure to delete?");
    if(result){
        delete_user();
    } else {
        return;
    }
}


// function delete_user_card() {
//     let data = document.getElementById("delete_user_btn").value;
//     let , admin_type;
//     [user_id, admin_type] = data.match(/[0-9]+/g);
//     if (admin_type != 2) {
//         alert("Method is not allowed");
//         reutrn;
//     }
//     let article = document.getElementById(`${user_id}`);
//     if (article) article.remove();
//     fetch(`${window.origin}/delete_user`, {
//         method: "POST",
//         body: JSON.stringify({
//             "user_id": user_id
//         }),
//         headers: {
//             'Content-type': 'application/json'
//         }
//     })
//     .then(response => response.json())
//     .then(resVal => console.log(resVal['user_id']))
//     .catch(err => console.log(err))
//
// }