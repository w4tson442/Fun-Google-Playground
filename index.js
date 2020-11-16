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
    console.log("test");
    $.ajax({
        type: "GET",
        url: "index.py",
        data: { email: "email" },
        success: gmail_final(resopnse)
    });
    console.log("test");
}

function gmail_validate(){ /* validate gmail */

}

function gmail_final(response){ /* goes to the backend for python to send to the GoogleAPI */
    console.log(response);
}
