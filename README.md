# FLASK SIMPLE MVC APPLICATION (Alpha 0.01)

## Description:

This light weight framework crete a skelet of MVC, base on Flask web framework and python

You can manage some option for your project.
For exemple you can easy change, authorization method, app config, admin temaplte and many more

## Install 

For instal you need to clone github repo (only for Alpha version) or copy just one file named: create_app.py

To clone repositories:

```bash
git clone https://github.com/Maruda-Patryk/Flask-SMVCA.git
```

Your file tree should look like:

Flask-SMVCA
|-create_app.py
...

## Quick Start 

1. Go to the folder where you have 'create_app.py' file
2. create json config file by 
    ```bash
    python create_app.py <name_of_your_project>
    ```

    After that your file tree should look like:
    |-create_app.py
    |-config.json
    ...
    
3. In config.json you can change option for your project (Documentation should apper on this [page](http://patryk-maruda.pl/flask-smvca/doc) soon if this page dosn't work that's mean that i dosn't finished docs yet)
4. For create project with option wich was given in config.json just type again:
    ```bash
    python create_app.py <name_of_your_project>
    ```

That's all, you should have a MVC aplication with authorization, RBAC(role-based access control)

after those operation you file tree should look like:

```tree
|-main_.py
|-config.py
|-manage.py
|-create_app.py
|-requirements.txt
|-<app_name>
    |-__init__.py
    |-auth
        |-__init__.py
        |-controllers.py
        |-forms.py
        |-models.py
    |-main
    	|-__init__.py
        |- controllers.py
    |-templates
    	|-auth
        	|-login.htlm
            |-register.html
        |-404.html
        |-base.html
```