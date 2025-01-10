    setTimeout(() => {
        document.getElementById('spsc').classList.toggle('fade');
    }, 2000);

    function confirmEmail() {
        if (confirm("Do you want to proceed to email?")) {
            window.location.href = "mailto:shizocatto@gmail.com";
        }
        else {
            console.log('Edi wag.');
          }
    }