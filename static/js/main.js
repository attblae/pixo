const username = document.getElementById("username").value;
const password = document.getElementById("password").value;
const response = await fetch("/hello", {
                method: "POST",
                headers: { "Accept": "application/json", "Content-Type": "application/json" },
                body: JSON.stringify({
                    name: username,
                    age: userage
                })
            });
            if (response.ok) {
                const data = await response.json();
                document.getElementById("message").textContent = data.message;
            }
            else
                console.log(response);