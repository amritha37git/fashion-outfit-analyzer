document.addEventListener(
    "DOMContentLoaded",
    function(){

        const form = document.querySelector(
            "form"
        );


        if(form){

            form.addEventListener(
                "submit",
                function(){

                    const button =
                    document.querySelector(
                        ".generate-btn"
                    );


                    if(button){

                        button.innerHTML =
                        "Creating your outfit...";

                        button.disabled = true;

                    }

                }
            );

        }


    }
);