<h1 align="center">
  Googlio
</h1>
<p align="center">
  Google Information Dashboard of Google Doc, Google Calendar and Gmail built with <a href="https://www.djangoproject.com" target="_blank">django</a>, <a href="https://www.python.org/" target="_blank">Python</a> and <a href="https://console.developers.google.com" target="_blank">Google API</a>
</p>

![demo](https://github.com/w4tson442/Fun-Google-Playground/blob/main/display_image/Login_Screen.png)
![demo](https://github.com/w4tson442/Fun-Google-Playground/blob/main/display_image/Google_Doc_example.png)
![demo](https://github.com/w4tson442/Fun-Google-Playground/blob/main/display_image/Google_Gmail_example.png)
![demo](https://github.com/w4tson442/Fun-Google-Playground/blob/main/display_image/Google_Calendar_example.png)

## :runner: SET UP
1. This project works with [Apache](https://httpd.apache.org/) and [MYSQL](https://www.mysql.com/) I recommend using my [VM](https://github.com/w4tson442/AMU-virtualmachine) which has both
2. Run Main Script
   ```sh
   source start.sh
   ```
3. Visit the site! (🚨 The site URL should end with /front)

## :gear: USEFUL COMMANDS
1. Create Admin User "I want to check the DB and other settings for Django" (🚨 The site URL should end with /admin)
   ```sh
   source project_env/bin/activate
   ./manage.py createsuperuser
   ./manage.py collectstatic
   deactivate
   ```
---
**original creator:** Justin Ichiro Toyomitsu  
**email:** ichitsurume@gmail.com
