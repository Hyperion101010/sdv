# Developer Guide

For updating User Interface and adding/removing input simply update html input/div tags in [site/index.html](src/site/index.html)(inside any `<fieldset class='pdfData'>`)  rest will update automatically.



#### HTML syntax that the web-app understands to read/write PDF on github:

Note: In below syntax 'name' attribute matters! 'name' attribute maps to corresponding key in PDF.

* Adding simple key:value 

  ```json
  { "owner" : "" }
  ```

  ```html
  <input name='owner'>
  ```

  <br>

* Adding Object 

  ```json
  "lab" : { 
             "owner": "", 
             "area": "" 
          }
  ```

  ```html
  <div name='lab'>
      <input name='owner'>
      <input name='area'>
  </div>
  ```

  <br>

* Adding array example:

  ```json
  "lab_access": [
                  {
                     "owner": "",
                     "area": ""
                   }
                ]
  ```

  ```html
  <div class="arr" name='lab_access'>
  	<input name='owner'>
      <input name='area'>
  </div><div class="add-button" onclick="duplicate(this)"></div>
  ```

  <br>

* Adding simple key:value but limiting input values option

  ```json
  "lab": 'lab1'
  OR
  "lab": 'lab2'
  OR
  "lab": 'lab5'
  ```

  ```html
  <select name='lab'>
  	<option value="lab1">some lab1 text</option>
  	<option value="lab2">some lab2 text</option>
      <option value="lab5">some lab5 text</option>
      
  </select><i class="select"></i>
  ```

  <br>

* Representing PDF nested keys directly (using Dot convention)

  ```
  "lab" : { 
             "owner": "", 
             "area": "" 
          }
  ```

  ```html
  <input name='lab.owner'>
  <input name='lab.area'>
  ```

  

  