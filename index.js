/*
 * Created By: Justin Toyomitsu
 * email: ichitsurume@gmail.com
 * Date Created: November 13th 2020
 * Last Modified:
 * =====================================================
 */

//This is the javascript for the main page
//1. Main page to enter your gmail for google integration
//2. redirect to a dashboard of all the informatino
//3. 

function gmail_submit(){ /* submit button goes here */

    var gmail = document.getElementById("gmail").value

    if(gmail_validate(gmail) == false){
        alert('Something Wrong with Your Input')
    }
    else{
        $.ajax({
            type: "GET",
            url: "index.py",
            data: { email: gmail },
            success: function(data){
                gmail_final(data)
            }
        });
    }
}

function gmail_validate(email){ /* validate gmail */
    var email_check  = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/
    return email_check.test(email)
}

function gmail_final(response){ /* goes to the backend for python to send to the GoogleAPI */
    console.log(response);
}
