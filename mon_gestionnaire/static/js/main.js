
document.addEventListener('DOMContentLoaded', function () {
const generate_button = document.querySelector('.nav__register');
const password_field = document.querySelector('.gen--pass');
const savepass_form = document.querySelector('.save__pass');
const genPassBtn = document.querySelector('.btn--one');
const viewPassBtn = document.querySelector('.btn--two');
const searchPassBtn = document.querySelector('.btn--three');
const genPassDiv = document.querySelector('.dashboard__generate--password');
const viewPassDiv = document.querySelector('.dashboard__view--password');
const searchPassDiv = document.querySelector('.dashboard__search--password');
const table = document.querySelector('.password--table');
const table_two = document.querySelector('.search__pass--table');
const allDashboardDiv = [genPassDiv, viewPassDiv, searchPassDiv];
const allDashboardBtn = [genPassBtn, viewPassBtn, searchPassBtn];

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

generate_button.addEventListener('click', async function () {
    let response = await fetch('/gen_pass');
    let data = await response.json();
    password_field.value = data['password'];
});

savepass_form.addEventListener('submit', async function (e) {
    e.preventDefault();
    let message = document.querySelector('.success__message');
    let website_name = document.querySelector('.gen--website');
    let user_name = document.querySelector('.gen--username');
    let generated_password = document.querySelector('.gen--pass');

    let response = await fetch('/save_pass', {
        method: "POST",
        body: JSON.stringify({
            'user': session_username,
            'website': website_name.value.toLowerCase(),
            'username': user_name.value,
            'password': generated_password.value,
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });

    let data = await response.json();

    if (data['message'] == 'Saved') {
        [website_name, user_name, generated_password].forEach(input => input.value = '');
        message.textContent = "Mot de passe enregistré avec succès";
    } else if (data['message'] == 'Exists') {
        message.textContent = "Un compte existe déjà avec ce nom d'utilisateur.";
    } else {
        message.textContent = "Oups ! Une erreur est survenue.";
    }
    setTimeout(() => message.textContent = '', 3000);
});



const resetDashboard = function () {
    allDashboardDiv.forEach(div => div.classList.add('hide'))
    allDashboardBtn.forEach(div => div.classList.remove('active'))
}

genPassBtn.addEventListener('click', function () {
    resetDashboard()
    genPassDiv.classList.remove('hide');
    this.classList.add('active')
})

const deletePassword = async function (e) {
    if (!e.target.classList.contains('delete_password')) return
    const table_row = e.target.closest('tr');
    const data = {
        "website": table_row.querySelector('.website--js').textContent,
        "username": table_row.querySelector('.username--js').textContent,
        "password": table_row.querySelector('.password--js').textContent,
    }
    let response = await fetch('/del_pass', {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    response = await response.json()
    if (response.message == "OK") {
        table_row.parentNode.removeChild(table_row)
    }
}

const togglePasswordsVisibility = function() {
    document.querySelectorAll('.password--js').forEach(function(passwordElement) {
        passwordElement.classList.toggle('hidden-password');
    });
};


const addDataToTable = function (data, table) {
    let passwords = data['passwords']
    passwords.forEach(password => {
        const table_row = `
            <tr>
                <td class="website--js">${password.website}</td>
                <td class="username--js">${password.username}</td>
                <td>
                    <span class="password--js hidden-password">${password.password}</span>
                </td>
                <td>
                    <button class="delete_password" type="submit">Supprimer</button>
                </td>
            </tr>
            `
        table.insertAdjacentHTML('beforeend', table_row);
    })
}


viewPassBtn.addEventListener('click', async function () {
    if (this.classList.contains('active')) return;
    table.innerHTML = null;
    let table_headers = `
            <tr>
                <th>Site Web / Application</th>
                <th>Nom d'utilisateur</th>
                <th>Mot de passe</th>
                <th>Supprimer</th>
            </tr>
            `
    table.insertAdjacentHTML('beforeend', table_headers)
    resetDashboard()
    viewPassDiv.classList.remove('hide')
    this.classList.add('active')
    let data;
    data = await fetch("/get_pass")
    data = await data.json()
    addDataToTable(data, table);
})

table_two.addEventListener('click', async (e) => {
    if (e.target.classList.contains("search_password")) {
        const search_string = document.querySelector('.search_password_input').value
        if (!search_string) return;
        data = await fetch(`/search_pass`, {
            method: "POST",
            body: JSON.stringify({
                'username': session_username,
                'website': search_string.toLowerCase(),
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
        data = await data.json()
        table_two.innerHTML = null;
        let table_headers = `
            <tr>
                <th colspan="3"><input placeholder="Rechercher une appli ou un site" class="search_password_input" type="text"></th>
                <th><button class="search_password" type="submit">Rechercher</button></th>
            </tr>
            `
        table_two.insertAdjacentHTML('beforeend', table_headers)
        addDataToTable(data, table_two)
    } else if (e.target.classList.contains('delete_password')) {
        deletePassword(e)
    } else return;
})

searchPassBtn.addEventListener('click', async function () {
    resetDashboard()
    searchPassDiv.classList.remove('hide')
    this.classList.add('active')
    table_two.innerHTML = null;
    let table_headers = `
            <tr>
                <th colspan="3"><input placeholder="Rechercher une appli ou un site" class="search_password_input" type="text"></th>
                <th><button class="search_password" type="submit">Rechercher</button></th>
            </tr>
            `
    table_two.insertAdjacentHTML('beforeend', table_headers)
})

table.addEventListener('click', deletePassword);

const togglePasswordsButton = document.getElementById('togglePasswords');
    const toggleSearchPasswordsButton = document.getElementById('toggleSearchPasswords');

    if (togglePasswordsButton) {
        togglePasswordsButton.addEventListener('click', function() {
            document.querySelectorAll('.password--js').forEach(function(el) {
                el.classList.toggle('hidden-password');
            });
        });
    }

    if (toggleSearchPasswordsButton) {
        toggleSearchPasswordsButton.addEventListener('click', function() {
            document.querySelectorAll('.dashboard__search--password .password--js').forEach(function(el) {
                el.classList.toggle('hidden-password');
            });
        });
    }
});
