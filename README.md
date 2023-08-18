# library_microservice
A library microservice api that allows you save,borrow and fetch books


To start the project, run the command "docker-composer up build"
the api routes are as follows 

For Admin

http://127.0.0.1:8000/api/books

http://127.0.0.1:8000/api/books/id

http://127.0.0.1:8000/api/users/
<!-- 
http://127.0.0.1:8000/api/user-books-borrowed/

http://127.0.0.1:8000/api/unavailable-books/ -->


For Client

http://127.0.0.1:8080/api/books/ 

http://127.0.0.1:8080/api/books/id/

http://127.0.0.1:8080/api/books/id/borrow/

http://127.0.0.1:8080/api/books/enrol-user/
