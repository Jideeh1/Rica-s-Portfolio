window.onload = function() {
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

    document.querySelectorAll('.img').forEach(image => {
        image.onclick = () => {
            console.log("Image clicked:", image.getAttribute('src')); //This is for debugging only ;^;
            document.querySelector('.modal').style.display = 'block';
            document.querySelector('.modal img').src = image.getAttribute('src');
        };
    });
    
    document.querySelectorAll('.modal span').forEach(span => {
        span.onclick = () => {
            console.log("Modal closed"); //You don't know how much trouble I went through without debugging! Learned the leason hard
            document.querySelector('section .modal').style.display = 'none';
        };
    });
    
};