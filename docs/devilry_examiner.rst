==========================================================
:mod:`devilry_examiner` --- The devilry examiner UI
==========================================================

The devilry examiner UI uses django-simple-rest, ExtJS and CoffeeScript.


Building CoffeeScript
#####################
We use CoffeeScript to write our JavaScript code. This means that you have to
compile the CoffeeScript sources to JavaScript for each change.


Install CoffeeScript
====================
Use the following to install coffeescript in ``src/devilry_examiner/devilry_examiner/buildstatic/devilry_examiner/node_modules/``::

    $ cd src/devilry_examiner/devilry_examiner/buildstatic/devilry_examiner/
    $ npm install

You only have to do this once.


Build the CoffeeScript sources
==============================
To compile the CoffeeScript sources to JS on each change, use the
``coffeeWatch`` task from our Cakefile::

    $ cd src/devilry_examiner/devilry_examiner/buildstatic/devilry_examiner/
    $ node_modules/.bin/cake coffeeWatch

Just keep the ``coffeeWatch`` task running in a terminal while you develop.


Tips
====
For vim, you may want to install Syntastic to get CoffeeScript error messages to get syntax error messages in the editor.


Building the CSS
################
Just like ExtJS, we use compass/sass for our stylesheets. To build the css, run the following::

    $ cd src/devilry_examiner/devilry_examiner/buildstatic/devilry_examiner/
    $ compass watch
