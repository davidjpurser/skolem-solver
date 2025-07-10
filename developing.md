# How to structure the code

- Only code inside a html folder is visible on the webserver. 
  - Code in the html folder is accessible directly
  - Code in an html folder inside an algorithm folder is accessed at /algorithm/algorithm_folder_name/
- Algorithms should be developed in their own folder
- Common elements should be developed in `utils` folder
- Run ./buildsage.sh to convert .sage files into .py files.