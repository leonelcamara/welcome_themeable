Welcome Themeable
==================
web2py welcome application made themeable whether it wants to or not. **Do not use this** as it is just a proof of concept and an exploration into how to implement theming in web2py.

Instructions:
- install latest web2py
- copy this app to the applications/* folder

To make a theme:
- go to application/welcome_themeable/static/themes
- Create a folder with your theme name
- Create any view files you want, they will be directly accessible to the views as if they were on views/
- Namely you will probably want to create a layout.html
- Add a css and js folder to your theme and use them in layout.html
- Add a run.py file, it can be empty, if it's not it is executed in the models so use it to configure stuff such as formstyles

Examples:
- Look into the ones in static/themes
- Don't pay attention to how poorly the pure one is implemented.
