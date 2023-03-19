start_service:
	docker run --name mariadb -p 3306:3306 -d --env-file $(PWD)/mariadb/.env mariadb:10.6.12
	docker run --name prometheus -p 9090:9090 -p 5000:5000 -d -v prometheus:/etc/prometheus prom/prometheus:v2.37.6
	docker run --name phpmyadmin -p 8080:80 --link mariadb:db -d --env-file $(PWD)/phpmyadmin/.env phpmyadmin:5.2.1

stop_service:
	docker stop mariadb
	docker stop prometheus
	docker stop phpmyadmin

clean:
	docker rm -f mariadb
	docker rm -f prometheus
	docker rm -f phpmyadmin